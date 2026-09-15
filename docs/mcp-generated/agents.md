# agents module

MCP primitives registered by the `agents` module of the `datarheo-mcp` server: **5** tool(s), **0** prompt(s), **0** resource(s).

## Tools (5)

<a id="execute_agent_connector"></a>

### execute_agent_connector

**Hints:** `open-world`

**Availability:** experimental, insiders only (`DATARHEO_MCP_INSIDERS=1` for stdio, `X-MCP-Insiders: 1` for hosted servers, or name the module in the include-modules setting; `DATARHEO_MCP_INSIDERS=0` disables it regardless).

Execute a single action against an Airbyte Agents connector, including writes.

    Prefer `execute_agent_connector_ro` when only reading, since it is available in
    read-only mode. Entity types and actions are connector-specific, so call
    `inspect_agent_connector` first. The connector must belong to the given workspace.
    

The Airbyte Agents API authenticates with Airbyte Cloud credentials. When connecting to a hosted MCP server, provide a bearer token via the `Authorization` header, or client credentials via the transport `Client-Id` and `Client-Secret` headers. For local or stdio connections, set the `DATARHEO_CLOUD_BEARER_TOKEN` environment variable, or both `DATARHEO_CLOUD_CLIENT_ID` and `DATARHEO_CLOUD_CLIENT_SECRET`. Call `list_agent_connectors` to discover connector IDs, then `inspect_agent_connector` to learn which entities a connector supports, before calling `execute_agent_connector`.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `connector_id` | `string` | yes | — | The ID of the Airbyte Agents connector. |
| `entity_type` | `string` | yes | — | The type of entity to act on, for example 'issues'. Call `inspect_agent_connector` to see the entity types a connector supports. |
| `action` | `enum("list", "get", "search", "api_search", "sql_select", "create", "update", "delete")` | yes | — | The action to run against the entity type. For `sql_select`, pass `sql` and `sql_dialect` (snowflake, bigquery, athena, trino) in `api_args` and any value for `entity_type`. |
| `api_args` | `object \| string \| null` | no | `null` | Connector-specific arguments for the action, as an object or a JSON object string. For example {'repository': 'Vrahad-Analytics/pydatarheo'}. |
| `select_fields` | `array<string> \| string \| null` | no | `null` | Fields to keep in the response, as a list or a CSV string. |
| `exclude_fields` | `array<string> \| string \| null` | no | `null` | Fields to drop from the response, as a list or a CSV string. |
| `page_size` | `integer \| null` | no | `null` | Maximum number of entities to return in this page. |
| `cursor` | `string \| null` | no | `null` | Pagination cursor, taken from `end_cursor` of a previous result. |
| `intent` | `string \| null` | no | `null` | A short description of why the action is being run. |
| `read_only` | `boolean \| null` | no | `null` | Set to `true` to reject write actions before any request is sent, when the caller wants a read guarantee from this tool. |
| `workspace_id` | `string \| null` | no | `null` | Workspace ID. Hosted MCP connections pass it via the `X-DataRheo-Workspace-Id` header; local or stdio connections use the `DATARHEO_CLOUD_WORKSPACE_ID` environment variable. |
| `organization_id` | `string \| null` | no | `null` | Organization ID. Omit it when the credentials belong to exactly one organization, or when it is already configured via the `X-DataRheo-Organization-Id` header or the `DATARHEO_CLOUD_ORGANIZATION_ID` environment variable. To discover organization IDs, call `list_agent_workspaces`, which reports the owning organization of each workspace, or `list_cloud_organizations` to search organizations by name. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "connector_id": {
      "description": "The ID of the Airbyte Agents connector.",
      "type": "string"
    },
    "entity_type": {
      "description": "The type of entity to act on, for example 'issues'. Call `inspect_agent_connector` to see the entity types a connector supports.",
      "type": "string"
    },
    "action": {
      "description": "The action to run against the entity type. For `sql_select`, pass `sql` and `sql_dialect` (snowflake, bigquery, athena, trino) in `api_args` and any value for `entity_type`.",
      "enum": [
        "list",
        "get",
        "search",
        "api_search",
        "sql_select",
        "create",
        "update",
        "delete"
      ],
      "type": "string"
    },
    "api_args": {
      "anyOf": [
        {
          "additionalProperties": true,
          "type": "object"
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Connector-specific arguments for the action, as an object or a JSON object string. For example {'repository': 'Vrahad-Analytics/pydatarheo'}."
    },
    "select_fields": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Fields to keep in the response, as a list or a CSV string."
    },
    "exclude_fields": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Fields to drop from the response, as a list or a CSV string."
    },
    "page_size": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Maximum number of entities to return in this page."
    },
    "cursor": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Pagination cursor, taken from `end_cursor` of a previous result."
    },
    "intent": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "A short description of why the action is being run."
    },
    "read_only": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Set to `true` to reject write actions before any request is sent, when the caller wants a read guarantee from this tool."
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
    "organization_id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Organization ID. Omit it when the credentials belong to exactly one organization, or when it is already configured via the `X-DataRheo-Organization-Id` header or the `DATARHEO_CLOUD_ORGANIZATION_ID` environment variable. To discover organization IDs, call `list_agent_workspaces`, which reports the owning organization of each workspace, or `list_cloud_organizations` to search organizations by name."
    }
  },
  "required": [
    "connector_id",
    "entity_type",
    "action"
  ],
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "description": "Result of executing a single action against an Airbyte Agents connector.",
  "properties": {
    "status": {
      "type": "string"
    },
    "result": {
      "default": null,
      "title": "Result"
    },
    "has_next_page": {
      "default": false,
      "type": "boolean"
    },
    "end_cursor": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "execution_time_ms": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "warning": {
      "anyOf": [
        {
          "additionalProperties": true,
          "type": "object"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "message": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "required": [
    "status"
  ],
  "type": "object"
}
```

</details>

<a id="execute_agent_connector_ro"></a>

### execute_agent_connector_ro

**Hints:** `read-only` · `idempotent` · `open-world`

**Availability:** experimental, insiders only (`DATARHEO_MCP_INSIDERS=1` for stdio, `X-MCP-Insiders: 1` for hosted servers, or name the module in the include-modules setting; `DATARHEO_MCP_INSIDERS=0` disables it regardless).

Read data from an Airbyte Agents connector, without modifying anything.

    This tool only accepts read actions, so it stays available in read-only mode. Use
    `execute_agent_connector` for actions that create, update, or delete data. Entity types
    are connector-specific, so call `inspect_agent_connector` first. The connector must
    belong to the given workspace.
    

The Airbyte Agents API authenticates with Airbyte Cloud credentials. When connecting to a hosted MCP server, provide a bearer token via the `Authorization` header, or client credentials via the transport `Client-Id` and `Client-Secret` headers. For local or stdio connections, set the `DATARHEO_CLOUD_BEARER_TOKEN` environment variable, or both `DATARHEO_CLOUD_CLIENT_ID` and `DATARHEO_CLOUD_CLIENT_SECRET`. Call `list_agent_connectors` to discover connector IDs, then `inspect_agent_connector` to learn which entities a connector supports, before calling `execute_agent_connector`.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `connector_id` | `string` | yes | — | The ID of the Airbyte Agents connector. |
| `entity_type` | `string` | yes | — | The type of entity to act on, for example 'issues'. Call `inspect_agent_connector` to see the entity types a connector supports. |
| `action` | `enum("list", "get", "search", "api_search", "sql_select")` | yes | — | The read action to run against the entity type. For `sql_select`, pass `sql` and `sql_dialect` (snowflake, bigquery, athena, trino) in `api_args` and any value for `entity_type`. |
| `api_args` | `object \| string \| null` | no | `null` | Connector-specific arguments for the action, as an object or a JSON object string. For example {'repository': 'Vrahad-Analytics/pydatarheo'}. |
| `select_fields` | `array<string> \| string \| null` | no | `null` | Fields to keep in the response, as a list or a CSV string. |
| `exclude_fields` | `array<string> \| string \| null` | no | `null` | Fields to drop from the response, as a list or a CSV string. |
| `page_size` | `integer \| null` | no | `null` | Maximum number of entities to return in this page. |
| `cursor` | `string \| null` | no | `null` | Pagination cursor, taken from `end_cursor` of a previous result. |
| `intent` | `string \| null` | no | `null` | A short description of why the action is being run. |
| `workspace_id` | `string \| null` | no | `null` | Workspace ID. Hosted MCP connections pass it via the `X-DataRheo-Workspace-Id` header; local or stdio connections use the `DATARHEO_CLOUD_WORKSPACE_ID` environment variable. |
| `organization_id` | `string \| null` | no | `null` | Organization ID. Omit it when the credentials belong to exactly one organization, or when it is already configured via the `X-DataRheo-Organization-Id` header or the `DATARHEO_CLOUD_ORGANIZATION_ID` environment variable. To discover organization IDs, call `list_agent_workspaces`, which reports the owning organization of each workspace, or `list_cloud_organizations` to search organizations by name. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "connector_id": {
      "description": "The ID of the Airbyte Agents connector.",
      "type": "string"
    },
    "entity_type": {
      "description": "The type of entity to act on, for example 'issues'. Call `inspect_agent_connector` to see the entity types a connector supports.",
      "type": "string"
    },
    "action": {
      "description": "The read action to run against the entity type. For `sql_select`, pass `sql` and `sql_dialect` (snowflake, bigquery, athena, trino) in `api_args` and any value for `entity_type`.",
      "enum": [
        "list",
        "get",
        "search",
        "api_search",
        "sql_select"
      ],
      "type": "string"
    },
    "api_args": {
      "anyOf": [
        {
          "additionalProperties": true,
          "type": "object"
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Connector-specific arguments for the action, as an object or a JSON object string. For example {'repository': 'Vrahad-Analytics/pydatarheo'}."
    },
    "select_fields": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Fields to keep in the response, as a list or a CSV string."
    },
    "exclude_fields": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Fields to drop from the response, as a list or a CSV string."
    },
    "page_size": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Maximum number of entities to return in this page."
    },
    "cursor": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Pagination cursor, taken from `end_cursor` of a previous result."
    },
    "intent": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "A short description of why the action is being run."
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
    "organization_id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Organization ID. Omit it when the credentials belong to exactly one organization, or when it is already configured via the `X-DataRheo-Organization-Id` header or the `DATARHEO_CLOUD_ORGANIZATION_ID` environment variable. To discover organization IDs, call `list_agent_workspaces`, which reports the owning organization of each workspace, or `list_cloud_organizations` to search organizations by name."
    }
  },
  "required": [
    "connector_id",
    "entity_type",
    "action"
  ],
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "description": "Result of executing a single action against an Airbyte Agents connector.",
  "properties": {
    "status": {
      "type": "string"
    },
    "result": {
      "default": null,
      "title": "Result"
    },
    "has_next_page": {
      "default": false,
      "type": "boolean"
    },
    "end_cursor": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "execution_time_ms": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "warning": {
      "anyOf": [
        {
          "additionalProperties": true,
          "type": "object"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "message": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "required": [
    "status"
  ],
  "type": "object"
}
```

</details>

<a id="inspect_agent_connector"></a>

### inspect_agent_connector

**Hints:** `read-only` · `idempotent` · `open-world`

**Availability:** experimental, insiders only (`DATARHEO_MCP_INSIDERS=1` for stdio, `X-MCP-Insiders: 1` for hosted servers, or name the module in the include-modules setting; `DATARHEO_MCP_INSIDERS=0` disables it regardless).

Inspect an Airbyte Agents connector: metadata, readiness, warnings, and `docs_skill_id`.

    Call this before `execute_agent_connector` to learn what the connector exposes. The
    connector must belong to the given workspace.
    

The Airbyte Agents API authenticates with Airbyte Cloud credentials. When connecting to a hosted MCP server, provide a bearer token via the `Authorization` header, or client credentials via the transport `Client-Id` and `Client-Secret` headers. For local or stdio connections, set the `DATARHEO_CLOUD_BEARER_TOKEN` environment variable, or both `DATARHEO_CLOUD_CLIENT_ID` and `DATARHEO_CLOUD_CLIENT_SECRET`. Call `list_agent_connectors` to discover connector IDs, then `inspect_agent_connector` to learn which entities a connector supports, before calling `execute_agent_connector`.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `connector_id` | `string` | yes | — | The ID of the Airbyte Agents connector. |
| `workspace_id` | `string \| null` | no | `null` | Workspace ID. Hosted MCP connections pass it via the `X-DataRheo-Workspace-Id` header; local or stdio connections use the `DATARHEO_CLOUD_WORKSPACE_ID` environment variable. |
| `organization_id` | `string \| null` | no | `null` | Organization ID. Omit it when the credentials belong to exactly one organization, or when it is already configured via the `X-DataRheo-Organization-Id` header or the `DATARHEO_CLOUD_ORGANIZATION_ID` environment variable. To discover organization IDs, call `list_agent_workspaces`, which reports the owning organization of each workspace, or `list_cloud_organizations` to search organizations by name. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "connector_id": {
      "description": "The ID of the Airbyte Agents connector.",
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
    "organization_id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Organization ID. Omit it when the credentials belong to exactly one organization, or when it is already configured via the `X-DataRheo-Organization-Id` header or the `DATARHEO_CLOUD_ORGANIZATION_ID` environment variable. To discover organization IDs, call `list_agent_workspaces`, which reports the owning organization of each workspace, or `list_cloud_organizations` to search organizations by name."
    }
  },
  "required": [
    "connector_id"
  ],
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "description": "Details about a single Airbyte Agents connector.",
  "properties": {
    "connector_id": {
      "type": "string"
    },
    "connector_name": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
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
      "default": null
    },
    "source_definition_name": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "docs_skill_id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "context_store_entities": {
      "items": {
        "type": "string"
      },
      "type": "array"
    },
    "warnings": {
      "items": {
        "type": "string"
      },
      "type": "array"
    },
    "message": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "required": [
    "connector_id",
    "context_store_entities",
    "warnings"
  ],
  "type": "object"
}
```

</details>

<a id="list_agent_connectors"></a>

### list_agent_connectors

**Hints:** `read-only` · `idempotent` · `open-world`

**Availability:** experimental, insiders only (`DATARHEO_MCP_INSIDERS=1` for stdio, `X-MCP-Insiders: 1` for hosted servers, or name the module in the include-modules setting; `DATARHEO_MCP_INSIDERS=0` disables it regardless).

List the connectors configured in an Airbyte Agents workspace.

The Airbyte Agents API authenticates with Airbyte Cloud credentials. When connecting to a hosted MCP server, provide a bearer token via the `Authorization` header, or client credentials via the transport `Client-Id` and `Client-Secret` headers. For local or stdio connections, set the `DATARHEO_CLOUD_BEARER_TOKEN` environment variable, or both `DATARHEO_CLOUD_CLIENT_ID` and `DATARHEO_CLOUD_CLIENT_SECRET`. Call `list_agent_connectors` to discover connector IDs, then `inspect_agent_connector` to learn which entities a connector supports, before calling `execute_agent_connector`.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `workspace_id` | `string \| null` | no | `null` | Workspace ID. Hosted MCP connections pass it via the `X-DataRheo-Workspace-Id` header; local or stdio connections use the `DATARHEO_CLOUD_WORKSPACE_ID` environment variable. |
| `organization_id` | `string \| null` | no | `null` | Organization ID. Omit it when the credentials belong to exactly one organization, or when it is already configured via the `X-DataRheo-Organization-Id` header or the `DATARHEO_CLOUD_ORGANIZATION_ID` environment variable. To discover organization IDs, call `list_agent_workspaces`, which reports the owning organization of each workspace, or `list_cloud_organizations` to search organizations by name. |

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
    "organization_id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Organization ID. Omit it when the credentials belong to exactly one organization, or when it is already configured via the `X-DataRheo-Organization-Id` header or the `DATARHEO_CLOUD_ORGANIZATION_ID` environment variable. To discover organization IDs, call `list_agent_workspaces`, which reports the owning organization of each workspace, or `list_cloud_organizations` to search organizations by name."
    }
  },
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "description": "Result of listing connectors in an Airbyte Agents workspace.",
  "properties": {
    "connectors": {
      "items": {
        "description": "Information about a connector configured on the Airbyte Agents platform.",
        "properties": {
          "connector_id": {
            "type": "string"
          },
          "connector_name": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "default": null
          }
        },
        "required": [
          "connector_id"
        ],
        "type": "object"
      },
      "type": "array"
    },
    "message": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "required": [
    "connectors"
  ],
  "type": "object"
}
```

