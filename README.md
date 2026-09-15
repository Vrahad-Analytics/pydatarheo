# pydatarheo

**Vrahad Analytics' native Python connector framework for local, streaming data pipelines.**

[![CI](https://github.com/Vrahad-Analytics/pydatarheo/actions/workflows/ci.yml/badge.svg)](https://github.com/Vrahad-Analytics/pydatarheo/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/tests-pytest-blue)](#testing)
[![Coverage](https://img.shields.io/badge/coverage-gate%20%E2%89%A590%25-blue)](#testing)

Configure a source, iterate over ordinary Python dictionaries, transform records,
and write a local JSONL/CSV file or an in-memory result. No service, database,
container, connector download, telemetry, or third-party runtime dependency is
required. Both the distribution and import package are named `pydatarheo`.

**Release status:** `1.0.0.dev1` is a development release. The dependency-free
native API ships three source types: `memory`, `jsonl`, and `csv`. The retained
`datarheo` connector runtime — external protocol connectors, SQL caches,
cloud/agent integrations, and MCP tools — is available by installing the
`connectors` extra. See [Retained connector runtime](#retained-connector-runtime)
and [Compatibility and limits](#compatibility-and-limits).

## Installation

Python **3.10+**, Linux or macOS. From a clone of this repository:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
python -c "import pydatarheo; print(pydatarheo.__version__)"
```

Expected version: `1.0.0.dev1`. For development, use
`python -m pip install -e '.[dev]'` instead. Local installation is the verified
path; publication of this version to a package index is a separate release step.
See [INSTALL.md](INSTALL.md) for clean-install verification and troubleshooting.

To include the retained connector runtime and its third-party dependencies:

```bash
python -m pip install -e '.[connectors]'
# or, for the full retained test suite:
python -m pip install -e '.[dev,connectors,test-connectors]'
```

## Quickstart

```python
import pydatarheo as dr

source = dr.get_source(
    "memory",
    config={"records": [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Lin"}]},
)
source.check()
for record in source.read():
    print(record)
```

Output:

```text
{'id': 1, 'name': 'Ada'}
{'id': 2, 'name': 'Lin'}
```

For local files:

```python
from pydatarheo import JsonlSink, get_source, transform_records

source = get_source("csv", config={"path": "examples/data/sales.csv"})
source.check()
records = transform_records(source.read(), lambda row: {
    "id": int(row["id"]),
    "total_cents": int(row["quantity"]) * int(row["unit_cents"]),
})
count = JsonlSink("sales-output.jsonl").write(records)
print(f"Wrote {count} records")
```

Output: `Wrote 3 records`. Run from the repository root with a new output path.
File sinks refuse existing paths unless the Python caller explicitly passes
`overwrite=True`. Failures do not publish partial files. Output parent directories
must already exist.

## Sources, streams, and sinks

| Component | Configuration / behavior |
| --- | --- |
| `get_source("memory", config=...)` | Required `records`: list of string-keyed mappings; snapshots all input in memory |
| `get_source("jsonl", config=...)` | Required `path`: local UTF-8 file; one JSON object per non-blank line |
| `get_source("csv", config=...)` | Required `path`: local UTF-8 CSV with unique, non-empty column names; values stay strings |
| All built-in sources | Optional `stream`: non-empty name, default `records`; unknown config keys are errors |
| `JsonlSink(path)` | Strict JSONL output; rejects non-serializable values and non-finite numbers |
| `CsvSink(path, columns=[...])` | Explicit columns; rejects missing/extra keys and nested values; `None` becomes an empty cell |
| `MemorySink()` | Collects a detached snapshot; `.records` returns a copy |

`source.streams()` lists `Stream` objects. `source.read("records")` selects a
case-sensitive stream; multi-stream custom sources require an explicit selection.
`source.check()` checks catalog validity and, for files, accessibility. It does
not scan the dataset: malformed data raises during iteration.

### Streaming versus batching

```python
for batch in source.read_batches(batch_size=1000):
    print(len(batch))
```

File sources are pull-based and hold approximately one record at a time;
batching holds at most `batch_size` records plus parser buffers. Individual
records are not size-limited. Memory sources and sinks hold the whole dataset.
Each new file read starts from the beginning; there is no cursor/checkpoint store.

When stopping early, close the iterator explicitly:

```python
from contextlib import closing

with closing(source.read()) as records:
    first = next(records, None)
```

`transform_records(records, callback)` lazily maps copied records; returning
`None` drops a record. The callback's own exceptions propagate. Closing the
transformation closes its upstream iterator; sinks close consumed iterators on
success or failure. Use explicit conversions when mapping CSV data, rather than
relying on inferred types.

### Errors, retries, and logging

Catch `DatarheoError` at application boundaries. More specific types are
`ConfigError`, `SourceError`, `RecordError`, `SinkError`, and `TransientError`.
Library diagnostics do not include record bodies or configuration values.
The library does not configure logging; applications may enable the
`pydatarheo` logger through the standard `logging` module.

`retry(operation, policy=RetryPolicy(...))` retries **only** `TransientError`,
with bounded attempts and capped exponential backoff. Use it for an idempotent
operation, such as fetching one complete page before emitting its records.
Never retry a partially consumed stream or a non-idempotent write automatically.
See [the retries example](examples/retries_and_logging.py).

## End-to-end examples

All examples run offline after installation:

```bash
python examples/basic.py
python examples/custom_connector.py
python examples/retries_and_logging.py
python examples/pipeline.py --output /tmp/pydatarheo-sales.jsonl
pydatarheo read --source csv --input examples/data/sales.csv --output /tmp/pydatarheo-cli.jsonl
```

Choose unused output paths when rerunning. The pipeline prints
`Wrote 3 sales records`; the CLI prints `Wrote 3 records`.
See [examples/README.md](examples/README.md) for every example's expected output.
`pydr` is a CLI alias, and `python -m pydatarheo` exposes the same interface.

## Custom connectors

Subclass `Source`, implement `streams()` and `_read_stream(stream)`, and validate
configuration in the constructor. Register your factory on an application-owned
`SourceRegistry`; no global registration or automatic plugin execution occurs.

```python
from pydatarheo import SourceRegistry

registry = SourceRegistry()
registry.register("my-source", MySource)
source = registry.create("my-source", {"path": "input.jsonl"})
```

`MySource` above is your implementation, not a built-in class. A complete,
runnable implementation is in [examples/custom_connector.py](examples/custom_connector.py).
See [ARCHITECTURE.md](ARCHITECTURE.md) and [CONTRIBUTING.md](CONTRIBUTING.md)
for contracts, resource lifetime, testing, and extension guidance.

## Retained connector runtime

Installing `pydatarheo[connectors]` restores the `datarheo` import package:
connector registry, Python/Docker connector executors, DuckDB/Postgres/BigQuery/
Snowflake caches, hosted cloud and agent APIs, and the `datarheo-mcp` server.
Those integrations use external protocol packages (`airbyte-cdk`,
`airbyte-api`, `airbyte-protocol-models-pdv2`) and the public connector registry;
`import pydatarheo` alone never installs or runs them.

`pydatarheo.get_source("source-...", ...)` and `get_destination(...)` delegate to
the retained runtime lazily. Without the extra they raise
`ConnectorDependencyError` with install guidance instead of failing at import.
Native names (`memory`, `jsonl`, `csv`, and anything registered on a
`SourceRegistry`) always resolve natively first.

## Testing

```bash
python -m pip install -e '.[dev]'
pytest
pytest -m "not integration"
pytest -m "e2e"
pytest --cov=pydatarheo --cov-report=term-missing --cov-report=xml
ruff check src tests examples scripts
ruff format --check src tests examples scripts
mypy --strict --python-version 3.10 src/pydatarheo
python scripts/verify_install.py
```

The retained suite is gated and requires the connector extras:

```bash
python -m pip install -e '.[dev,connectors,test-connectors]'
pytest --run-compatibility
pytest --run-compatibility --run-live   # only with provisioned credentials/services
```

Docker-backed connector tests skip automatically when no Docker daemon is
reachable; credential-gated tests require `--run-live` plus the documented
environment secrets.

Unit tests cover contracts and failure cases. Integration tests use real local
files. E2E tests build an sdist and wheel, install the wheel without dependencies
or index access into a fresh venv, then run the examples and CLI outside the
source tree. No tests require secrets or public APIs. The separate verification
script checks standard editable and regular pip installs with build isolation;
it needs a package index or configured wheelhouse for build requirements.

CI runs Linux Python 3.10–3.14 and macOS Python 3.12, enforces a 90% branch-aware
coverage gate, and uploads test/coverage reports. The coverage badge describes
the configured gate, not a live measured result. Index publishing is manual,
requires passing CI on a matching version tag, and uses protected environments
and trusted publishing; it is never triggered by a normal push.

## Compatibility and limits

The native `pydatarheo` API is new code: memory/JSONL/CSV sources, local sinks,
and an explicit `SourceRegistry`. The `datarheo` package retains the earlier
connector runtime, caches, cloud/agent APIs, and MCP tools behind the
`connectors` extra; its public API is unchanged and its tests run under
`pytest --run-compatibility`.

The native API does not implement warehouse/HTTP connectors, async reads,
schema evolution, incremental state, orchestration, or exactly-once delivery.
The retained runtime carries those capabilities and their third-party
dependencies. Third-party packages and connectors retain their own licenses and
ownership; retained code derives from an upstream project (see `NOTICE`).

## License

Maintained by **Vrahad Analytics LLP** under the MIT license. See
[LICENSE](LICENSE) and [NOTICE](NOTICE) for required legal attribution.
See [CHANGELOG.md](CHANGELOG.md) for release notes.
