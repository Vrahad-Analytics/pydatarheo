# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""Base module for all caches."""

from __future__ import annotations

from typing import TYPE_CHECKING

from datarheo.caches.base import CacheBase
from datarheo.caches.bigquery import BigQueryCache
from datarheo.caches.duckdb import DuckDBCache
from datarheo.caches.motherduck import MotherDuckCache
from datarheo.caches.postgres import PostgresCache
from datarheo.caches.snowflake import SnowflakeCache
from datarheo.caches.util import get_default_cache, new_local_cache


# Submodules imported here for documentation reasons: https://github.com/mitmproxy/pdoc/issues/757
if TYPE_CHECKING:
    # ruff: noqa: TC004
    from datarheo.caches import base, bigquery, duckdb, motherduck, postgres, snowflake, util

# We export these classes for easy access: `datarheo.caches...`
__all__ = [
    # Factories
    "get_default_cache",
    "new_local_cache",
    # Classes
    "BigQueryCache",
    "CacheBase",
    "DuckDBCache",
    "MotherDuckCache",
    "PostgresCache",
    "SnowflakeCache",
    # Submodules,
    "util",
    "bigquery",
    "duckdb",
    "motherduck",
    "postgres",
    "snowflake",
    "base",
]
