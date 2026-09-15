# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""A simple test of PyDataRheo, using the PokeAPI source connector.

Usage (from PyDataRheo root directory):
> poetry run python ./examples/run_pokeapi.py

No setup is needed, but you may need to delete the .venv-source-pokeapi folder
if your installation gets interrupted or corrupted.
"""

from __future__ import annotations

import datarheo as dr
from datarheo import get_source


source = get_source(
    "source-pokeapi",
    config={"pokemon_name": "bulbasaur"},
    source_manifest=True,
)
source.check()

# print(list(source.get_records("pokemon")))
source.read(cache=dr.new_local_cache("poke"))
