# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""Fixtures for Cloud Workspace integration tests."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Generator

import pytest
from datarheo._util.api_util import CLOUD_API_ROOT
from datarheo._util.temp_files import as_temp_files
from datarheo._util.venv_util import get_bin_dir
from datarheo.cloud import CloudWorkspace
from datarheo.destinations.base import Destination
from datarheo.secrets.base import SecretString
from datarheo.secrets.google_gsm import GoogleGSMSecretManager
from datarheo.sources.base import Source
from datarheo.sources.util import get_source
from airbyte_api.models import (
    DestinationBigquery,
    DestinationDuckdb,
    DestinationPostgres,
    DestinationSnowflake,
)


DATARHEO_CLOUD_WORKSPACE_ID = "19d7a891-8e0e-40ac-8a8c-5faf8d11e47c"

ENV_MOTHERDUCK_API_KEY = "PYDATARHEO_MOTHERDUCK_API_KEY"
DATARHEO_CLOUD_API_KEY_SECRET_NAME = "PYDATARHEO_CLOUD_INTEROP_API_KEY"
DATARHEO_CLOUD_CREDS_SECRET_NAME = "PYDATARHEO_CLOUD_INTEROP_CREDS"


@pytest.fixture(autouse=True)
def add_venv_bin_to_path(monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch the PATH to include the virtual environment's bin directory."""
    # Get the path to the bin directory of the virtual environment
    venv_bin_path = str(get_bin_dir(Path(sys.prefix)))

    # Add the bin directory to the PATH
    new_path = f"{venv_bin_path}{os.pathsep}{os.environ['PATH']}"
    monkeypatch.setenv("PATH", new_path)


@pytest.fixture
def workspace_id() -> str:
    return DATARHEO_CLOUD_WORKSPACE_ID


@pytest.fixture
def datarheo_cloud_api_root() -> str:
    return CLOUD_API_ROOT


CloudAPICreds = tuple[SecretString, SecretString]


@pytest.fixture
def datarheo_cloud_credentials(
    ci_secret_manager: GoogleGSMSecretManager,
) -> CloudAPICreds:
    secret = ci_secret_manager.get_secret(
        DATARHEO_CLOUD_CREDS_SECRET_NAME,
    ).parse_json()
    return SecretString(secret["client_id"]), SecretString(secret["client_secret"])


@pytest.fixture
def datarheo_cloud_client_id(
    datarheo_cloud_credentials: CloudAPICreds,
) -> SecretString:
    return datarheo_cloud_credentials[0]


@pytest.fixture
def datarheo_cloud_client_secret(
    datarheo_cloud_credentials: CloudAPICreds,
) -> SecretString:
    return datarheo_cloud_credentials[1]


@pytest.fixture
def motherduck_api_key(motherduck_secrets: dict) -> SecretString:
    return SecretString(motherduck_secrets["motherduck_api_key"])


@pytest.fixture
def cloud_workspace(
    workspace_id: str,
    datarheo_cloud_api_root: str,
    datarheo_cloud_client_id: SecretString,
    datarheo_cloud_client_secret: SecretString,
) -> CloudWorkspace:
    return CloudWorkspace(
        workspace_id=workspace_id,
        api_root=datarheo_cloud_api_root,
        client_id=datarheo_cloud_client_id,
        client_secret=datarheo_cloud_client_secret,
    )


@pytest.fixture
def deployable_dummy_source(*, use_docker: bool) -> Source:
    """A local PyDataRheo `Source` object.

    For some reason `source-hardcoded-records` and `source-e2e-tests` are not working.
    """
    return get_source(
        "source-faker",
        streams=["products"],
        config={
            "count": 100,
        },
        # install_if_missing=False,
        docker_image=use_docker,
    )


@pytest.fixture
def deployable_dummy_destination(
    new_bigquery_destination: Destination,
) -> Destination:
    """A local PyDataRheo `Destination` object.

    # TODO: Use DevNullDestination instead of BigQueryDestination.
    # Problem is that 'dev-null' is not accepted on Cloud as of now.
    # Need a workaround.
    """
    return new_bigquery_destination


@pytest.fixture(scope="function")
def new_deployable_destination(
    request,
) -> (
    DestinationDuckdb | DestinationPostgres | DestinationBigquery | DestinationSnowflake
):
    """This is a placeholder fixture that will be overridden by pytest_generate_tests()."""
    return request.getfixturevalue(request.param)


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Override default pytest behavior, parameterizing our tests based on the available cache types.

    This is useful for running the same tests with different cache types, to ensure that the tests
    can pass across all cache types.
    """
    deployable_destination_fixtures: dict[str, str] = {
        # Ordered by priority (fastest first)
        # "MotherDuck": "new_motherduck_destination",
        # "Postgres": "new_remote_postgres_cache",
        "BigQuery": "new_bigquery_destination",
        "Snowflake": "new_snowflake_destination",
    }

    if "new_deployable_destination" in metafunc.fixturenames:
        metafunc.parametrize(
            "new_deployable_destination",
            deployable_destination_fixtures.values(),
            ids=deployable_destination_fixtures.keys(),
            indirect=True,
            scope="function",
        )


@pytest.fixture(scope="session")
def with_bigquery_credentials_env_vars(
    ci_secret_manager: GoogleGSMSecretManager,
) -> Generator[None, Any, None]:
    """This fixture sets up the BigQuery credentials file for the session.

    This is needed because when retrieving config from the REST API, the credentials are
    obfuscated.
    """
    dest_bigquery_config = ci_secret_manager.get_secret(
        secret_name="SECRET_DESTINATION-BIGQUERY_CREDENTIALS__CREDS"
    ).parse_json()

    credentials_json = dest_bigquery_config["credentials_json"]
    with as_temp_files(files_contents=[credentials_json]) as (credentials_path,):
        os.environ["BIGQUERY_CREDENTIALS_PATH"] = credentials_path
        os.environ["BIGQUERY_CREDENTIALS_JSON"] = json.dumps(credentials_json)

        yield

    return


@pytest.fixture(scope="session")
def snowflake_creds(ci_secret_manager: GoogleGSMSecretManager) -> dict:
    return ci_secret_manager.get_secret(
        "DATARHEO_LIB_SNOWFLAKE_CREDS",
    ).parse_json()


@pytest.fixture(scope="session")
def with_snowflake_password_env_var(snowflake_creds: dict):
    """This fixture sets up Snowflake credentials for tests.

    This is needed because when retrieving config from the REST API, the credentials are
    obfuscated.
    """
    os.environ["SNOWFLAKE_PASSWORD"] = snowflake_creds["password"]

    yield

    return
