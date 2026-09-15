# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""***PyDataRheo moves data between hundreds of systems, from plain Python.***

[![PyPI version](https://badge.fury.io/py/pydatarheo.svg)](https://badge.fury.io/py/pydatarheo)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pydatarheo)](https://pypi.org/project/pydatarheo/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydatarheo)](https://pypi.org/project/pydatarheo/)
[![Star on GitHub](https://img.shields.io/github/stars/Vrahad-Analytics/pydatarheo.svg?style=social&label=★%20on%20GitHub)](https://github.com/Vrahad-Analytics/pydatarheo)

PyDataRheo is a library, not a platform. Pick a source, read from it, and land the records
somewhere useful. It runs wherever your Python runs, with no orchestrator and no cluster.

Connector packages and metadata come from the public open connector registry,
which is what gives PyDataRheo several hundred sources and destinations without
shipping any integration code of its own.

Install it with `pip install pydatarheo`. The import package is `datarheo`.

# Getting Started

## Reading Data

You can connect to any of hundreds of sources from the connector registry
using the `get_source` method. You can then read data from sources using `Source.read` method.

```python
from datarheo import get_source

source = get_source(
    "source-faker",
    config={},
)
read_result = source.read()

for record in read_result["users"].records:
    print(record)
```

For more information, see the `datarheo.sources` module.

## Writing to SQL Caches

Data can be written to caches using a number of SQL-based cache implementations, including
Postgres, BigQuery, Snowflake, DuckDB, and MotherDuck. If you do not specify a cache, PyDataRheo
will automatically use a local DuckDB cache by default.

For more information, see the `datarheo.caches` module.

## Writing to Destination Connectors

Data can be written to destinations using the `Destination.write` method. You can connect to
destinations using the `get_destination` method. PyDataRheo supports every destination connector
published in the registry, but Docker is required on your machine in order to run
Java-based destinations.

**Note:** When loading to a SQL database, we recommend using SQL cache (where available,
[see above](#writing-to-sql-caches)) instead of a destination connector. This is because SQL caches
are Python-native and therefor more portable when run from different Python-based environments which
might not have Docker container support. Destinations in PyDataRheo are uniquely suited for loading
to non-SQL platforms such as vector stores and other reverse ETL-type use cases.

For more information, see the `datarheo.destinations` module and the full list of destination
connectors in the public registry.

# PyDataRheo API

## Importing as `dr`

Most examples in the PyDataRheo documentation use the `import datarheo as dr` convention. The `dr`
alias is recommended, making code more concise and readable. When getting started, this
also saves you from digging in submodules to find the classes and functions you need, since
frequently-used classes and functions are available at the top level of the `datarheo` module.

## Navigating the API

While many PyDataRheo classes and functions are available at the top level of the `datarheo`
module, you can also import classes and functions from submodules directly. For example, while you
can import the `Source` class from `datarheo`, you can also import it from the `sources` submodule
like this:

```python
from datarheo.sources import Source
```

Whether you import from the top level or from a submodule, the classes and functions are the same.
We expect that most users will import from the top level when getting started, and then import from
submodules when they are deploying more complex implementations.

For quick reference, top-Level modules are listed in the left sidebar of this page.

# Configuration

Every environment variable PyDataRheo reads is prefixed `DATARHEO_`, for example
`DATARHEO_CACHE_ROOT` and `DATARHEO_NO_UV`. An environment still carrying the older
`AIRBYTE_`-prefixed names keeps working: each `AIRBYTE_FOO` is read as `DATARHEO_FOO`
unless the `DATARHEO_` name is also set.

Usage reporting is off by default and sends nothing unless `DATARHEO_TRACKING_KEY` is set. See
the `datarheo.constants` module for the full list of settings.

# Other Resources

- [PyDataRheo GitHub Readme](https://github.com/Vrahad-Analytics/pydatarheo)
- [PyDataRheo Issue Tracker](https://github.com/Vrahad-Analytics/pydatarheo/issues)
- [Frequently Asked Questions](https://github.com/Vrahad-Analytics/pydatarheo/blob/main/docs/faq.md)
- [PyDataRheo Contributors Guide](https://github.com/Vrahad-Analytics/pydatarheo/blob/main/docs/CONTRIBUTING.md)
- [GitHub Releases](https://github.com/Vrahad-Analytics/pydatarheo/releases)

----------------------

# API Reference

Below is a list of all classes, functions, and modules available in the top-level `datarheo`
module. (This is a long list!) If you are just starting out, we recommend beginning by selecting a
submodule to navigate to from the left sidebar or from the list below:

Each module
has its own documentation and code samples related to effectively using the related capabilities.

- **`datarheo.cloud`** - Working with the hosted cloud API, including running jobs
    remotely.
- **`datarheo.agents`** - Working with the agents platform, including executing single
    read and write actions on Agents connectors.
- **`datarheo.caches`** - Working with caches, including how to inspect a cache and get data from
    it.
- **`datarheo.datasets`** - Working with datasets, including how to read from datasets and convert
    to
    other formats, such as Pandas, Arrow, and LLM Document formats.
- **`datarheo.destinations`** - Working with destinations, including how to write to destination
    connectors.
- **`datarheo.documents`** - Working with LLM documents, including how to convert records into
    document formats, for instance, when working with AI libraries like LangChain.
- **`datarheo.exceptions`** - Definitions of all exception and warning classes used in PyDataRheo.
- **`datarheo.experimental`** - Experimental features and utilities that do not yet have a stable
    API.
- **`datarheo.logs`** - Logging functionality and configuration.
- **`datarheo.records`** - Internal record handling classes.
- **`datarheo.results`** - Documents the classes returned when working with results from
    `Source.read` and `Destination.write`
- **`datarheo.secrets`** - Tools for managing secrets in PyDataRheo.
- **`datarheo.sources`** - Tools for creating and reading from sources. This includes
    `datarheo.source.get_source` to declare a source, `datarheo.source.Source.read` for reading
    data, and `datarheo.source.Source.get_records()` to peek at records without caching or writing
    them directly.

----------------------

"""  # noqa: D415

from __future__ import annotations

from typing import TYPE_CHECKING

from datarheo import registry
from datarheo.caches.bigquery import BigQueryCache
from datarheo.caches.duckdb import DuckDBCache
from datarheo.caches.util import get_colab_cache, get_default_cache, new_local_cache
from datarheo.datasets import CachedDataset
from datarheo.destinations.base import Destination
from datarheo.destinations.util import get_destination
from datarheo.records import StreamRecord
from datarheo.registry import get_available_connectors
from datarheo.results import ReadResult, WriteResult
from datarheo.secrets import SecretSourceEnum, get_secret
from datarheo.sources.base import Source
from datarheo.sources.util import get_source

# Submodules imported here for documentation reasons: https://github.com/mitmproxy/pdoc/issues/757
if TYPE_CHECKING:
    # ruff: noqa: TC004  # imports used for more than type checking
    from datarheo import (
        agents,
        caches,
        callbacks,
        cli,
        cloud,
        constants,
        datasets,
        destinations,
        documents,
        exceptions,  # noqa: ICN001  # No 'exc' alias for top-level module
        experimental,
        logs,
        mcp,
        records,
        results,
        secrets,
        sources,
    )


__all__ = [
    # Modules
    "agents",
    "caches",
    "callbacks",
    "cli",
    "cloud",
    "constants",
    "datasets",
    "destinations",
    "documents",
    "exceptions",
    "experimental",
    "logs",
    "mcp",
    "records",
    "registry",
    "results",
    "secrets",
    "sources",
    # Factories
    "get_available_connectors",
    "get_colab_cache",
    "get_default_cache",
    "get_destination",
    "get_secret",
    "get_source",
    "new_local_cache",
    # Classes
    "BigQueryCache",
    "CachedDataset",
    "Destination",
    "DuckDBCache",
    "ReadResult",
    "SecretSourceEnum",
    "Source",
    "StreamRecord",
    "WriteResult",
]

__docformat__ = "google"
