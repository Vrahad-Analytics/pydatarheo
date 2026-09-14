"""Verify editable and regular pip installs in separate fresh virtual environments."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True, timeout=300)


def main() -> None:
    # Only this script's temporary directory is cleaned up; existing environments are untouched.
    with tempfile.TemporaryDirectory(prefix="pydatarheo-install-") as directory:
        temporary = Path(directory)
        for mode in ("editable", "regular"):
            environment = temporary / mode
            venv.EnvBuilder(with_pip=True, symlinks=os.name != "nt").create(environment)
            python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
            install = [str(python), "-I", "-m", "pip", "install"]
            if mode == "editable":
                install.append("-e")
            run([*install, str(ROOT)], temporary)
            run([str(python), "-I", "-m", "pip", "check"], temporary)
            run(
                [str(python), "-I", "-c", "import pydatarheo; print(pydatarheo.__version__)"],
                temporary,
            )
            run([str(python), "-I", str(ROOT / "examples/basic.py")], temporary)
            run(
                [
                    str(python),
                    "-I",
                    str(ROOT / "examples/pipeline.py"),
                    "--output",
                    str(temporary / f"{mode}.jsonl"),
                ],
                temporary,
            )
            print(f"{mode}: install, import, and pipeline passed", flush=True)
    print(f"Verified with Python {sys.version.split()[0]}")


if __name__ == "__main__":
    main()
