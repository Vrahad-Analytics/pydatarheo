"""Explicit bridge to the retained connector, warehouse, cloud, and MCP runtime.

Install `pydatarheo[connectors]` to enable this module's delegated capabilities.
External protocol/package identifiers remain truthful for interoperability.
"""

from __future__ import annotations

from importlib import import_module
from types import ModuleType
from typing import Any

from pydatarheo.exceptions import ConfigError


class ConnectorDependencyError(ConfigError):
    """The optional connector runtime is not installed completely."""


def backend() -> ModuleType:
    """Load the retained implementation only when explicitly requested."""
    try:
        return import_module("datarheo")
    except ModuleNotFoundError as error:
        raise ConnectorDependencyError(
            "Install the connector runtime with python -m pip install 'pydatarheo[connectors]' "
            "(from a checkout: python -m pip install '.[connectors]'). "
            f"Missing module: {error.name}"
        ) from error


def get_source(name: str, config: dict[str, Any] | None = None, **kwargs: Any) -> Any:
    """Create a retained source, preserving its stream/cache/state APIs and options."""
    return backend().get_source(name, config=config, **kwargs)


def get_destination(name: str, **kwargs: Any) -> Any:
    """Create a retained destination connector without altering its protocol."""
    return backend().get_destination(name, **kwargs)


def __getattr__(name: str) -> Any:
    if name.startswith("_"):
        raise AttributeError(name)
    return getattr(backend(), name)
