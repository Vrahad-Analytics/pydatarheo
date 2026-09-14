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


def get_source(name: str, *, config: Mapping[str, Any]) -> Source:
    """Configure a built-in connector by its native name."""
    return builtin_registry().create(name, config)
