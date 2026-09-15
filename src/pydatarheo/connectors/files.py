"""UTF-8 local file connectors with bounded, pull-based reads."""

from __future__ import annotations

import csv
import json
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any

from pydatarheo.config import Config, _finite_float, _reject_constant
from pydatarheo.core import Record, Source, Stream
from pydatarheo.exceptions import ConfigError, RecordError, SourceError


class _FileSource(Source):
    def __init__(self, config: Mapping[str, Any]) -> None:
        settings = Config(config)
        settings.only("path", "stream")
        path = settings.require("path", str)
        if not path.strip():
            raise ConfigError("Configuration field 'path' must not be empty")
        self.path = Path(path)
        self._stream = Stream(settings.get("stream", "records"))

    def streams(self) -> tuple[Stream, ...]:
        return (self._stream,)

    def check(self) -> None:
        """Check catalog and file accessibility without consuming or validating records."""
        super().check()
        try:
            with self.path.open("r", encoding="utf-8"):
                pass
        except OSError:
            raise SourceError("Source file cannot be opened") from None


class JsonlSource(_FileSource):
    """Read one JSON object per non-blank line; report malformed line numbers safely."""

    def _read_stream(self, stream: str) -> Iterator[Record]:
        try:
            with self.path.open("r", encoding="utf-8") as handle:
                for line_number, line in enumerate(handle, 1):
                    if not line.strip():
                        continue
                    try:
                        record = json.loads(
                            line, parse_constant=_reject_constant, parse_float=_finite_float
                        )
                    except ValueError:
                        raise RecordError(f"Invalid JSON on line {line_number}") from None
                    if not isinstance(record, dict):
                        raise RecordError(f"Expected a JSON object on line {line_number}")
                    yield record
        except (OSError, UnicodeError):
            raise SourceError("Source file cannot be read as UTF-8") from None


class CsvSource(_FileSource):
    """Read a header-based CSV. Values remain strings, including empty cells."""

    def _read_stream(self, stream: str) -> Iterator[Record]:
        try:
            with self.path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.reader(handle, strict=True)
                headers = next(reader, None)
                if not headers or any(not name.strip() for name in headers):
                    raise RecordError("CSV must have a non-empty header row")
                if len(set(headers)) != len(headers):
                    raise RecordError("CSV column names must be unique")
                for values in reader:
                    if not values:
                        continue
                    if len(values) != len(headers):
                        raise RecordError(f"CSV column count mismatch on line {reader.line_num}")
                    yield dict(zip(headers, values, strict=True))
        except csv.Error:
            raise RecordError("Invalid CSV format") from None
        except (OSError, UnicodeError):
            raise SourceError("Source file cannot be read as UTF-8") from None
