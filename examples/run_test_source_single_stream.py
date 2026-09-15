# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
from __future__ import annotations

import os

import datarheo as dr


# preparation (from PyDataRheo main folder):
#   python -m venv .venv-source-test
#   source .venv-source-test/bin/activate
#   pip install -e ./tests/integration_tests/fixtures/source-test
# In separate terminal:
#   poetry run python examples/run_test_source.py

os.environ["DATARHEO_LOCAL_REGISTRY"] = (
    "./tests/integration_tests/fixtures/registry.json"
)

source = dr.get_source("source-test", config={"apiKey": "test"})

print(list(source.read(streams=["stream1"])))
