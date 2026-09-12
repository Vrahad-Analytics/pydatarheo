# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""A simple test of PyDataRheo, using the Faker source connector.

Usage (from PyDataRheo root directory):
> poetry run python ./examples/run_faker.py

No setup is needed, but you may need to delete the .venv-source-faker folder
if your installation gets interrupted or corrupted.
"""

from __future__ import annotations

import datarheo as dr

SCALE = 200_000  # Number of records to generate between users and purchases.
FORCE_FULL_REFRESH = True  # Whether to force a full refresh on the source.


cache = dr.get_default_cache()
source = dr.get_source(
    "source-faker",
    config={"count": SCALE / 2},
    install_if_missing=True,
)
source.check()
source.select_streams(["products", "users", "purchases"])

result = source.read(
    cache=cache,
    force_full_refresh=FORCE_FULL_REFRESH,
)

print("Read complete. Validating results...")
for name, records in result.streams.items():
    print(f"Stream {name}: {len(records)} records")
