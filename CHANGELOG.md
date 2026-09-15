# Changelog

## Unreleased

## 1.0.0.dev1 — Native framework + retained connector runtime

### Added

- Native `pydatarheo` package: memory, JSONL, and CSV sources; JSONL, CSV, and
  memory sinks; isolated connector registries; streaming/batching;
  transformations; bounded retries; atomic file publication.
- Lazy `pydatarheo.compat` bridge delegating `source-*`/`destination-*` names to
  the retained `datarheo` runtime; raises `ConnectorDependencyError` with
  install guidance when connector extras are absent.
- `connectors` and `test-connectors` extras for the retained runtime and its
  test suite; retained tests run under `pytest --run-compatibility`, with
  `--run-live` required for credential-gated tests.
- Layered, secret-free native tests, clean-install checks, runnable examples,
  CI, and an explicitly gated trusted-publishing workflow.

### Fixed

- Docker image resolution uses connector publisher metadata.
- Registry manifest/component downloads use bounded timeouts and honor explicit
  manifest URLs.
- File logger handlers are closed on reconfiguration (no descriptor leaks).
- Connector stdin pump tolerates broken pipes during shutdown.
- SQL connection teardown tolerates already-closed connections when lazy
  dataset generators are garbage-collected.
- Pydantic v2 validator schema construction no longer uses deprecated fields.
- Connector install/test caches and logs are isolated per test; both `uv` and
  `pip` install paths are exercised.

### Notes

Python 3.10+. The native layer has no third-party runtime dependencies; the
retained runtime's dependencies live behind extras. Docker-backed tests skip
when no Docker daemon is reachable. Required legal attribution remains in
LICENSE and NOTICE.
