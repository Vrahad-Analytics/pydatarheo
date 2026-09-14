"""CLI success, input validation, and safe error output."""

import pytest

from pydatarheo import __version__
from pydatarheo.cli import main


def test_cli_version_prints_distribution_version(capsys):
    with pytest.raises(SystemExit) as error:
        main(["--version"])
    assert error.value.code == 0
    assert capsys.readouterr().out.strip() == __version__


def test_cli_jsonl_workflow_writes_records(jsonl_path, tmp_path, capsys):
    assert (
        main(
            [
                "read",
                "--source",
                "jsonl",
                "--input",
                str(jsonl_path),
                "--output",
                str(tmp_path / "out.jsonl"),
            ]
        )
        == 0
    )
    assert capsys.readouterr().out == "Wrote 2 records\n"


def test_cli_missing_input_returns_nonzero(tmp_path, capsys):
    with pytest.raises(SystemExit) as error:
        main(
            [
                "read",
                "--source",
                "csv",
                "--input",
                str(tmp_path / "missing"),
                "--output",
                str(tmp_path / "output"),
            ]
        )
    assert error.value.code == 1
    assert "Source file cannot be opened" in capsys.readouterr().err


def test_cli_no_command_returns_usage_error():
    with pytest.raises(SystemExit) as error:
        main([])
    assert error.value.code == 2
