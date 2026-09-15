# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""PyDataRheo classes and methods for interacting with the hosted cloud API.

You can use this module to interact with managed Cloud, OSS, and Enterprise deployments.

## Self-managed instances

For self-managed instances, set `api_root` to the Public API root for your
deployment. For the default self-managed route, that usually ends in `/api/public/v1`.
PyDataRheo uses the Public API for workspace and organization discovery.

Some Cloud module methods also call the Config API, including methods such as
`CloudConnection.dump_raw_catalog()`, which reads the configured catalog directly
from the deployment. For documented self-managed deployments where the Public API root ends in
`/api/public/v1`, PyDataRheo infers the Config API root by replacing that suffix with
`/api/v1`.

If your deployment uses custom ingress or a nonstandard reverse proxy, pass
`config_api_root` explicitly or set the `DATARHEO_CLOUD_CONFIG_API_URL` environment
variable.

```python
from datarheo import cloud

workspace = cloud.CloudWorkspace(
    workspace_id="...",
    client_id="...",
    client_secret="...",
    api_root="https://airbyte.example.com/api/public/v1",
    config_api_root="https://airbyte.example.com/api/v1",
)

connection = workspace.get_connection(connection_id="...")
raw_catalog = connection.dump_raw_catalog()
```

## Examples

### Basic Sync Example:

```python
import datarheo as dr
from datarheo import cloud

# Initialize a cloud workspace object
workspace = cloud.CloudWorkspace(
    workspace_id="123",
    api_key=dr.get_secret("DATARHEO_CLOUD_API_KEY"),
)

# Run a sync job on the cloud
connection = workspace.get_connection(connection_id="456")
sync_result = connection.run_sync()
print(sync_result.get_job_status())
```

### Example Read From Cloud Destination:

If your destination is supported, you can read records directly from the
`SyncResult` object. Currently this is supported in Snowflake and BigQuery only.


```python
# Assuming we've already created a `connection` object...

# Get the latest job result and print the stream names
sync_result = connection.get_sync_result()
print(sync_result.stream_names)

# Get a dataset from the sync result
dataset: CachedDataset = sync_result.get_dataset("users")

# Get a SQLAlchemy table to use in SQL queries...
users_table = dataset.to_sql_table()
print(f"Table name: {users_table.name}")

# Or iterate over the dataset directly
for record in dataset:
    print(record)
```
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from datarheo.cloud.client import CloudClient
from datarheo.cloud.client_config import CloudClientConfig
from datarheo.cloud.connections import CloudConnection
from datarheo.cloud.models import (
    CloudDefaultContextInfo,
    CloudWorkspaceInfo,
    JobStatusEnum,
    JobTypeEnum,
    WorkspacePrivilegeScope,
)
from datarheo.cloud.organizations import CloudOrganization
from datarheo.cloud.sync_results import SyncResult
from datarheo.cloud.workspaces import CloudWorkspace

# Submodules imported here for documentation reasons: https://github.com/mitmproxy/pdoc/issues/757
if TYPE_CHECKING:
    # ruff: noqa: TC004
    from datarheo.cloud import (
        client,
        client_config,
        connections,
        constants,
        organizations,
        sync_results,
        workspaces,
    )


__all__ = [
    # Submodules
    "workspaces",
    "client",
    "organizations",
    "connections",
    "constants",
    "client_config",
    "sync_results",
    # Classes
    "CloudClient",
    "CloudOrganization",
    "CloudWorkspace",
    "CloudConnection",
    "CloudClientConfig",
    "CloudDefaultContextInfo",
    "CloudWorkspaceInfo",
    "SyncResult",
    # Enums
    "JobStatusEnum",
    "JobTypeEnum",
    "WorkspacePrivilegeScope",
]
