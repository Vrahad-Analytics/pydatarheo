"""Built-in connectors; none require downloads or services."""

from pydatarheo.connectors.files import CsvSource, JsonlSource
from pydatarheo.connectors.memory import MemorySource

__all__ = ["CsvSource", "JsonlSource", "MemorySource"]
