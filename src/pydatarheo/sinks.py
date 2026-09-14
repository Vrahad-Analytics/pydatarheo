"""Local sinks: publish complete files atomically and refuse accidental overwrite."""

from __future__ import annotations

import csv
import json
import os
import tempfile
from collections.abc import Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import Any, TextIO

from pydatarheo.core import Record, _managed_iterator, copy_record
from pydatarheo.exceptions import ConfigError, RecordError, SinkError


@contextmanager
def _atomic_text(path: Path, overwrite: bool) -> Iterator[TextIO]:
    temporary: Path | None = None
    try:
        if not overwrite and path.exists():
            raise SinkError("Output already exists; choose a new path or set overwrite=True")
        descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        temporary = Path(name)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            yield handle
            handle.flush()
            os.fsync(handle.fileno())
        if overwrite:
            os.replace(temporary, path)
        else:
            os.link(temporary, path)
    except UnicodeError:
        raise RecordError("Output contains text that cannot be encoded as UTF-8") from None
    except OSError:
        raise SinkError("Output could not be published; check its parent and permissions") from None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


class JsonlSink:
    """Serialize strict JSON objects, one per line, to a new UTF-8 file."""

    def __init__(self, path: str | Path, *, overwrite: bool = False) -> None:
        self.path = Path(path)
        self.overwrite = overwrite

    def write(self, records: Iterable[Mapping[str, Any]]) -> int:
        count = 0
        with _atomic_text(self.path, self.overwrite) as handle, _managed_iterator(records) as rows:
            for record in rows:
                row = copy_record(record)
                try:
                    encoded = json.dumps(row, ensure_ascii=False, allow_nan=False)
                except (TypeError, ValueError, OverflowError):
                    raise RecordError("Record cannot be serialized as strict JSON") from None
                handle.write(encoded + "\n")
                count += 1
        return count


class CsvSink:
    """Write an explicit column schema. Missing/extra fields are rejected; None becomes empty."""

    def __init__(
        self, path: str | Path, *, columns: Sequence[str], overwrite: bool = False
    ) -> None:
        if isinstance(columns, str) or not columns:
            raise ConfigError("CSV columns must be a non-empty sequence of names")
        if any(not isinstance(column, str) or not column.strip() for column in columns):
            raise ConfigError("CSV columns must be non-empty strings")
        if len(set(columns)) != len(columns):
            raise ConfigError("CSV columns must be unique")
        self.path = Path(path)
        self.columns = tuple(columns)
        self.overwrite = overwrite

    def write(self, records: Iterable[Mapping[str, Any]]) -> int:
        count = 0
        with _atomic_text(self.path, self.overwrite) as handle, _managed_iterator(records) as rows:
            writer = csv.DictWriter(handle, fieldnames=self.columns)
            writer.writeheader()
            for record in rows:
                row = copy_record(record)
                if row.keys() != set(self.columns):
                    raise RecordError("CSV record fields must match the declared columns")
                if any(
                    value is not None and not isinstance(value, (str, int, float, bool))
                    for value in row.values()
                ):
                    raise RecordError("CSV values must be scalar values or None")
                writer.writerow(row)
                count += 1
        return count


class MemorySink:
    """Collect records in memory, replacing the snapshot only after a successful write."""

    def __init__(self) -> None:
        self._records: list[Record] = []

    @property
    def records(self) -> list[Record]:
        return [copy_record(row) for row in self._records]

    def write(self, records: Iterable[Mapping[str, Any]]) -> int:
        with _managed_iterator(records) as rows:
            collected = [copy_record(row) for row in rows]
        self._records = collected
        return len(self._records)
