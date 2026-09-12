# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""A MotherDuck implementation of the cache, built on the DuckDB implementation."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from duckdb_engine import DuckDBEngineWarning
from overrides import overrides

from datarheo._processors.sql.duckdb import DuckDBSqlProcessor
from datarheo._writers.jsonl import JsonlWriter


if TYPE_CHECKING:
    from datarheo.caches.motherduck import MotherDuckCache


# Suppress warnings from DuckDB about reflection on indices.
# https://github.com/Mause/duckdb_engine/issues/905
warnings.filterwarnings(
    "ignore",
    message="duckdb-engine doesn't yet support reflection on indices",
    category=DuckDBEngineWarning,
)


class MotherDuckSqlProcessor(DuckDBSqlProcessor):
    """A cache implementation for MotherDuck."""

    supports_merge_insert = True  # MotherDuck runs on DuckDB 1.4.0+ with native MERGE INTO support
    file_writer_class = JsonlWriter
    cache: MotherDuckCache

    @overrides
    def _setup(self) -> None:
        """Do any necessary setup, if applicable.

        Note: The DuckDB parent class requires pre-creation of local directory structure. We
        don't need to do that here so we override the method be a no-op.
        """
        # No setup to do and no need to pre-create local file storage.
        pass
