# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""
Usage:
    poetry install
    poetry run python examples/run_bigquery_destination.py
"""

from __future__ import annotations

import tempfile
import warnings

import datarheo as dr
from datarheo.secrets.google_gsm import GoogleGSMSecretManager


warnings.filterwarnings("ignore", message="Cannot create BigQuery Storage client")


DATARHEO_INTERNAL_GCP_PROJECT = "dataline-integration-testing"
SECRET_NAME = "SECRET_DESTINATION-BIGQUERY_CREDENTIALS__CREDS"

bigquery_destination_secret: dict = (
    GoogleGSMSecretManager(  # type: ignore[union-attr]
        project=DATARHEO_INTERNAL_GCP_PROJECT,
        credentials_json=dr.get_secret("GCP_GSM_CREDENTIALS"),
    )
    .get_secret(SECRET_NAME)
    .parse_json()
)


def main() -> None:
    source = dr.get_source(
        "source-faker",
        config={"count": 1000, "seed": 0, "parallelism": 1, "always_updated": False},
        install_if_missing=True,
    )
    source.check()
    source.select_all_streams()

    with tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8") as temp:
        # Write credentials to the temp file
        temp.write(bigquery_destination_secret["credentials_json"])
        temp.flush()
        temp.close()

        destination = dr.get_destination(
            "destination-bigquery",
            config={**bigquery_destination_secret, "dataset_id": "pydatarheo_tests"},
        )
        write_result = destination.write(
            source,
            # cache=False,  # Toggle comment to test with/without caching
        )


if __name__ == "__main__":
    main()
