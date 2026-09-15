"""Build an sdist and wheel, then exercise the wheel outside the source tree."""

import json
import os
import re
import subprocess
import sys
import venv
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
pytestmark = pytest.mark.e2e


def run(command, cwd):
    result = subprocess.run(
        command, cwd=cwd, text=True, capture_output=True, timeout=180
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result


@pytest.fixture(scope="module")
def installed_environment(tmp_path_factory):
    directory = tmp_path_factory.mktemp("installed")
    artifacts = directory / "dist"
    run(
        [
            sys.executable,
            "-m",
            "build",
            "--no-isolation",
            "--outdir",
            str(artifacts),
            str(ROOT),
        ],
        directory,
    )
    wheels = list(artifacts.glob("*.whl"))
    assert len(wheels) == 1
    assert len(list(artifacts.glob("*.tar.gz"))) == 1
    environment = directory / "venv"
    venv.EnvBuilder(with_pip=True, symlinks=os.name != "nt").create(environment)
    python = str(
        environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    )
    run(
        [
            python,
            "-I",
            "-m",
            "pip",
            "install",
            "--no-index",
            "--no-deps",
            str(wheels[0]),
        ],
        directory,
    )
    run([python, "-I", "-m", "pip", "check"], directory)
    return python, directory


def test_wheel_import_version_and_metadata_are_self_contained(installed_environment):
    python, directory = installed_environment
    result = run(
        [
            python,
            "-I",
            "-c",
            (
                "import json, pydatarheo; from importlib.metadata import distribution; "
                "d = distribution('pydatarheo'); "
                "assert pydatarheo.__version__ == d.version; "
                "assert not [r for r in d.requires or [] if 'extra ==' not in r]; "
                "assert any(str(f).endswith('pydatarheo/py.typed') for f in d.files); "
                "assert any(str(f).endswith('/licenses/LICENSE') for f in d.files); "
                "assert any(str(f).endswith('/licenses/NOTICE') for f in d.files); "
                "print(json.dumps({'version': d.version, 'path': pydatarheo.__file__}))"
            ),
        ],
        directory,
    )
    metadata = json.loads(result.stdout)
    assert metadata["version"]
    assert Path(metadata["path"]).is_relative_to(directory)


@pytest.mark.parametrize(
    "example,expected",
    [
        ("basic.py", "{'id': 1, 'name': 'Ada'}"),
        ("custom_connector.py", "[{'number': 4}]"),
        ("retries_and_logging.py", "Fetched 1 record after 3 attempts"),
    ],
)
def test_installed_example_completes_with_documented_output(
    installed_environment, tmp_path, example, expected
):
    python, _ = installed_environment
    result = run([python, "-I", str(ROOT / "examples" / example)], tmp_path)
    assert expected in result.stdout


def test_installed_pipeline_reads_transforms_and_writes_sales(
    installed_environment, tmp_path
):
    python, _ = installed_environment
    output = tmp_path / "sales.jsonl"
    result = run(
        [python, "-I", str(ROOT / "examples/pipeline.py"), "--output", str(output)],
        tmp_path,
    )
    assert result.stdout.strip() == "Wrote 3 sales records"
    rows = [
        json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()
    ]
    assert rows == [
        {"id": 1, "customer": "Ada", "total_cents": 2500},
        {"id": 2, "customer": "Lin", "total_cents": 999},
        {"id": 3, "customer": "Renée", "total_cents": 1500},
    ]


def test_installed_console_scripts_run_without_source_imports(
    installed_environment, tmp_path
):
    python, _ = installed_environment
    for name in ("pydatarheo", "pydr"):
        executable = Path(python).parent / (name + (".exe" if os.name == "nt" else ""))
        assert run([str(executable), "--version"], tmp_path).stdout.strip()
    output = tmp_path / "cli.jsonl"
    result = run(
        [
            python,
            "-I",
            "-m",
            "pydatarheo",
            "read",
            "--source",
            "csv",
            "--input",
            str(ROOT / "examples/data/sales.csv"),
            "--output",
            str(output),
        ],
        tmp_path,
    )
    assert result.stdout.strip() == "Wrote 3 records"
    assert len(output.read_text(encoding="utf-8").splitlines()) == 3


@pytest.mark.parametrize(
    "index,expected", [(0, "{'id': 2, 'name': 'Lin'}"), (1, "Wrote 3 records")]
)
def test_readme_quickstarts_run_against_installed_wheel(
    installed_environment, tmp_path, index, expected
):
    python, _ = installed_environment
    snippets = re.findall(
        r"```python\n(.*?)```", (ROOT / "README.md").read_text(encoding="utf-8"), re.S
    )
    sample = tmp_path / "examples/data/sales.csv"
    sample.parent.mkdir(parents=True)
    sample.write_bytes((ROOT / "examples/data/sales.csv").read_bytes())
    result = run([python, "-I", "-c", snippets[index]], tmp_path)
    assert expected in result.stdout
