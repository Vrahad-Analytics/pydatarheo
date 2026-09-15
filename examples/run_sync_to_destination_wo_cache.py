# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.

"""Test a sync to an Airbyte destination.

Usage:
```
poetry run python examples/run_sync_to_destination_wo_cache.py
```
"""

from __future__ import annotations

import datetime

import datarheo as dr

SCALE = 200_000


def get_my_source() -> dr.Source:
    # Create a token here: https://github.com/settings/tokens
    # Then export as env var `GITHUB_PERSONAL_ACCESS_TOKEN`
    github_pat = dr.get_secret("GITHUB_PERSONAL_ACCESS_TOKEN")
    assert str(github_pat), "Could not locate Github PAT"
    source = dr.get_source(
        "source-github",
        config={
            "repositories": ["Vrahad-Analytics/pydatarheo"],
            "credentials": {
                "personal_access_token": github_pat,
            },
        },
    )
    source.check()
    source.select_streams(["issues"])
    return source


def get_cache() -> dr.DuckDBCache:
    return dr.new_local_cache(
        cache_name="state_cache",
    )


def get_my_destination() -> dr.Destination:
    return dr.get_destination(
        name="destination-duckdb",
        config={
            # This path is relative to the container:
            "destination_path": "/local/temp/db.duckdb",
        },
        docker_image="airbyte/destination-duckdb:latest",
        # OR:
        # pip_url="git+https://github.com/airbytehq/airbyte.git#subdirectory=airbyte-integrations/connectors/destination-duckdb",
    )


def main() -> None:
    """Test writing from the source to the destination."""
    source = get_my_source()
    source.check()
    destination = get_my_destination()
    destination.check()
    state_cache = get_cache()
    write_result: dr.WriteResult = destination.write(
        source,
        cache=False,
        state_cache=state_cache,
    )
    print(
        f"Completed writing {write_result.processed_records:,} records "
        f"to destination at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
    )


if __name__ == "__main__":
    main()
