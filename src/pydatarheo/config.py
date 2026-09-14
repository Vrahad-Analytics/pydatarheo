"""Explicit configuration snapshots with no implicit environment or secret lookup."""

from __future__ import annotations

import json
import math
from collections.abc import Iterator, Mapping
from copy import deepcopy
from typing import Any

from pydatarheo.exceptions import ConfigError


def _reject_constant(value: str) -> None:
    raise ValueError("Non-finite JSON numbers are not supported")


def _finite_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("JSON number exceeds the supported floating-point range")
    return number


class Config(Mapping[str, Any]):
    """A defensive copy of a string-keyed mapping; repr never contains values."""

    def __init__(self, values: Mapping[str, Any]) -> None:
        if not isinstance(values, Mapping) or any(not isinstance(key, str) for key in values):
            raise ConfigError("Configuration must be a string-keyed mapping")
        self._values = deepcopy(dict(values))

    @classmethod
    def from_json(cls, text: str) -> Config:
        """Parse a JSON object, reporting errors without exposing configuration values."""
        try:
            return cls(json.loads(text, parse_constant=_reject_constant, parse_float=_finite_float))
        except (TypeError, ValueError):
            raise ConfigError("Configuration must be a valid JSON object") from None

    def __getitem__(self, key: str) -> Any:
        return deepcopy(self._values[key])

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def __repr__(self) -> str:
        return f"Config(<{len(self)} fields; values redacted>)"

    def require(self, key: str, expected_type: type) -> Any:
        """Require a field of the requested type without coercing values."""
        if key not in self or not isinstance(self._values[key], expected_type):
            raise ConfigError(f"Configuration field '{key}' must be {expected_type.__name__}")
        return self[key]

    def only(self, *keys: str) -> None:
        """Reject unsupported options rather than silently ignoring typos."""
        if self.keys() - set(keys):
            raise ConfigError("Configuration contains unsupported fields")
