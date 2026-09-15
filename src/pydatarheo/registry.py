"""Explicit local connector registration, without remote discovery or code installation."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from pydatarheo.config import Config
from pydatarheo.connectors import CsvSource, JsonlSource, MemorySource
from pydatarheo.core import Source
from pydatarheo.exceptions import ConfigError

SourceFactory = Callable[[Mapping[str, Any]], Source]


class SourceRegistry:
    """An application-owned registry. Instances never share registrations."""

    def __init__(self) -> None:
        self._factories: dict[str, SourceFactory] = {}

    def register(self, name: str, factory: SourceFactory) -> None:
        if not isinstance(name, str) or not name.strip() or not callable(factory):
            raise ConfigError("A connector requires a non-empty name and callable factory")
        if name in self._factories:
            raise ConfigError("Connector name is already registered")
        self._factories[name] = factory

    def available(self) -> tuple[str, ...]:
        return tuple(sorted(self._factories))

    def create(self, name: str, config: Mapping[str, Any]) -> Source:
        if name not in self._factories:
            raise ConfigError("Unknown connector; register a native source factory first")
        source = self._factories[name](Config(config))
        if not isinstance(source, Source):
            raise ConfigError("Connector factory must return a Source")
        return source


def builtin_registry() -> SourceRegistry:
    """Return an independent registry populated with the shipped source types."""
    registry = SourceRegistry()
    registry.register("memory", MemorySource)
    registry.register("jsonl", JsonlSource)
    registry.register("csv", CsvSource)
    return registry


def get_source(name: str, config: Mapping[str, Any] | None = None, **kwargs: Any) -> Any:
    """Configure a native source or delegate a source-* name to the retained runtime."""
    if name.startswith("source-"):
        from pydatarheo.compat import get_source as get_connector_source

        return get_connector_source(
            name, config=dict(config) if config is not None else None, **kwargs
        )
    if kwargs:
        raise ConfigError("Native sources do not accept external execution options")
    return builtin_registry().create(name, config if config is not None else {})
