"""Handle transient failures safely; simulate an idempotent request without a network."""

import logging

from pydatarheo import DatarheoError, RetryPolicy, TransientError, retry


def main() -> None:
    # Applications own logging. The library never configures the root logger.
    logging.basicConfig(level=logging.DEBUG, format="%(name)s: %(message)s")
    attempts = 0

    def fetch_page():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            # Only mark errors transient when repeating the operation is safe.
            raise TransientError("Simulated temporary unavailability")
        return [{"id": 1}]

    try:
        # Retry a complete page before yielding any of its records, not an entire stream.
        rows = retry(fetch_page, policy=RetryPolicy(max_attempts=3, initial_delay=0))
    except DatarheoError:
        print("Request failed; no records were emitted")
        raise
    print(f"Fetched {len(rows)} record after {attempts} attempts")


if __name__ == "__main__":
    main()
