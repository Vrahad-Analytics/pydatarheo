"""Isolated registration and retry boundaries."""

import pytest

from pydatarheo import (
    ConfigError,
    MemorySource,
    RetryPolicy,
    SourceRegistry,
    TransientError,
    builtin_registry,
    get_source,
    retry,
)


def test_registry_custom_factory_returns_source(records):
    registry = SourceRegistry()
    registry.register("custom", MemorySource)
    assert list(registry.create("custom", {"records": records}).read()) == records
    assert registry.available() == ("custom",)
    assert SourceRegistry().available() == ()


def test_registry_duplicate_name_raises_config_error():
    registry = builtin_registry()
    with pytest.raises(ConfigError):
        registry.register("memory", MemorySource)
    assert builtin_registry().available() == ("csv", "jsonl", "memory")


@pytest.mark.parametrize(
    "name,factory", [("", MemorySource), (1, MemorySource), ("bad", None)]
)
def test_registry_invalid_registration_raises_config_error(name, factory):
    with pytest.raises(ConfigError):
        SourceRegistry().register(name, factory)


def test_registry_invalid_factory_result_raises_config_error():
    registry = SourceRegistry()
    registry.register("bad", lambda config: None)
    with pytest.raises(ConfigError):
        registry.create("bad", {})


def test_registry_unknown_name_raises_without_downloading():
    with pytest.raises(ConfigError):
        get_source("unknown", config={})


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_attempts": 0},
        {"max_attempts": True},
        {"initial_delay": -1},
        {"max_delay": float("inf")},
        {"initial_delay": float("nan")},
        {"initial_delay": True},
        {"max_delay": "1"},
        {"initial_delay": 6},
    ],
)
def test_retry_invalid_policy_raises_config_error(kwargs):
    with pytest.raises(ConfigError):
        RetryPolicy(**kwargs)


def test_retry_transient_failure_backs_off_and_succeeds(caplog):
    attempts = []
    delays = []

    def operation():
        attempts.append(1)
        if len(attempts) < 4:
            raise TransientError("private value")
        return "ok"

    with caplog.at_level("DEBUG", logger="pydatarheo.retry"):
        result = retry(operation, policy=RetryPolicy(4, 0.1, 0.15), sleep=delays.append)
    assert result == "ok"
    assert delays == [0.1, 0.15, 0.15]
    assert "private value" not in caplog.text


def test_retry_exhausted_attempts_reraises_original_error():
    error = TransientError("temporary")
    attempts = []

    def operation():
        attempts.append(1)
        raise error

    with pytest.raises(TransientError) as caught:
        retry(operation, policy=RetryPolicy(2, 0, 0), sleep=lambda delay: None)
    assert caught.value is error
    assert len(attempts) == 2


def test_retry_permanent_error_does_not_retry():
    attempts = []

    def operation():
        attempts.append(1)
        raise ValueError("permanent")

    with pytest.raises(ValueError):
        retry(operation)
    assert len(attempts) == 1


def test_retry_success_returns_without_sleeping():
    delays = []
    assert retry(lambda: 42, sleep=delays.append) == 42
    assert delays == []
