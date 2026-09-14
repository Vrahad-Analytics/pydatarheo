# pydatarheo architecture

## Scope

pydatarheo is Vrahad Analytics' synchronous, in-process connector framework.
The native package has no runtime dependencies beyond Python's standard library.
It provides local connectors and extension contracts, not a hosted platform or
an external connector execution engine. Distribution and import names are both
`pydatarheo`; code lives under `src/pydatarheo` to prevent accidental imports
from an uninstalled checkout.

## Data flow

```text
explicit Config -> SourceRegistry / source constructor -> Source
                                                          |
                                                    Stream selection
                                                          |
                                                   read(): Iterator[Record]
                                                          |
                                              optional transform_records()
                                                          |
                                              JSONL / CSV / memory sink
```

## Core abstractions

- **Config** is a string-keyed mapping snapshot. Values are copied on entry and
  access. `from_json()` requires a JSON object; `require()` validates types and
  `only()` rejects unsupported options. Its repr hides all values. Configuration
  is explicit: there is no environment expansion, secret lookup, or evaluation.
- **Record** is a plain `dict[str, Any]`. The framework validates string keys and
  copies records at source, transformation, and sink boundaries. Source and
  transform implementations cannot mutate a consumer's record through aliasing.
  Nested values must be deepcopy-compatible; JSON sinks additionally require
  strict JSON-serializable values. The contract does not imply a schema engine.
- **Stream** is an immutable, non-empty, case-sensitive name. Each source exposes
  an ordered catalog of uniquely named streams. Multiple streams must be selected
  explicitly; records are not mixed or wrapped in control messages.
- **Source** is the abstract connector contract. Implement `streams()` and
  `_read_stream(stream)`. `read()` validates the catalog/selection and yields
  detached records. `read_batches()` groups the same iterator into bounded lists.
  `check()` validates the catalog; file connectors also check accessibility.
- **SourceRegistry** maps local names to explicit factories accepting configuration.
  Each instance is independent; duplicate registrations are errors. The helper
  `builtin_registry()` returns a fresh registry with `memory`, `jsonl`, and `csv`.
  `get_source()` is shorthand for constructing one of those built-in types.
- **Sinks** implement a simple structural contract: `write(iterable) -> int`.
  `JsonlSink` and `CsvSink` stream into a temporary sibling file, flush and fsync
  it, then publish it. The default hard-link publication refuses an existing
  destination, including one created by a racing writer. Explicit overwrite uses
  atomic replacement. Temporary output is cleaned up on failure. `MemorySink`
  replaces its snapshot only after successful collection. There is no mandatory
  sink base class; application sinks can implement the same method.
- **transform_records** invokes a callback on each detached record. A mapping is
  output; `None` filters the record. Application exceptions are not concealed.
- **RetryPolicy / retry** handle bounded retries of operations that raise
  `TransientError`. Delay doubles up to a configured cap. Callers guarantee
  idempotency. A whole stream is never implicitly replayed after partial emission.

## Built-in connectors

`MemorySource` snapshots a configured list and supports repeatable reads.
`JsonlSource` reads UTF-8 JSON objects one line at a time and skips blank lines.
`CsvSource` requires a unique, non-empty header and preserves cells as strings;
quoted commas/newlines work, blank rows are skipped, and column-count mismatches
are rejected. Both file connectors open the source on iteration, not import or
construction. Every new read starts at the beginning of the file.

Files are caller-selected local paths, not URLs. The framework does not restrict
paths to a sandbox: applications accepting untrusted configuration must enforce
their own path policy. Local file connectors should be used with trusted regular
files, not arbitrary device files or pipes. File size and record size limits are
application responsibilities.

## Resource lifetime and failure semantics

File handles are scoped inside connector generators. Exhausting or closing a
`Source.read()` iterator closes its underlying iterator when supported. Closing
a batch or transformation iterator closes its upstream iterator. Sinks close
consumed iterators on success or failure, before publishing output. Callers
stopping early should use `contextlib.closing`; a `break` alone does not guarantee
immediate cleanup on all Python implementations. Transformation callbacks and
custom connectors must follow the same explicit resource-lifetime discipline.

Streaming memory use scales with the current record, or batch size, rather than
file length. Memory sources/sinks necessarily scale with the full dataset.
Defensive copying costs CPU and an extra record-sized allocation in exchange for
clear ownership. No checkpoint, cursor persistence, implicit deduplication,
transaction spanning multiple sinks, or exactly-once guarantee is provided.

File sink atomicity is scoped to one local file. It requires a filesystem with
hard-link and atomic-replacement support. Output parents must exist. Failure
leaves an existing destination intact; `overwrite=True` is deliberate replacement,
not append. The temporary file is fsynced, but its parent directory is not: this
is not a guarantee of durability through a power loss. CSV serialization preserves
text rather than sanitizing spreadsheet formulas; sanitize untrusted values
before opening exports in spreadsheet software.

`DatarheoError` is the public framework boundary, with configuration, source,
record, sink, and transient subclasses. Errors include safe context such as line
numbers, not record bodies, credentials, or configuration values. User code may
raise its own exceptions. The standard `pydatarheo.retry` logger reports attempt
numbers only. Applications own logging configuration; the library has no network
logging endpoint or telemetry.

## Conceptual break from the previous runtime

The former architecture orchestrated separately installed connector executables,
serialized protocol catalogs/control messages, remote connector registries, SQL
caches, and hosted APIs. The native architecture directly calls trusted Python
factories and iterates records. Stream selection and configuration are local
contracts, not wrappers around an external SDK. There is no compatibility adapter
or runtime dependency on the former implementation.

This deliberately sacrifices prior connector breadth. The old `datarheo` import,
cloud/agent integrations, MCP server, warehouse caches, subprocess/container
executors, and implicit installation settings are not part of this release.
Existing applications require an explicit migration and replacement connectors.
Required repository provenance is maintained in LICENSE and NOTICE; naming alone
does not transfer ownership of third-party contributions.

## Extension checklist

1. Create a module under `src/pydatarheo/connectors/` or in your own installed
   package. Subclass `Source`; validate configuration without coercing surprising
   values or logging secrets.
2. Expose stable stream names, implement `_read_stream()`, and yield string-keyed
   mappings. Put connection/file cleanup inside `with` or `try/finally` blocks.
3. Override `check()` when a bounded connectivity check is meaningful. Avoid
   reading all data or mutating the source in a check.
4. For network connectors, set timeouts and implement pagination explicitly.
   Retry one idempotent page request before yielding that page. Do not convert
   authentication, configuration, or decoding failures into transient errors.
5. Register the factory on an application-owned `SourceRegistry`. Registration
   executes no code until construction, and no plugins are loaded implicitly.
6. Add unit tests for invalid config, stream selection, decoding, and cleanup;
   local/mock integration tests; and a secret-free runnable example. External
   credential tests must be optional and skipped unless explicitly configured.

See `examples/custom_connector.py` for a complete implementation and
CONTRIBUTING.md for verification commands. New optional dependencies should be
isolated to connector extras so the base installation stays lightweight.

## Packaging and verification

Hatchling builds wheels from `src/pydatarheo`; `pyproject.toml` is the single
version source. `__version__` comes from installed distribution metadata. Wheels
include `py.typed` and legal notices; sdists include tests, examples, and usage docs.
The test suite builds a wheel from an sdist, installs it without index access in
a fresh venv, and runs real file pipelines and CLI commands outside the checkout.
A separate script validates standard editable and regular pip installs with build
isolation. CI tests supported Python versions, gates coverage, checks artifacts,
and makes publishing an explicit, protected release action.
