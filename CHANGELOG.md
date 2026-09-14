# Changelog

## Unreleased

### Added

- Placeholder for changes after the native alpha release.

## 1.0.0a1 — Native framework preview

### Breaking

- Use `import pydatarheo`; the previous `datarheo` API is retired.
- Replace external protocol execution, remote catalogs, hosted integrations,
  SQL caches, and MCP tools with explicit native Python source contracts.
- Retire legacy environment namespaces and automatic connector installation.
- Support Python 3.10+ with no third-party runtime dependencies.

### Added

- Native memory, JSONL, and CSV sources; JSONL, CSV, and memory sinks.
- Isolated connector registries, defensive config snapshots, streaming/batching,
  transformations, and opt-in bounded retries for idempotent operations.
- Atomic file publication with overwrite protection.
- Layered, secret-free tests, clean-install checks, runnable examples, and CI.
- Explicitly gated trusted-publishing workflow for TestPyPI/PyPI.

### Notes

This version is a breaking alpha, not a feature-parity replacement for earlier
releases. No publication date is assigned until a release is approved. Required
legal attribution remains in LICENSE and NOTICE.
