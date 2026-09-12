<p align="center">
  <img src="https://raw.githubusercontent.com/Vrahad-Analytics/pydatarheo/main/docs/brand/pydatarheo-logo.svg" alt="PyDataRheo" width="260">
</p>

# PyDataRheo

**PyDataRheo moves data between hundreds of systems, from plain Python.**

Pick a source, read from it, and land the records in DuckDB, Postgres, Snowflake, BigQuery,
MotherDuck, or any destination connector. No orchestrator, no cluster, no YAML pipeline
definition. It is a library, so it runs wherever your Python runs: a script, a notebook, a
Lambda, an Airflow or Dagster task.

PyDataRheo runs [Airbyte-protocol connectors](https://docs.airbyte.com/integrations/), which is
what gives it several hundred sources and destinations on day one.

[![PyPI version](https://badge.fury.io/py/pydatarheo.svg)](https://badge.fury.io/py/pydatarheo)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pydatarheo)](https://pypi.org/project/pydatarheo/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydatarheo)](https://pypi.org/project/pydatarheo/)
[![Star on GitHub](https://img.shields.io/github/stars/Vrahad-Analytics/pydatarheo.svg?style=social&label=★%20on%20GitHub)](https://github.com/Vrahad-Analytics/pydatarheo)

## Install

```bash
pip install pydatarheo
```

The import package is `datarheo`; the distribution on PyPI is `pydatarheo`.

## Quick start

```py
import datarheo as dr

source = dr.get_source(
    "source-faker",
    config={"count": 5_000},
    install_if_missing=True,
)
source.check()
source.select_all_streams()

result = source.read()  # Lands in a local DuckDB cache by default.

for record in result["users"].records:
    print(record)
```

Read into a dataframe:

```py
df = result["users"].to_pandas()
```

Write to a real warehouse instead of the default local cache:

```py
from datarheo.caches import SnowflakeCache

cache = SnowflakeCache(
    account="my-account",
    username="my-user",
    password=dr.get_secret("SNOWFLAKE_PASSWORD"),
    database="my-db",
    warehouse="my-wh",
    role="my-role",
)
source.read(cache=cache)
```

## Command line

These console scripts are installed:

| Command | What it does |
| --- | --- |
| `pydatarheo` / `pydr` | Benchmark, validate, and smoke-test connectors |
| `datarheo-mcp` | Run the DataRheo MCP server over stdio |
| `datarheo-mcp-http` | Run the DataRheo MCP server over HTTP |

```bash
pydr --help
pydr validate --connector=source-faker
```

## Connector installation

### Declarative (YAML) sources

Declarative sources are downloaded as a single YAML manifest and executed directly. These have
the fastest install times, because there is nothing to build.

### Python sources

When a connector publishes a Python package, PyDataRheo installs it automatically. Installation
uses [`uv`](https://docs.astral.sh/uv) rather than `pip`, which is both much faster and able to
install a connector under a different Python version than the one PyDataRheo itself is running
on. Set `DATARHEO_NO_UV=true` to fall back to `pip`.

To pin a connector to a specific Python version:

```py
source = dr.get_source("source-faker", use_python="3.10.17")
```

### Docker

Pass `docker_image=True` to `get_source()` or `get_destination()` to run the connector from its
published image instead, or `docker_image="my-org/my-image:tag"` to pick an exact image. Docker
is the most reproducible option, because every dependency is locked inside the image, and it is
required for Java-based destinations.

## Configuration

Every environment variable PyDataRheo reads is prefixed `DATARHEO_`. The most useful ones:

| Variable | Effect |
| --- | --- |
| `DATARHEO_CACHE_ROOT` | Where cache files are written (default `./.cache`) |
| `DATARHEO_PROJECT_DIR` | Parent directory for cache and connector installs |
| `DATARHEO_NO_UV` | Set to `1` to install connectors with `pip` instead of `uv` |
| `DATARHEO_OFFLINE_MODE` | Tolerate an unreachable connector registry; also disables telemetry |
| `DATARHEO_TEMP_DIR` | Directory for temporary files |
| `DATARHEO_CLOUD_CLIENT_ID` / `DATARHEO_CLOUD_CLIENT_SECRET` | Credentials for the hosted Cloud API |

An environment still carrying the older `AIRBYTE_`-prefixed names keeps working: each
`AIRBYTE_FOO` is read as `DATARHEO_FOO` unless the `DATARHEO_` name is also set, in which case
the explicit `DATARHEO_` value wins.

## Telemetry

**Off by default.** PyDataRheo sends nothing anywhere unless you set `DATARHEO_TRACKING_KEY` to
a Segment write key that you own. Setting `DO_NOT_TRACK`, or enabling offline mode, disables
reporting outright.

## Documentation

The full API reference is generated from the source with `poe docs-generate` and published at
[vrahad-analytics.github.io/pydatarheo](https://vrahad-analytics.github.io/pydatarheo).

## Contributing

See the [Contributors Guide](https://github.com/Vrahad-Analytics/pydatarheo/blob/main/docs/CONTRIBUTING.md).

## Frequently asked questions

**Is PyDataRheo a replacement for a data platform?**
No. It is a library. It has no orchestration, scheduling, alerting, or pipeline monitoring. Run
it inside whatever scheduler you already use.

**What is the cache? Is it a destination?**
Effectively yes: it is a built-in destination implementation backed by a SQL engine. We call it
a cache to keep it distinct from the destination connectors, which are separate executables.

**Does it work with Airflow, Dagster, Prefect, or Snowpark?**
Yes. It is an ordinary Python dependency with no background services.

**Can I build a normal ETL pipeline with it?**
Yes. Choose the cache type that matches where the data should land, such as `SnowflakeCache` for
Snowflake.

**Can it run a connector from a local directory?**
Yes. Any connector exposing a CLI works, and connectors already on `PATH` are found by name.

## License and provenance

PyDataRheo is released under the MIT license and is a rebranded derivative of
[PyAirbyte](https://github.com/airbytehq/PyAirbyte), which is also MIT licensed. See
[LICENSE](https://github.com/Vrahad-Analytics/pydatarheo/blob/main/LICENSE) and [NOTICE](https://github.com/Vrahad-Analytics/pydatarheo/blob/main/NOTICE).

## Changelog

See the [GitHub Releases](https://github.com/Vrahad-Analytics/pydatarheo/releases) page.
