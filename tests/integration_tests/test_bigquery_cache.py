# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""Unit tests specific to BigQuery caches."""

from __future__ import annotations

import pytest

import datarheo as dr


@pytest.mark.requires_creds
def test_bigquery_props(
    new_bigquery_cache: dr.BigQueryCache,
) -> None:
    """Test that the BigQueryCache properties are set correctly."""
    # assert new_bigquery_cache.credentials_path.endswith(".json")
    assert new_bigquery_cache.dataset_name == new_bigquery_cache.schema_name, (
        "Dataset name should be the same as schema name."
    )
    assert new_bigquery_cache.schema_name != "datarheo_raw", (
        "Schema name should not be the default value."
    )

    assert new_bigquery_cache.get_database_name() == new_bigquery_cache.project_name, (
        "Database name should be the same as project name."
    )
