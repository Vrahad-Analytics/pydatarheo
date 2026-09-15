"""Public exception boundaries for connector applications."""


class DatarheoError(Exception):
    """Base error raised by the framework."""


class ConfigError(DatarheoError, ValueError):
    """Invalid connector configuration or stream selection."""


class RecordError(DatarheoError, ValueError):
    """A record does not satisfy the mapping or serialization contract."""


class SourceError(DatarheoError):
    """The source could not be opened or decoded."""


class SinkError(DatarheoError):
    """The sink could not publish its output."""


class TransientError(DatarheoError):
    """An operation may safely be retried by its caller."""
