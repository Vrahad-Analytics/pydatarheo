# interactive module

MCP primitives registered by the `interactive` module of the `datarheo-mcp` server: **3** tool(s), **0** prompt(s), **0** resource(s).

## Tools (3)

<a id="show_connection_sync_history"></a>

### show_connection_sync_history

**Hints:** `read-only` · `idempotent` · `open-world`

**Availability:** requires an MCP Apps UI-capable client (declares the `io.modelcontextprotocol/ui` extension).

Show interactive sync history dashboard for a cloud connection.

    Renders a rich UI with metrics (success rate, total records, total bytes),
    charts (success/fail by date, records over time, bytes over time), and
    a detailed job history table.
    

When connecting to a hosted MCP server, provide a bearer token via the `Authorization` header, or client credentials via the transport `Client-Id` and `Client-Secret` headers. When no workspace ID is provided, the authenticated user's default workspace (and its organization) is used automatically. Call `get_default_cloud_context` to inspect the resolved context. To discover other workspaces, call `list_cloud_workspaces` with an organization ID or broader privilege scope. Only call `list_cloud_organizations` when you need to search organizations by name, passing `name_contains`. For local or stdio connections, set the `DATARHEO_CLOUD_BEARER_TOKEN` environment variable, or both `DATARHEO_CLOUD_CLIENT_ID` and `DATARHEO_CLOUD_CLIENT_SECRET`. If discovery returns multiple candidates, ask the user to choose one; do not select automatically.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `connection_id` | `string` | yes | — | The ID of the cloud connection to show sync history for. |
| `workspace_id` | `string \| null` | no | `null` | Workspace ID. Hosted MCP connections pass it via the `X-DataRheo-Workspace-Id` header; local or stdio connections use the `DATARHEO_CLOUD_WORKSPACE_ID` environment variable. |
| `max_jobs` | `integer` | no | `30` | Maximum number of recent sync jobs to display. Defaults to 30. Maximum allowed value is 100. |
| `agent_context` | `enum("verbose", "summary", "min")` | no | `"min"` | Controls how much context is returned to the agent in the text response. 'verbose': full job-level data for detailed follow-up analysis. 'summary': aggregates and key observations only. 'min': one-liner confirmation that the dashboard rendered. |
| `suppress_ui` | `boolean` | no | `false` | If True, skip rendering the visual dashboard and return only the agent text response. Use this for follow-up data retrieval without re-rendering the UI that the user has already seen. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "connection_id": {
      "description": "The ID of the cloud connection to show sync history for.",
      "type": "string"
    },
    "workspace_id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Workspace ID. Hosted MCP connections pass it via the `X-DataRheo-Workspace-Id` header; local or stdio connections use the `DATARHEO_CLOUD_WORKSPACE_ID` environment variable."
    },
    "max_jobs": {
      "default": 30,
      "description": "Maximum number of recent sync jobs to display. Defaults to 30. Maximum allowed value is 100.",
      "maximum": 100,
      "minimum": 1,
      "type": "integer"
    },
    "agent_context": {
      "default": "min",
      "description": "Controls how much context is returned to the agent in the text response. 'verbose': full job-level data for detailed follow-up analysis. 'summary': aggregates and key observations only. 'min': one-liner confirmation that the dashboard rendered.",
      "enum": [
        "verbose",
        "summary",
        "min"
      ],
      "type": "string"
    },
    "suppress_ui": {
      "default": false,
      "description": "If True, skip rendering the visual dashboard and return only the agent text response. Use this for follow-up data retrieval without re-rendering the UI that the user has already seen.",
      "type": "boolean"
    }
  },
  "required": [
    "connection_id"
  ],
  "type": "object"
}
```

</details>

<a id="show_connectors_list"></a>

### show_connectors_list

**Hints:** `read-only` · `idempotent` · `open-world`

**Availability:** requires an MCP Apps UI-capable client (declares the `io.modelcontextprotocol/ui` extension).

Show an interactive public connector catalog from the OSS registry.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `support_level` | `string` | no | `""` | Exact support level to match, such as `certified`, `community`, or `archived`. Empty string means no filter. |
| `certified` | `boolean` | no | `false` | When `True`, return only certified connectors. Shorthand for `support_level='certified'`. |
| `min_support_level` | `string` | no | `""` | Minimum support level threshold. Levels: `archived` < `community` < `certified`. Empty string means no filter. |
| `connector_type` | `string` | no | `""` | Filter by connector type: `source` or `destination`. Empty string means no filter. |
| `search` | `string` | no | `""` | Case-insensitive search across connector name, display name, definition ID, Docker repository, subtype, and docs URL. |
| `limit` | `integer` | no | `0` | Maximum number of connectors to return. Use `0` for no limit. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "support_level": {
      "default": "",
      "description": "Exact support level to match, such as `certified`, `community`, or `archived`. Empty string means no filter.",
      "type": "string"
    },
    "certified": {
      "default": false,
      "description": "When `True`, return only certified connectors. Shorthand for `support_level='certified'`.",
      "type": "boolean"
    },
    "min_support_level": {
      "default": "",
      "description": "Minimum support level threshold. Levels: `archived` < `community` < `certified`. Empty string means no filter.",
      "type": "string"
    },
    "connector_type": {
      "default": "",
      "description": "Filter by connector type: `source` or `destination`. Empty string means no filter.",
      "type": "string"
    },
    "search": {
      "default": "",
      "description": "Case-insensitive search across connector name, display name, definition ID, Docker repository, subtype, and docs URL.",
      "type": "string"
    },
    "limit": {
      "default": 0,
      "description": "Maximum number of connectors to return. Use `0` for no limit.",
      "minimum": 0,
      "type": "integer"
    }
  },
  "type": "object"
}
```

