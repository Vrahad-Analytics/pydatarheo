# pydatarheo examples

Install from the repository root with `python -m pip install .`. Every example
runs offline on Python 3.10+ without secrets. Run the following from that root;
output parent directories must exist and output paths must be unused.

## 1. Basic configuration and iteration

```bash
python examples/basic.py
```

Configures a memory source, checks it, and prints each record:

```text
{'id': 1, 'name': 'Ada'}
```

## 2. Custom connector and batching

```bash
python examples/custom_connector.py
```

Defines a generator-backed source, validates its count, registers a factory on a
local registry, and reads batches of two. Expected output:

```text
[{'number': 0}, {'number': 1}]
[{'number': 2}, {'number': 3}]
[{'number': 4}]
```

Unlike a memory source, this generator does not store all records in advance.
Change `read_batches()` to `read()` to consume one record at a time. Close either
iterator with `contextlib.closing` if stopping before it is exhausted.

## 3. Retry boundaries and debugging

```bash
python examples/retries_and_logging.py
```

Simulates an idempotent page fetch that fails twice, enables application-owned
logging, and handles the framework exception boundary. Debug output on stderr:

```text
pydatarheo.retry: Retrying operation after attempt 1
pydatarheo.retry: Retrying operation after attempt 2
```

Summary on stdout:

```text
Fetched 1 record after 3 attempts
```

Only `TransientError` is retried. Real connectors should retry a page request
before yielding that page, not a stream that already delivered partial data.
Do not log request headers, secret configuration, or complete record bodies.

## 4. Full local sales pipeline

```bash
python examples/pipeline.py --output /tmp/pydatarheo-sales.jsonl
```

Reads `data/sales.csv` relative to the script, converts explicitly typed integer
fields, computes totals in cents, and writes an atomic UTF-8 JSONL file.
Expected stdout: `Wrote 3 sales records`.

Expected file contents:

```jsonl
{"id": 1, "customer": "Ada", "total_cents": 2500}
{"id": 2, "customer": "Lin", "total_cents": 999}
{"id": 3, "customer": "Renée", "total_cents": 1500}
```

A second run with the same path raises `SinkError` and preserves the first output.
Choose a new path to rerun. The script does not delete or overwrite user data.
Use `CsvSink(path, columns=[...])` for scalar CSV output or `MemorySink()` for a
small in-memory result; neither performs automatic field conversion.

## 5. CLI workflow

```bash
pydatarheo read --source csv --input examples/data/sales.csv --output /tmp/pydatarheo-cli.jsonl
```

Expected stdout: `Wrote 3 records`. This copies all CSV columns as strings;
it does not apply the sales transformation. `pydr` and `python -m pydatarheo`
provide the same interface. Use `--help` or `--version` for discovery.

The e2e suite runs all four Python examples and the CLI against a freshly
installed wheel outside the source tree. See ../ARCHITECTURE.md for extension
contracts and ../INSTALL.md for environment verification.
