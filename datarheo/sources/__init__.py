# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""Sources connectors module for PyDataRheo."""

from __future__ import annotations

from typing import TYPE_CHECKING

from datarheo.registry import (
    ConnectorMetadata,
    get_available_connectors,
    get_connector_metadata,
)
from datarheo.sources.base import Source
from datarheo.sources.util import (
    get_benchmark_source,
    get_source,
)

# Submodules imported here for documentation reasons: https://github.com/mitmproxy/pdoc/issues/757
if TYPE_CHECKING:
    # ruff: noqa: TC004  # imports used for more than type checking
    from datarheo.sources import (
        base,
        registry,
        util,
    )

__all__ = [
    # Submodules
    "base",
    "registry",
    "util",
    # Factories
    "get_source",
    "get_benchmark_source",
    # Helper Functions
    "get_available_connectors",
    "get_connector_metadata",
    # Classes
    "Source",
    "ConnectorMetadata",
]
