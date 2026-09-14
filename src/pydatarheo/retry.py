"""Bounded retries for explicitly idempotent operations, never whole record iterators."""

from __future__ import annotations

import logging
import math
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from pydatarheo.exceptions import ConfigError, TransientError

T = TypeVar("T")
logger = logging.getLogger("pydatarheo.retry")


@dataclass(frozen=True)
class RetryPolicy:
    """Total attempts and capped exponential delay in seconds."""

    max_attempts: int = 3
    initial_delay: float = 0.1
    max_delay: float = 5.0

    def __post_init__(self) -> None:
        if type(self.max_attempts) is not int or self.max_attempts < 1:
            raise ConfigError("max_attempts must be a positive integer")
        for delay in (self.initial_delay, self.max_delay):
            if isinstance(delay, bool) or not isinstance(delay, (int, float)):
                raise ConfigError("Retry delays must be finite non-negative numbers")
            if not math.isfinite(delay) or delay < 0:
                raise ConfigError("Retry delays must be finite non-negative numbers")
        if self.initial_delay > self.max_delay:
            raise ConfigError("initial_delay cannot exceed max_delay")


def retry(
    operation: Callable[[], T],
    *,
    policy: RetryPolicy | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> T:
    """Retry only TransientError. The caller guarantees the operation is safe to repeat."""
    policy = policy if policy is not None else RetryPolicy()
    delay = policy.initial_delay
    for attempt in range(1, policy.max_attempts + 1):
        try:
            return operation()
        except TransientError:
            if attempt == policy.max_attempts:
                raise
            logger.debug("Retrying operation after attempt %d", attempt)
            sleep(delay)
            delay = min(policy.max_delay, delay * 2)
    raise AssertionError("Unreachable with a valid retry policy")
