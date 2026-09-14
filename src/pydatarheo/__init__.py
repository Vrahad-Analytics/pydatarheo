"""pydatarheo: Vrahad Analytics' native Python connector framework."""

from importlib.metadata import version

from pydatarheo.config import Config
from pydatarheo.connectors import CsvSource, JsonlSource, MemorySource
from pydatarheo.core import Record, Source, Stream, transform_records
from pydatarheo.exceptions import (
    ConfigError,
    DatarheoError,
    RecordError,
    SinkError,
    SourceError,
    TransientError,
)
from pydatarheo.registry import SourceRegistry, builtin_registry, get_source
from pydatarheo.retry import RetryPolicy, retry
from pydatarheo.sinks import CsvSink, JsonlSink, MemorySink

__version__ = version("pydatarheo")

__all__ = [
    "Config",
    "ConfigError",
    "CsvSink",
    "CsvSource",
    "DatarheoError",
    "JsonlSink",
    "JsonlSource",
    "MemorySink",
    "MemorySource",
    "Record",
    "RecordError",
    "RetryPolicy",
    "SinkError",
    "Source",
    "SourceError",
    "SourceRegistry",
    "Stream",
    "TransientError",
    "__version__",
    "builtin_registry",
    "get_source",
    "retry",
    "transform_records",
]
