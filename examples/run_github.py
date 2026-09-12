# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""A simple test of PyDataRheo, using the Faker source connector.

Usage (from PyDataRheo root directory):
> poetry run python ./examples/run_github.py

No setup is needed, but you may need to delete the .venv-source-faker folder
if your installation gets interrupted or corrupted.
"""

from __future__ import annotations

import datarheo as dr


# Create a token here: https://github.com/settings/tokens
GITHUB_TOKEN = dr.get_secret("GITHUB_PERSONAL_ACCESS_TOKEN")


source = dr.get_source("source-github")
source.set_config({
    "repositories": ["airbytehq/airbyte-lib-private-beta"],
    "credentials": {"personal_access_token": GITHUB_TOKEN},
})
source.check()
source.select_streams([
    "issues",
    "pull_requests",
    "commits",
    "collaborators",
    "deployments",
])

result = source.read(cache=dr.new_local_cache("github"))
print(result.processed_records)

for name, records in result.streams.items():
    print(f"Stream {name}: {len(records)} records")
