# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""PyDataRheo classes and methods for the agents platform.

> ## ⚠️ Experimental Interface
>
> **The agents Python interfaces are experimental.** Class names, method signatures,
> and result models may change or be removed without notice between minor versions of
> PyDataRheo. Pin an exact PyDataRheo version if you depend on them.

Agents connectors expose read and write actions on individual entities, executed
one action at a time, rather than the batch record replication that `datarheo.cloud`
provides. This module is that interface.

Cloud credentials authenticate against the Agents API, so no Agents-specific
credentials or environment variables exist: the `DATARHEO_CLOUD_*` variables are reused.

## Usage Examples

Read entities from a connector, paging automatically as you iterate:

```python
from datarheo import agents

workspace = agents.AgentWorkspace.from_env()
connector = workspace.get_connector("GitHub")  # by ID or name (case insensitive)

for issue in connector.iter_entities(
    "issues",
    api_args={"repository": "Vrahad-Analytics/pydatarheo"},  # Passthrough API args
):
    print(issue["title"])
```

Fetch a single page instead, when the result's status and metadata are needed:

```python
result = connector.list_entities(
    "issues",
    api_args={"repository": "Vrahad-Analytics/pydatarheo"},
    page_size=50,
)
print(result.status, result.has_next_page)
for entity in result.entities:
    print(entity["title"])
```

Pass `result.end_cursor` back as `cursor` to page through manually:

```python
cursor = None
while True:
    result = connector.list_entities(
        "issues",
        api_args={"repository": "Vrahad-Analytics/pydatarheo"},
        cursor=cursor,
    )
    print(len(result.entities))
    if not result.has_next_page:
        break
    cursor = result.end_cursor
```

Discover what a connector supports, and what an organization can reach:

```python
organization = agents.AgentOrganization.from_env()
for workspace in organization.list_workspaces():
    print(workspace.workspace_id, workspace.name)

print(connector.inspect().source_definition_name)
```

Convert between the Cloud and Agents domains:

```python
from datarheo.cloud import CloudWorkspace

cloud_workspace = CloudWorkspace.from_env()
agent_workspace = agents.AgentWorkspace.from_cloud_workspace(cloud_workspace)
back_to_cloud = agent_workspace.as_cloud_workspace()
```
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from datarheo.agents.connectors import AgentConnector
from datarheo.agents.models import (
    AgentConnectorDetails,
    AgentConnectorInfo,
    AgentConnectorMetadata,
    AgentContextStoreEntity,
    AgentContextStoreReadiness,
    AgentExecuteResult,
    AgentExecutionMetadata,
    AgentWorkspaceInfo,
)
from datarheo.agents.organizations import AgentOrganization
from datarheo.agents.workspaces import AgentWorkspace

# Submodules imported here for documentation reasons: https://github.com/mitmproxy/pdoc/issues/757
if TYPE_CHECKING:
    # ruff: noqa: TC004
    from datarheo.agents import (
        connectors,
        models,
        organizations,
        workspaces,
    )


__all__ = [
    # Submodules
    "connectors",
    "models",
    "organizations",
    "workspaces",
    # Classes
    "AgentConnector",
    "AgentConnectorDetails",
    "AgentConnectorInfo",
    "AgentConnectorMetadata",
    "AgentContextStoreEntity",
    "AgentContextStoreReadiness",
    "AgentExecuteResult",
    "AgentExecutionMetadata",
    "AgentOrganization",
    "AgentWorkspace",
    "AgentWorkspaceInfo",
]