</details>

<a id="show_workspace_sync_status"></a>

### show_workspace_sync_status

**Hints:** `read-only` · `idempotent` · `open-world`

**Availability:** requires an MCP Apps UI-capable client (declares the `io.modelcontextprotocol/ui` extension).

Show an interactive sync status dashboard for a cloud workspace.

When connecting to a hosted MCP server, provide a bearer token via the `Authorization` header, or client credentials via the transport `Client-Id` and `Client-Secret` headers. When no workspace ID is provided, the authenticated user's default workspace (and its organization) is used automatically. Call `get_default_cloud_context` to inspect the resolved context. To discover other workspaces, call `list_cloud_workspaces` with an organization ID or broader privilege scope. Only call `list_cloud_organizations` when you need to search organizations by name, passing `name_contains`. For local or stdio connections, set the `DATARHEO_CLOUD_BEARER_TOKEN` environment variable, or both `DATARHEO_CLOUD_CLIENT_ID` and `DATARHEO_CLOUD_CLIENT_SECRET`. If discovery returns multiple candidates, ask the user to choose one; do not select automatically.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `workspace_id` | `string \| null` | no | `null` | Workspace ID. Hosted MCP connections pass it via the `X-DataRheo-Workspace-Id` header; local or stdio connections use the `DATARHEO_CLOUD_WORKSPACE_ID` environment variable. |
| `max_connections` | `integer` | no | `50` | Maximum number of workspace connections to inspect. Defaults to 50. Maximum allowed value is 100. |
| `max_jobs_per_connection` | `integer` | no | `5` | Maximum number of recent jobs to inspect for each connection. Defaults to 5. Maximum allowed value is 10. |
| `recent_hours` | `integer` | no | `24` | Window, in hours, used for the Recently Synced metric. Defaults to 24. |
| `agent_context` | `enum("verbose", "summary", "min")` | no | `"min"` | Controls how much context is returned to the agent in the text response. 'verbose': capped connection-level data for follow-up analysis. 'summary': aggregates and key observations only. 'min': one-liner confirmation that the dashboard rendered. |
| `suppress_ui` | `boolean` | no | `false` | If True, skip rendering the visual dashboard and return only the agent text response. Use this for follow-up data retrieval without re-rendering the UI that the user has already seen. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "workspace_id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Workspace ID. Hosted MCP connections pass it via the `X-DataRheo-Workspace-Id` header; local or stdio connections use the `DATARHEO_CLOUD_WORKSPACE_ID` environment variable."
    },
    "max_connections": {
      "default": 50,
      "description": "Maximum number of workspace connections to inspect. Defaults to 50. Maximum allowed value is 100.",
      "maximum": 100,
      "minimum": 1,
      "type": "integer"
    },
    "max_jobs_per_connection": {
      "default": 5,
      "description": "Maximum number of recent jobs to inspect for each connection. Defaults to 5. Maximum allowed value is 10.",
      "maximum": 10,
      "minimum": 1,
      "type": "integer"
    },
    "recent_hours": {
      "default": 24,
      "description": "Window, in hours, used for the Recently Synced metric. Defaults to 24.",
      "maximum": 720,
      "minimum": 1,
      "type": "integer"
    },
    "agent_context": {
      "default": "min",
      "description": "Controls how much context is returned to the agent in the text response. 'verbose': capped connection-level data for follow-up analysis. 'summary': aggregates and key observations only. 'min': one-liner confirmation that the dashboard rendered.",
      "enum": [
        "verbose",
        "summary",
        "min"
      ],
      "type": "string"
    },
    "suppress_ui": {
      "default": false,
      "description": "If True, skip rendering the visual dashboard and return only the agent text response. Use this for follow-up data retrieval without re-rendering the UI that the user has already seen.",
      "type": "boolean"
    }
  },
  "type": "object"
}
```

</details>

