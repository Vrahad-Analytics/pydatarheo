"""Repeatable, isolated in-memory data for small pipelines and tests."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import Any

from pydatarheo.config import Config
from pydatarheo.core import Record, Source, Stream, copy_record


class MemorySource(Source):
    """Snapshot a list of records. All input is held in memory."""

    def __init__(self, config: Mapping[str, Any]) -> None:
        settings = Config(config)
        settings.only("records", "stream")
        self._stream = Stream(settings.get("stream", "records"))
        self._records = tuple(copy_record(row) for row in settings.require("records", list))

    def streams(self) -> tuple[Stream, ...]:
        return (self._stream,)

    def _read_stream(self, stream: str) -> Iterator[Record]:
        yield from self._records
