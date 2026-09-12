# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""A Generic SQL Cache implementation."""

from __future__ import annotations

from overrides import overrides

from datarheo.caches.base import CacheBase
from datarheo.secrets.base import SecretString


class GenericSQLCacheConfig(CacheBase):
    """Allows configuring 'sql_alchemy_url' directly."""

    sql_alchemy_url: SecretString | str

    @overrides
    def get_sql_alchemy_url(self) -> SecretString:
        """Returns a SQL Alchemy URL."""
        return SecretString(self.sql_alchemy_url)
