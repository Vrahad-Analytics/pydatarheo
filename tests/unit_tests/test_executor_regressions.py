"""Regression tests for actual connector identifiers and explicit manifest URLs."""

from unittest.mock import Mock

import pytest

from datarheo._executors import util
from datarheo.registry import ConnectorMetadata, InstallType, Language


@pytest.fixture
def connector_metadata(monkeypatch, tmp_path):
    metadata = ConnectorMetadata(
        name="source-example",
        latest_available_version="1.2.3",
        pypi_package_name=None,
        language=Language.JAVA,
        install_types={InstallType.DOCKER},
        docker_repository="publisher/source-example",
    )
    monkeypatch.setattr(util, "get_connector_metadata", lambda name: metadata)
    monkeypatch.setattr(util, "DEFAULT_PROJECT_DIR", tmp_path)
    return metadata


def test_docker_default_image_uses_publisher_metadata(connector_metadata):
    executor = util.get_connector_executor(
        "source-example", docker_image=True, version="1.2.3"
    )
    assert executor.image_name_full == "publisher/source-example:1.2.3"


def test_manifest_downloads_have_bounded_network_timeouts(monkeypatch):
    manifest = Mock(status_code=200, text="type: DeclarativeSource\nstreams: []")
    manifest.raise_for_status.return_value = None
    components = Mock(status_code=404)
    get = Mock(side_effect=[manifest, components])
    monkeypatch.setattr(util.requests, "get", get)
    util._try_get_manifest_connector_files("source-example", "1.2.3")
    assert all(call.kwargs.get("timeout") for call in get.call_args_list)


def test_explicit_manifest_url_is_used_instead_of_registry_url(
    monkeypatch, connector_metadata
):
    get = Mock(
        return_value=Mock(text="type: DeclarativeSource\nstreams: []", status_code=200)
    )
    monkeypatch.setattr(util.requests, "get", get)
    factory = Mock(return_value=object())
    monkeypatch.setattr(util, "DeclarativeExecutor", factory)
    url = "https://example.com/custom/manifest.yaml"
    assert (
        util.get_connector_executor("source-example", source_manifest=url)
        is factory.return_value
    )
    get.assert_called_once()
    assert (
        get.call_args.kwargs.get(
            "url", get.call_args.args[0] if get.call_args.args else None
        )
        == url
    )
    assert get.call_args.kwargs["timeout"]
    assert factory.call_args.kwargs["manifest"]["type"] == "DeclarativeSource"
