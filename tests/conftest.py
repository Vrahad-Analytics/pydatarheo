"""Shared, isolated sample data; no network services or credentials."""

import functools
import json
import os
import sys
from pathlib import Path

import pytest


@functools.lru_cache(maxsize=1)
def _docker_daemon_available():
    import subprocess

    try:
        return (
            subprocess.run(
                ["docker", "info"], capture_output=True, timeout=10
            ).returncode
            == 0
        )
    except Exception:
        return False


@pytest.fixture
def records():
    return [
        {"id": 1, "name": "Ada", "amount": 10},
        {"id": 2, "name": "Lin", "amount": 20},
    ]


@pytest.fixture
def jsonl_path(tmp_path, records):
    path = tmp_path / "records.jsonl"
    path.write_text(
        "\n".join(json.dumps(row) for row in records) + "\n", encoding="utf-8"
    )
    return path


@pytest.fixture
def csv_path(tmp_path):
    path = tmp_path / "records.csv"
    path.write_text("id,name,amount\n1,Ada,10\n2,Lin,20\n", encoding="utf-8")
    return path


def pytest_addoption(parser):
    parser.addoption(
        "--run-compatibility",
        action="store_true",
        help="Run retained connector tests; requires connectors and test-connectors extras",
    )
    parser.addoption(
        "--run-live",
        action="store_true",
        help="Enable explicitly provisioned external-service tests",
    )


def pytest_ignore_collect(collection_path, config):
    retained = {"unit_tests", "integration_tests", "docs_tests", "lint_tests"}
    if collection_path.name in retained and not config.getoption("--run-compatibility"):
        return True
    return None


def pytest_report_header(config):
    if not config.getoption("--run-compatibility"):
        return "Retained connector tests require --run-compatibility and the connectors,test-connectors extras"
    return "Retained connector compatibility tests enabled; live services require --run-live"


def pytest_collection_modifyitems(config, items):
    for item in items:
        if "unit_tests" in item.path.parts or "integration_tests" in item.path.parts:
            item.add_marker(pytest.mark.compatibility)
        if "integration_tests" in item.path.parts:
            item.add_marker(pytest.mark.integration)
        requires_live = (
            item.get_closest_marker("requires_creds")
            or "ci_secret_manager" in item.fixturenames
        )
        if (
            requires_live or item.get_closest_marker("super_slow")
        ) and not config.getoption("--run-live"):
            item.add_marker(
                pytest.mark.skip(
                    reason="External credentials/services not provisioned; use --run-live explicitly"
                )
            )
        requires_docker = (
            item.path.name == "test_docker_executable.py"
            or item.path.name == "test_source_to_destination.py"
            or "e2e_test_destination" in item.fixturenames
        )
        if requires_docker and not _docker_daemon_available():
            item.add_marker(pytest.mark.skip(reason="Docker daemon not available"))


@pytest.fixture
def source_test_registry(monkeypatch):
    import datarheo.registry as registry

    path = Path(__file__).parent / "integration_tests/fixtures/registry.json"
    monkeypatch.setattr(registry, "_get_registry_url", lambda: str(path))
    monkeypatch.setattr(registry, "__cache", None)


@pytest.fixture
def new_duckdb_cache(tmp_path):
    from datarheo.caches.util import new_local_cache

    return new_local_cache(cache_dir=tmp_path / "cache")


@pytest.fixture
def use_docker():
    return False


@pytest.fixture(autouse=True)
def disable_tracking(monkeypatch):
    monkeypatch.setenv("DO_NOT_TRACK", "true")


@pytest.fixture(autouse=True)
def isolated_compatibility_paths(request, monkeypatch, tmp_path):
    if not ({"unit_tests", "integration_tests"} & set(request.node.path.parts)):
        return
    from datarheo import constants, logs
    from datarheo.caches import util as cache_util

    monkeypatch.setattr(constants, "DEFAULT_CACHE_ROOT", tmp_path / "cache")
    monkeypatch.setattr(cache_util, "DEFAULT_CACHE_ROOT", tmp_path / "cache")
    monkeypatch.setattr(logs, "DATARHEO_LOGGING_ROOT", tmp_path / "logs")
    monkeypatch.setenv("DATARHEO_CACHE_ROOT", str(tmp_path / "cache"))
    if hasattr(request.module, "UNIT_TEST_DB_PATH"):
        monkeypatch.setattr(
            request.module, "UNIT_TEST_DB_PATH", tmp_path / "test_db.duckdb"
        )


@pytest.fixture(scope="session", params=[True, False], ids=["uv", "pip"])
def source_test_installation(request, tmp_path_factory):
    import datarheo.registry as registry
    from datarheo._executors import python as executor_module
    from datarheo._executors.python import VenvExecutor

    patches = pytest.MonkeyPatch()
    root = tmp_path_factory.mktemp("connector-install")
    package = Path(__file__).parent / "integration_tests/fixtures/source-test"
    patches.setenv("DATARHEO_LOCAL_REGISTRY", str(package.parent / "registry.json"))
    patches.setattr(registry, "__cache", None)
    patches.setattr(executor_module, "DEFAULT_INSTALL_DIR", root)
    patches.setattr(executor_module, "NO_UV", not request.param)
    patches.setenv(
        "PATH",
        f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}",
    )
    executor = VenvExecutor(
        name="source-test",
        pip_url=str(package),
        install_root=root,
        use_python=Path(sys.executable),
    )
    try:
        executor.install()
        yield executor
    finally:
        patches.undo()


@pytest.fixture
def source_test_env(source_test_installation):
    return source_test_installation


@pytest.fixture
def new_postgres_cache():
    pytest.skip(
        "PostgreSQL service not provisioned; no existing containers will be modified"
    )
