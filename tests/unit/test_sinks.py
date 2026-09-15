"""Atomicity, overwrite protection, and output validation."""

import json

import pytest

from pydatarheo import (
    ConfigError,
    CsvSink,
    JsonlSink,
    MemorySink,
    RecordError,
    SinkError,
)


@pytest.mark.parametrize(
    "factory", [JsonlSink, lambda path, **kw: CsvSink(path, columns=["id"], **kw)]
)
def test_file_sink_existing_output_is_preserved(factory, tmp_path):
    path = tmp_path / "output"
    path.write_text("original", encoding="utf-8")
    with pytest.raises(SinkError):
        factory(path).write([{"id": 1}])
    assert path.read_text(encoding="utf-8") == "original"
    assert list(tmp_path.iterdir()) == [path]


def test_jsonl_sink_explicit_overwrite_replaces_output(tmp_path):
    path = tmp_path / "output.jsonl"
    path.write_text("original", encoding="utf-8")
    assert JsonlSink(path, overwrite=True).write([{"id": 2}]) == 1
    assert json.loads(path.read_text(encoding="utf-8")) == {"id": 2}


@pytest.mark.parametrize(
    "row", [{"bad": object()}, {"bad": float("nan")}, {"bad": float("inf")}, []]
)
def test_jsonl_sink_invalid_record_leaves_no_partial_file(row, tmp_path):
    path = tmp_path / "output.jsonl"
    with pytest.raises(RecordError):
        JsonlSink(path).write([{"id": 1}, row])
    assert list(tmp_path.iterdir()) == []


def test_file_sink_source_failure_preserves_existing_output(tmp_path):
    path = tmp_path / "output.jsonl"
    path.write_text("original", encoding="utf-8")

    def failing_records():
        yield {"id": 1}
        raise RuntimeError("source failed")

    with pytest.raises(RuntimeError):
        JsonlSink(path, overwrite=True).write(failing_records())
    assert path.read_text(encoding="utf-8") == "original"
    assert list(tmp_path.iterdir()) == [path]


def test_file_sink_missing_parent_raises_sink_error(tmp_path):
    with pytest.raises(SinkError):
        JsonlSink(tmp_path / "missing" / "out").write([])


def test_file_sink_racing_output_is_not_clobbered(tmp_path):
    path = tmp_path / "output"

    def records():
        yield {"id": 1}
        path.write_text("other writer", encoding="utf-8")

    with pytest.raises(SinkError):
        JsonlSink(path).write(records())
    assert path.read_text(encoding="utf-8") == "other writer"
    assert list(tmp_path.iterdir()) == [path]


@pytest.mark.parametrize("columns", [[], "id", [""], [1], ["id", "id"]])
def test_csv_sink_invalid_schema_raises_config_error(columns, tmp_path):
    with pytest.raises(ConfigError):
        CsvSink(tmp_path / "out.csv", columns=columns)


@pytest.mark.parametrize("row", [{}, {"id": 1, "extra": 2}, {"id": []}])
def test_csv_sink_invalid_record_leaves_no_output(row, tmp_path):
    with pytest.raises(RecordError):
        CsvSink(tmp_path / "out.csv", columns=["id"]).write([row])
    assert list(tmp_path.iterdir()) == []


def test_jsonl_sink_empty_input_writes_empty_file(tmp_path):
    path = tmp_path / "empty.jsonl"
    assert JsonlSink(path).write([]) == 0
    assert path.read_bytes() == b""


def test_memory_sink_snapshots_and_failed_write_preserves_previous(records):
    sink = MemorySink()
    assert sink.write(records) == 2
    records[0]["name"] = "changed"
    returned = sink.records
    returned[0]["name"] = "changed again"
    with pytest.raises(RecordError):
        sink.write([{"id": 3}, []])
    assert sink.records[0]["name"] == "Ada"


@pytest.mark.parametrize("kind", ["jsonl", "csv", "memory"])
def test_sink_invalid_record_closes_upstream_generator(kind, tmp_path):
    closed = []

    def rows():
        try:
            yield []
        finally:
            closed.append(True)

    upstream = rows()
    sink = {
        "jsonl": JsonlSink(tmp_path / "out.jsonl"),
        "csv": CsvSink(tmp_path / "out.csv", columns=["id"]),
        "memory": MemorySink(),
    }[kind]
    with pytest.raises(RecordError):
        sink.write(upstream)
    assert closed == [True]


@pytest.mark.parametrize("kind", ["jsonl", "csv"])
def test_file_sink_invalid_unicode_raises_record_error_without_partial_output(
    kind, tmp_path
):
    sink = (
        JsonlSink(tmp_path / "out")
        if kind == "jsonl"
        else CsvSink(tmp_path / "out", columns=["id"])
    )
    with pytest.raises(RecordError):
        sink.write([{"id": "\ud800"}])
    assert list(tmp_path.iterdir()) == []