</details>

<a id="list_agent_workspaces"></a>

### list_agent_workspaces

**Hints:** `read-only` · `idempotent` · `open-world`

**Availability:** experimental, insiders only (`DATARHEO_MCP_INSIDERS=1` for stdio, `X-MCP-Insiders: 1` for hosted servers, or name the module in the include-modules setting; `DATARHEO_MCP_INSIDERS=0` disables it regardless).

List the workspaces reachable through the Airbyte Agents API.

The Airbyte Agents API authenticates with Airbyte Cloud credentials. When connecting to a hosted MCP server, provide a bearer token via the `Authorization` header, or client credentials via the transport `Client-Id` and `Client-Secret` headers. For local or stdio connections, set the `DATARHEO_CLOUD_BEARER_TOKEN` environment variable, or both `DATARHEO_CLOUD_CLIENT_ID` and `DATARHEO_CLOUD_CLIENT_SECRET`. Call `list_agent_connectors` to discover connector IDs, then `inspect_agent_connector` to learn which entities a connector supports, before calling `execute_agent_connector`.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `organization_id` | `string \| null` | no | `null` | Organization ID. Omit it when the credentials belong to exactly one organization, or when it is already configured via the `X-DataRheo-Organization-Id` header or the `DATARHEO_CLOUD_ORGANIZATION_ID` environment variable. To discover organization IDs, call `list_agent_workspaces`, which reports the owning organization of each workspace, or `list_cloud_organizations` to search organizations by name. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "organization_id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Organization ID. Omit it when the credentials belong to exactly one organization, or when it is already configured via the `X-DataRheo-Organization-Id` header or the `DATARHEO_CLOUD_ORGANIZATION_ID` environment variable. To discover organization IDs, call `list_agent_workspaces`, which reports the owning organization of each workspace, or `list_cloud_organizations` to search organizations by name."
    }
  },
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "description": "Result of listing workspaces on the Airbyte Agents platform.",
  "properties": {
    "workspaces": {
      "items": {
        "description": "Information about a workspace on the Airbyte Agents platform.",
        "properties": {
          "workspace_id": {
            "type": "string"
          },
          "workspace_name": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "default": null
          },
          "organization_id": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "default": null
          }
        },
        "required": [
          "workspace_id"
        ],
        "type": "object"
      },
      "type": "array"
    },
    "message": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "required": [
    "workspaces"
  ],
  "type": "object"
}
```

</details>

