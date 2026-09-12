# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""A simple test of PyDataRheo, using the File source connector.

Usage (from PyDataRheo root directory):
> poetry run python ./examples/run_file.py

No setup is needed, but you may need to delete the .venv-source-file folder
if your installation gets interrupted or corrupted.
"""

from __future__ import annotations

import datarheo as dr


source = dr.get_source(
    "source-file",
    install_if_missing=True,
)
source.check()

# print(list(source.get_records("pokemon")))
source.read(cache=dr.new_local_cache("poke"))
