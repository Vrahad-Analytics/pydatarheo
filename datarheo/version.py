# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""Support for PyDataRheo version checks."""

from __future__ import annotations

import importlib.metadata


DISTRIBUTION_NAME = "pydatarheo"
"""The name PyDataRheo is published under on PyPI.

The import package is `datarheo`; the distribution that provides it is `pydatarheo`.
"""

datarheo_version = importlib.metadata.version(DISTRIBUTION_NAME)


def get_version() -> str:
    """Return the version of PyDataRheo."""
    return datarheo_version
