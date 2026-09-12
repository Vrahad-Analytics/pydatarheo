# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""A MotherDuck implementation of the PyDataRheo cache, built on DuckDB.

## Usage Example

```python
from datarheo as ab
from datarheo.caches import MotherDuckCache

cache = MotherDuckCache(
    database="mydatabase",
    schema_name="myschema",
    api_key=ab.get_secret("MOTHERDUCK_API_KEY"),
)
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, ClassVar

from airbyte_api.models import DestinationDuckdb
from duckdb_engine import DuckDBEngineWarning
from overrides import overrides
from pydantic import Field

from datarheo._processors.sql.duckdb import DuckDBConfig
from datarheo._processors.sql.motherduck import MotherDuckSqlProcessor
from datarheo.caches._utils._cache_to_dest import (
    motherduck_cache_to_destination_configuration,
)
from datarheo.caches.duckdb import DuckDBCache
from datarheo.secrets import SecretString


if TYPE_CHECKING:
    from datarheo.shared.sql_processor import SqlProcessorBase


class MotherDuckConfig(DuckDBConfig):
    """Configuration for the MotherDuck cache."""

    database: str = Field()
    api_key: SecretString = Field()
    db_path: str = Field(default="md:")  # pyrefly: ignore[bad-override]
    _paired_destination_name: str = "destination-motherduck"

    @overrides
    def get_sql_alchemy_url(self) -> SecretString:
        """Return the SQLAlchemy URL to use."""
        # Suppress warnings from DuckDB about reflection on indices.
        # https://github.com/Mause/duckdb_engine/issues/905
        warnings.filterwarnings(
            "ignore",
            message="duckdb-engine doesn't yet support reflection on indices",
            category=DuckDBEngineWarning,
        )

        return SecretString(
            f"duckdb:///md:{self.database}?motherduck_token={self.api_key}"
            # Not sure why this doesn't work. We have to override later in the flow.
            # f"&schema={self.schema_name}"
        )

    @overrides
    def get_database_name(self) -> str:
        """Return the name of the database."""
        return self.database


class MotherDuckCache(MotherDuckConfig, DuckDBCache):
    """Cache that uses MotherDuck for external persistent storage."""

    _sql_processor_class: ClassVar[type[SqlProcessorBase]] = MotherDuckSqlProcessor

    paired_destination_name: ClassVar[str | None] = "destination-motherduck"
    paired_destination_config_class: ClassVar[type | None] = DestinationDuckdb

    @property
    def paired_destination_config(self) -> DestinationDuckdb:
        """Return a dictionary of destination configuration values."""
        return motherduck_cache_to_destination_configuration(cache=self)


# Expose the Cache class and also the Config class.
__all__ = [
    "MotherDuckCache",
    "MotherDuckConfig",
]
