"""The lightweight public API must not eagerly import the optional connector runtime."""

import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from pydatarheo import (
    ConfigError,
    ConnectorDependencyError,
    compat,
    get_destination,
    get_source,
)


def test_bridge_dunder_lookup_does_not_import_runtime(monkeypatch):
    loader = Mock(side_effect=AssertionError("unexpected import"))
    monkeypatch.setattr(compat, "import_module", loader)
    with pytest.raises(AttributeError):
        getattr(compat, "__path__")
    loader.assert_not_called()


def test_bridge_missing_dependency_has_install_instructions(monkeypatch):
    def missing(name):
        raise ModuleNotFoundError("missing", name="airbyte_cdk")

    monkeypatch.setattr(compat, "import_module", missing)
    with pytest.raises(ConnectorDependencyError, match=r"\[connectors\]"):
        get_source("source-faker", config={"count": 2})


def test_bridge_source_preserves_configuration_and_options(monkeypatch):
    factory = Mock(return_value=object())
    monkeypatch.setattr(
        compat, "import_module", lambda name: SimpleNamespace(get_source=factory)
    )
    config = {"count": 3}
    result = get_source(
        "source-faker",
        config=config,
        version="0.1.0",
        streams=["users"],
        install_if_missing=False,
    )
    assert result is factory.return_value
    factory.assert_called_once_with(
        "source-faker",
        config=config,
        version="0.1.0",
        streams=["users"],
        install_if_missing=False,
    )


def test_bridge_destination_preserves_options(monkeypatch):
    factory = Mock(return_value=object())
    monkeypatch.setattr(
        compat, "import_module", lambda name: SimpleNamespace(get_destination=factory)
    )
    assert get_destination("destination-test", config={}) is factory.return_value
    factory.assert_called_once_with("destination-test", config={})


def test_bridge_named_export_delegates_without_changing_identity(monkeypatch):
    cache = object()
    monkeypatch.setattr(
        compat, "import_module", lambda name: SimpleNamespace(DuckDBCache=cache)
    )
    assert compat.DuckDBCache is cache


def test_native_unknown_options_are_not_silently_ignored():
    with pytest.raises(ConfigError):
        get_source("memory", config={"records": []}, typo=True)


def test_native_missing_config_reports_required_field():
    with pytest.raises(ConfigError):
        get_source("memory")


def test_bridge_import_does_not_load_databases_in_fresh_process():
    import subprocess

    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "import sys, pydatarheo; assert 'datarheo' not in sys.modules; assert 'duckdb' not in sys.modules",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
