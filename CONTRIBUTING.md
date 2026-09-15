# Contributing to pydatarheo

Vrahad Analytics maintains this native connector framework. Contributions must
respect LICENSE/NOTICE and must not claim ownership of third-party work.

## Local setup

Use Python 3.10+ and a fresh virtual environment from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

## Connector contributions

Read ARCHITECTURE.md, then follow examples/custom_connector.py:

- Implement `Source.streams()` and `Source._read_stream(stream)`.
- Validate explicit configuration in the constructor with `Config` and reject
  unknown fields. Keep credentials out of repr, logs, and error messages.
- Yield string-keyed mappings with stable stream names. Avoid hidden global state.
- Own resources within generator context managers and test early closure.
- Keep connectivity checks bounded and side-effect-free. Network connectors need
  timeouts and explicit pagination; retries must not duplicate emitted records.
- Prefer application-owned `SourceRegistry` registration. Propose new built-ins
  deliberately; never auto-download or execute untrusted plugins.
- Keep connector-specific dependencies optional and out of the base runtime.
- Include a runnable example with sanitized expected output and document limits.

## Tests and style

Place isolated contracts/failure tests in `tests/unit/`, real local or mock-service
round trips in `tests/integration/`, and complete installed workflows in
`tests/e2e/`. Use `test_<component>_<scenario>_<expected>` names and shared fixtures
in `tests/conftest.py`. Fixtures must not remove existing containers, files, or
databases. Use `tmp_path`, deterministic data, and monkeypatch for external edges.
Default tests must need no secrets. Any future live-service tests must explicitly
opt in through environment variables and skip when credentials are absent.

Use typed public APIs, standard-library abstractions, Markdown docstrings, and
Ruff formatting. Run before submitting:

```bash
ruff check src tests examples scripts
ruff format --check src tests examples scripts
mypy --strict --python-version 3.10 src/pydatarheo
pytest --cov=pydatarheo --cov-report=term-missing --cov-report=xml
pytest -m "not integration"
pytest -m "e2e"
python scripts/verify_install.py
python -m build
python -m twine check dist/*
```

The coverage gate is 90%, including branch coverage. Unit tests should test
behavior, not implementation details; integration/e2e tests must exercise actual
installed code. Keep tests order-independent and do not silence warnings to hide
resource leaks. Update README/API examples with contract changes.

## Pull requests

Explain intent, compatibility impact, verification results, and limitations.
Do not commit virtualenvs, generated distributions, coverage output, data caches,
or secrets. Keep public branding consistent with `pydatarheo` / Vrahad Analytics.
Legal attribution is intentionally exempt from branding cleanup.

## Release process

1. Update the static version in `pyproject.toml` and CHANGELOG.md; run all checks.
2. Merge a reviewed PR. Tag that tested commit with `v<version>`; prereleases use
   a PEP 440 version such as `v1.0.0a1`.
3. Wait for the CI workflow on that exact tag/SHA to succeed.
4. Configure GitHub environments `testpypi` and `pypi` with required reviewers,
   and configure the corresponding index's trusted publisher for this repository,
   `publish.yml`, and environment. Confirm Vrahad controls the distribution name.
5. Manually dispatch `Publish package` on the version tag, selecting `testpypi`
   first. Inspect the installed package before approving a production dispatch.

The publish workflow checks the tag/version and successful CI for its exact SHA,
rebuilds artifacts, checks metadata, and verifies a wheel in a fresh environment.
Publishing uses OIDC and environment protections; no API token belongs in the
repository. It is never automatically performed by normal pushes or PRs. GitHub
and package-index configuration must be completed by repository administrators.
