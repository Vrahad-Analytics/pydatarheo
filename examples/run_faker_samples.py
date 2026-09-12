# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""A simple test of PyDataRheo, using the Faker source connector.

Usage (from PyDataRheo root directory):
> poetry run python ./examples/run_faker_samples.py
"""

import datarheo as dr


source = dr.get_source(
    "source-faker",
    config={"count": 200_000},
    streams="*",
)

# Print samples of the streams.
source.print_samples()
