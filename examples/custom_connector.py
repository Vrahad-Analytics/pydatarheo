"""Register a native source and consume bounded batches without external SDKs."""

from collections.abc import Iterator, Mapping
from typing import Any

from pydatarheo import Config, ConfigError, Record, Source, SourceRegistry, Stream


class CounterSource(Source):
    """Generate a configured number of records without holding them all in memory."""

    def __init__(self, config: Mapping[str, Any]) -> None:
        settings = Config(config)
        settings.only("count")
        self.count = settings.require("count", int)
        if type(self.count) is not int or self.count < 0:
            raise ConfigError("count must be a non-negative integer")

    def streams(self) -> tuple[Stream, ...]:
        return (Stream("numbers"),)

    def _read_stream(self, stream: str) -> Iterator[Record]:
        # A real connector would open its resource here and close it in a finally/with block.
        for number in range(self.count):
            yield {"number": number}


def main() -> None:
    # Each registry belongs to the application; there is no global plugin mutation.
    registry = SourceRegistry()
    registry.register("counter", CounterSource)
    source = registry.create("counter", {"count": 5})
    source.check()
    # Batching uses the same stream and retains the final partial batch.
    for batch in source.read_batches("numbers", batch_size=2):
        print(batch)


if __name__ == "__main__":
    main()
