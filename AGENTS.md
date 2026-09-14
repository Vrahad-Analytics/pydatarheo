# Repository guidance

## Native release scope

This is Vrahad Analytics' independent `pydatarheo` connector framework. Both the
Python import and distribution are named `pydatarheo`; implementation lives in
`src/pydatarheo`. The previous `datarheo` import, protocol executors, hosted
integrations, SQL caches, and MCP server are retired, not compatibility adapters.
Do not reintroduce implicit connector downloads, remote registries, telemetry,
or secret discovery. Preserve required provenance in LICENSE and NOTICE.

## Development and verification

Use Python 3.10+ on Linux/macOS. From a fresh venv:

```bash
python -m pip install -e '.[dev]'
ruff check src tests examples scripts
ruff format --check src tests examples scripts
mypy --strict --python-version 3.10 src/pydatarheo
pytest --cov=pydatarheo --cov-report=term-missing --cov-report=xml
python scripts/verify_install.py
python -m build
python -m twine check dist/*
```

Default tests are secret-free and do not use public network services. The e2e
packaging test needs the build backend from the dev extra, builds locally, and
installs a wheel into an isolated venv without accessing a package index. The
separate install verification script uses pip build isolation and needs access
to a package index (or a preconfigured local wheelhouse). Use symlink-based
virtualenvs on POSIX: copying standalone interpreter executables can prevent them
from locating their standard library when testing nested virtualenvs.

Keep connectors independent and validate configuration without including values
in diagnostics. File outputs must not clobber existing files by default. Use
function-scoped fixtures and temporary paths; never touch existing databases,
containers, or developer data during tests. Update tests and usage docs alongside
public contracts. Pyproject.toml is the single version source.
