"""Failure cases for file and memory connectors."""

import pytest

from pydatarheo import (
    Config,
    ConfigError,
    CsvSource,
    JsonlSource,
    MemorySource,
    RecordError,
    SourceError,
)


@pytest.mark.parametrize("factory", [JsonlSource, CsvSource])
@pytest.mark.parametrize(
    "config", [{}, {"path": 1}, {"path": ""}, {"path": "a", "typo": 1}]
)
def test_file_source_invalid_config_raises_config_error(factory, config):
    with pytest.raises(ConfigError):
        factory(config)


@pytest.mark.parametrize("config", [{}, {"records": ()}, {"records": [], "typo": 1}])
def test_memory_source_invalid_config_raises_config_error(config):
    with pytest.raises(ConfigError):
        MemorySource(config)


@pytest.mark.parametrize("factory", [JsonlSource, CsvSource])
def test_file_source_missing_file_raises_source_error(factory, tmp_path):
    source = factory({"path": str(tmp_path / "missing")})
    with pytest.raises(SourceError):
        source.check()
    with pytest.raises(SourceError):
        list(source.read())


@pytest.mark.parametrize("factory", [JsonlSource, CsvSource])
def test_file_source_invalid_encoding_raises_source_error(factory, tmp_path):
    path = tmp_path / "invalid"
    path.write_bytes(b"\xff\xfe")
    with pytest.raises(SourceError):
        list(factory({"path": str(path)}).read())


@pytest.mark.parametrize(
    "line", ['{"secret":', "[]", "null", '{"x": NaN}', '{"x": 1e999}']
)
def test_jsonl_source_invalid_record_reports_line_without_data(line, tmp_path):
    path = tmp_path / "invalid.jsonl"
    path.write_text("{}\n" + line + "\n", encoding="utf-8")
    source = JsonlSource({"path": str(path)})
    with pytest.raises(RecordError, match="line 2") as error:
        list(source.read())
    assert "secret" not in str(error.value)


def test_jsonl_source_blank_lines_are_skipped(tmp_path):
    path = tmp_path / "blank.jsonl"
    path.write_text('\n {}\n\t\n{"name": "Renée"}\n', encoding="utf-8")
    assert list(JsonlSource({"path": str(path)}).read()) == [{}, {"name": "Renée"}]


@pytest.mark.parametrize(
    "text", ["", "\n", "a,a\n", "a,\n", "a,b\n1\n", "a\n1,2\n", 'a\n"open']
)
def test_csv_source_malformed_file_raises_record_error(text, tmp_path):
    path = tmp_path / "invalid.csv"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(RecordError):
        list(CsvSource({"path": str(path)}).read())


def test_csv_source_quoted_cells_and_blanks_preserve_strings(tmp_path):
    path = tmp_path / "quoted.csv"
    path.write_text('id,text,empty\n\n001,"a,b\nc",\n', encoding="utf-8")
    source = CsvSource({"path": str(path), "stream": "items"})
    assert list(source.read("items")) == [{"id": "001", "text": "a,b\nc", "empty": ""}]


def test_config_required_missing_field_does_not_expose_values():
    config = Config({"password": "private"})
    with pytest.raises(ConfigError) as error:
        config.require("path", str)
    assert "private" not in str(error.value)
