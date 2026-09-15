"""Native connector contracts: named streams of ordinary Python records."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Generator, Iterable, Iterator, Mapping
from contextlib import closing, contextmanager
from copy import deepcopy
from dataclasses import dataclass
from itertools import islice
from typing import Any, TypeVar

from pydatarheo.exceptions import ConfigError, RecordError

Record = dict[str, Any]
_T = TypeVar("_T")


@contextmanager
def _managed_iterator(values: Iterable[_T]) -> Iterator[Iterator[_T]]:
    records = iter(values)
    try:
        yield records
    finally:
        close = getattr(records, "close", None)
        if close is not None:
            close()


def copy_record(value: Mapping[str, Any]) -> Record:
    """Validate and detach a record from its producer."""
    if not isinstance(value, Mapping) or any(not isinstance(key, str) for key in value):
        raise RecordError("Records must be string-keyed mappings")
    return deepcopy(dict(value))


@dataclass(frozen=True)
class Stream:
    """A case-sensitive logical collection of records."""

    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ConfigError("Stream name must be a non-empty string")


class Source(ABC):
    """Implement streams and _read_stream to define a native source connector."""

    @abstractmethod
    def streams(self) -> tuple[Stream, ...]:
        """Return an ordered, non-empty catalog with unique names."""
        raise NotImplementedError

    @abstractmethod
    def _read_stream(self, stream: str) -> Iterator[Record]:
        """Yield records, releasing resources when the iterator closes."""
        raise NotImplementedError

    def _stream_names(self) -> tuple[str, ...]:
        catalog = self.streams()
        if not catalog or any(not isinstance(item, Stream) for item in catalog):
            raise ConfigError("A source must expose at least one Stream")
        names = tuple(item.name for item in catalog)
        if len(set(names)) != len(names):
            raise ConfigError("Stream names must be unique")
        return names

    def check(self) -> None:
        """Check catalog validity; connectors should extend this for connectivity checks."""
        self._stream_names()

    def read(self, stream: str | None = None) -> Generator[Record, None, None]:
        """Lazily read one stream. Select explicitly when a source has multiple streams."""
        names = self._stream_names()
        if stream is None:
            if len(names) != 1:
                raise ConfigError("Select a stream explicitly for a multi-stream source")
            stream = names[0]
        if stream not in names:
            raise ConfigError("Unknown stream selection")
        with _managed_iterator(self._read_stream(stream)) as records:
            for record in records:
                yield copy_record(record)

    def read_batches(
        self, stream: str | None = None, *, batch_size: int = 1000
    ) -> Generator[list[Record], None, None]:
        """Read bounded batches, including a final partial batch."""
        if type(batch_size) is not int or batch_size < 1:
            raise ConfigError("batch_size must be a positive integer")
        with closing(self.read(stream)) as records:
            while batch := list(islice(records, batch_size)):
                yield batch


def transform_records(
    records: Iterable[Mapping[str, Any]],
    transform: Callable[[Record], Mapping[str, Any] | None],
) -> Generator[Record, None, None]:
    """Map detached records lazily; return None from transform to filter a record."""
    with _managed_iterator(records) as rows:
        for record in rows:
            transformed = transform(copy_record(record))
            if transformed is not None:
                yield copy_record(transformed)
