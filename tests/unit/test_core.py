"""Native public contracts and configuration validation."""

import pytest

from pydatarheo import (
    Config,
    ConfigError,
    MemorySource,
    RecordError,
    Source,
    Stream,
    transform_records,
)


def test_config_nested_mutation_preserves_snapshot():
    values = {"nested": {"token": "private"}}
    config = Config(values)
    values["nested"]["token"] = "changed"
    returned = config["nested"]
    returned["token"] = "changed again"
    assert config["nested"] == {"token": "private"}
    assert "private" not in repr(config)
    assert len(config) == 1
    assert list(config) == ["nested"]


@pytest.mark.parametrize("text", ["[]", "null", "{", '{"key": NaN}', '{"key": 1e999}'])
def test_config_invalid_json_raises_config_error(text):
    with pytest.raises(ConfigError):
        Config.from_json(text)


def test_config_valid_json_parses_mapping():
    assert Config.from_json('{"path": "sample.jsonl"}')["path"] == "sample.jsonl"


@pytest.mark.parametrize("value", [None, [], {1: "bad"}])
def test_config_invalid_mapping_raises_config_error(value):
    with pytest.raises(ConfigError):
        Config(value)


@pytest.mark.parametrize("name", ["", " ", 1])
def test_stream_invalid_name_raises_config_error(name):
    with pytest.raises(ConfigError):
        Stream(name)


def test_source_abstract_contract_cannot_instantiate():
    with pytest.raises(TypeError):
        Source()


def test_memory_source_reads_independent_snapshots(records):
    source = MemorySource({"records": records})
    records[0]["name"] = "changed"
    first = list(source.read())
    first[0]["name"] = "changed again"
    assert list(source.read())[0]["name"] == "Ada"
    assert source.streams() == (Stream("records"),)
    assert source.check() is None


def test_source_unknown_stream_raises_config_error(records):
    with pytest.raises(ConfigError):
        list(MemorySource({"records": records}).read("missing"))


@pytest.mark.parametrize("size", [0, -1, True, 1.5])
def test_source_invalid_batch_size_raises_config_error(size):
    with pytest.raises(ConfigError):
        list(MemorySource({"records": []}).read_batches(batch_size=size))


def test_source_batch_read_preserves_tail_and_order(records):
    source = MemorySource({"records": records + [{"id": 3}]})
    assert list(source.read_batches(batch_size=2)) == [records, [{"id": 3}]]


def test_source_empty_read_returns_no_batches():
    assert list(MemorySource({"records": []}).read_batches()) == []


@pytest.mark.parametrize("record", [[], 1, {1: "bad"}])
def test_memory_source_invalid_record_raises_record_error(record):
    with pytest.raises(RecordError):
        MemorySource({"records": [record]})


def test_transform_filters_and_maps_without_mutation(records):
    result = list(
        transform_records(
            records, lambda row: {"id": row["id"]} if row["id"] == 2 else None
        )
    )
    assert result == [{"id": 2}]
    assert records[1]["name"] == "Lin"


def test_transform_invalid_output_raises_record_error(records):
    with pytest.raises(RecordError):
        list(transform_records(records, lambda row: [row]))


def test_transform_mutating_callback_preserves_input(records):
    def change(row):
        row["name"] = "changed"
        return row

    assert list(transform_records(records, change))[0]["name"] == "changed"
    assert records[0]["name"] == "Ada"


class TrackingSource(Source):
    def __init__(self, catalog=None):
        self.catalog = (Stream("one"),) if catalog is None else catalog
        self.closed = False
        self.read_count = 0

    def streams(self):
        return self.catalog

    def _read_stream(self, stream):
        try:
            for number in range(10):
                self.read_count += 1
                yield {"id": number}
        finally:
            self.closed = True


@pytest.mark.parametrize("catalog", [(), ("bad",), (Stream("one"), Stream("one"))])
def test_source_invalid_catalog_raises_config_error(catalog):
    with pytest.raises(ConfigError):
        TrackingSource(catalog).check()


def test_source_multistream_requires_explicit_selection():
    source = TrackingSource((Stream("one"), Stream("two")))
    with pytest.raises(ConfigError):
        list(source.read())
    assert len(list(source.read("two"))) == 10


def test_source_early_close_releases_resources_without_eager_read():
    source = TrackingSource()
    records = source.read()
    assert source.read_count == 0
    assert next(records) == {"id": 0}
    assert source.read_count == 1
    records.close()
    assert source.closed


def test_source_batch_early_close_releases_underlying_stream():
    source = TrackingSource()
    batches = source.read_batches(batch_size=2)
    assert len(next(batches)) == 2
    assert source.read_count == 2
    batches.close()
    assert source.closed


def test_source_plain_iterator_is_supported():
    class PlainSource(TrackingSource):
        def _read_stream(self, stream):
            return iter([{"id": 1}])

    assert list(PlainSource().read()) == [{"id": 1}]


def test_transform_early_close_closes_source_iterator():
    source = TrackingSource()
    upstream = source.read()
    transformed = transform_records(upstream, lambda row: row)
    assert next(transformed) == {"id": 0}
    transformed.close()
    assert source.closed


def test_transform_callback_failure_closes_source_iterator():
    source = TrackingSource()
    upstream = source.read()

    def fail(row):
        raise ValueError("callback failed")

    with pytest.raises(ValueError):
        list(transform_records(upstream, fail))
    assert source.closed


def test_config_finite_json_float_is_preserved():
    assert Config.from_json('{"number": 1.25}')["number"] == 1.25
