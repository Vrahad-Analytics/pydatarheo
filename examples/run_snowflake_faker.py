# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""
Usage:
    poetry install
    poetry run python examples/run_snowflake_faker.py
"""

from __future__ import annotations

import datarheo as dr
from datarheo.caches import SnowflakeCache
from datarheo.secrets.google_gsm import GoogleGSMSecretManager


SCALE = 10_000


DATARHEO_INTERNAL_GCP_PROJECT = "dataline-integration-testing"
secret_mgr = GoogleGSMSecretManager(
    project=DATARHEO_INTERNAL_GCP_PROJECT,
    credentials_json=dr.get_secret("GCP_GSM_CREDENTIALS"),
)

secret = secret_mgr.get_secret(
    secret_name="DATARHEO_LIB_SNOWFLAKE_CREDS",
)
assert secret is not None, "Secret not found."
secret_config = secret.parse_json()


cache = SnowflakeCache(
    account=secret_config["account"],
    username=secret_config["username"],
    password=secret_config["password"],
    database=secret_config["database"],
    warehouse=secret_config["warehouse"],
    role=secret_config["role"],
)

source = dr.get_source(
    "source-faker",
    config={
        "count": SCALE,
    },
    install_if_missing=True,
    streams="*",
)
source.check()

result = source.read(cache)

for name in ["products"]:
    print(f"Stream {name}: {len(list(result[name]))} records")
