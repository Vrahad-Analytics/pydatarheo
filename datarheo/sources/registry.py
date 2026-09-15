# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""Backwards compatibility shim for datarheo.sources.registry.

This module re-exports symbols from datarheo.registry for backwards compatibility.
New code should import from datarheo.registry directly.
"""

from __future__ import annotations

from datarheo.registry import (
    ConnectorMetadata,
    InstallType,
    Language,
    get_available_connectors,
    get_connector_metadata,
)

__all__ = [
    "ConnectorMetadata",
    "InstallType",
    "Language",
    "get_available_connectors",
    "get_connector_metadata",
]
