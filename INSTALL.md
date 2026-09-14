# Installation and environment validation

## Requirements

- Python 3.10 or newer; Linux/macOS are the supported CI platforms.
- Python's `venv` and `pip` (some Linux distributions package venv separately).
- Package-index access for build/development tools, or a configured local wheelhouse.
- No database, Docker, external account, secret, or runtime dependency is needed.

## Fresh regular installation

From the repository root, choose a new venv path:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
python -m pip check
python -I -c "import pydatarheo; print(pydatarheo.__version__)"
python -m pydatarheo --version
```

Both version commands print `1.0.0a1`. Do not set `PYTHONPATH=src` to make an
uninstalled checkout importable: that would hide packaging failures.

## Editable development installation

```bash
python -m pip install -e '.[dev]'
pytest
pytest -m "not integration"
pytest -m "e2e"
pytest --cov=pydatarheo --cov-report=term-missing --cov-report=xml
```

`dev` includes pytest, coverage, Ruff, mypy, build, Hatchling, and Twine. It is not
installed by default. Coverage enforcement applies when coverage is requested;
plain marker-filtered tests do not require the full-suite coverage threshold.

## Automated clean-install verification

```bash
python scripts/verify_install.py
```

This creates two temporary, non-system venvs, runs regular and editable pip installs
independently, checks dependency consistency, imports with `-I` from outside the
checkout, and runs basic and file-pipeline examples. It removes only its own
temporary environments. Each successful mode prints:

```text
editable: install, import, and pipeline passed
regular: install, import, and pipeline passed
```

Pip build isolation fetches the pinned backend and its dependencies. This script
needs index access; alternatively configure `PIP_NO_INDEX=1` and
`PIP_FIND_LINKS=/absolute/path/to/wheelhouse` with all build requirements present.
The default pytest e2e test uses already installed dev build tools and installs
the built wheel with `--no-index --no-deps`, requiring no public network service.

## Build and install artifacts

```bash
python -m build
python -m twine check dist/*
python -m pip install --force-reinstall dist/pydatarheo-1.0.0a1-py3-none-any.whl
python -I -c "import pydatarheo; print(pydatarheo.__version__)"
```

The build includes a source distribution and a wheel built from that distribution.
No Git tags or VCS metadata are required to build a source archive. For a base
runtime installation from a prebuilt wheel, `pip install --no-index <wheel>` works
offline because there are no runtime dependencies.

## Reinstalling and migration

Prefer a new venv when moving from an earlier release, so retired dependencies
cannot conceal missing imports. Otherwise use `python -m pip install --force-reinstall .`.
Use `import pydatarheo`, not the retired `datarheo` package. Existing connector
configuration and APIs are not compatible; see README.md and ARCHITECTURE.md.
If imports fail, check `python -m pip --version` points at the active venv and
that Python meets the supported minimum. Pip installation errors fetching build
tools should be resolved through your index/proxy configuration, not by disabling
TLS verification. File sink errors on rerun generally mean the output exists:
choose a fresh path rather than deleting data automatically.
