"""Actual filesystem round trips, requiring no service or secret."""

import pytest

from pydatarheo import (
    CsvSink,
    CsvSource,
    JsonlSink,
    JsonlSource,
    MemorySink,
    get_source,
    transform_records,
)

pytestmark = pytest.mark.integration


def test_jsonl_pipeline_transform_and_sink_round_trip(jsonl_path, tmp_path):
    source = get_source("jsonl", config={"path": str(jsonl_path)})
    source.check()
    output = tmp_path / "transformed.jsonl"
    records = transform_records(
        source.read(), lambda row: {"id": row["id"], "double": row["amount"] * 2}
    )
    assert JsonlSink(output).write(records) == 2
    assert list(JsonlSource({"path": str(output)}).read()) == [
        {"id": 1, "double": 20},
        {"id": 2, "double": 40},
    ]


def test_csv_pipeline_batches_and_csv_sink_round_trip(csv_path, tmp_path):
    source = CsvSource({"path": str(csv_path)})
    source.check()
    assert [len(batch) for batch in source.read_batches(batch_size=1)] == [1, 1]
    output = tmp_path / "copy.csv"
    assert CsvSink(output, columns=["id", "name", "amount"]).write(source.read()) == 2
    assert list(CsvSource({"path": str(output)}).read()) == list(source.read())


def test_csv_sink_null_and_quoted_cells_round_trip(tmp_path):
    output = tmp_path / "quoted.csv"
    rows = [{"id": 1, "text": 'a,"b"\nc', "empty": None}]
    CsvSink(output, columns=["id", "text", "empty"]).write(rows)
    assert list(CsvSource({"path": str(output)}).read()) == [
        {"id": "1", "text": 'a,"b"\nc', "empty": ""},
    ]


def test_file_to_memory_pipeline_detaches_records(jsonl_path, records):
    sink = MemorySink()
    assert sink.write(JsonlSource({"path": str(jsonl_path)}).read()) == 2
    assert sink.records == records
