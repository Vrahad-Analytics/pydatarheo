# local module

MCP primitives registered by the `local` module of the `datarheo-mcp` server: **12** tool(s), **0** prompt(s), **0** resource(s).

## Tools (12)

<a id="describe_default_cache"></a>

### describe_default_cache

**Hints:** `read-only` · `idempotent`

**Availability:** requires trusted execution (`DATARHEO_MCP_TRUSTED_EXECUTION=1`, stdio transport only); never available over HTTP.

Describe the currently configured default cache.


You can provide `config` as JSON or a Path to a YAML/JSON file.
If a `dict` is provided, it must not contain hardcoded secrets.
Instead, secrets should be provided using environment variables,
and the config should reference them using the format
`secret_reference::ENV_VAR_NAME`.

You can also provide a `config_secret_name` to use a specific
secret name for the configuration. This is useful if you want to
validate a configuration that is stored in a secrets manager.

If `config_secret_name` is provided, it should point to a string
that contains valid JSON or YAML.

If both `config` and `config_secret_name` are provided, the
`config` will be loaded first and then the referenced secret config
will be layered on top of the non-secret config.

For declarative connectors, you can provide a `manifest_path` to
specify a local YAML manifest file instead of using the registry
version. This is useful for testing custom or locally-developed
connector manifests.

#### Parameters

*No parameters.*

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {},
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "additionalProperties": true,
  "type": "object"
}
```

</details>

<a id="destination_smoke_test"></a>

### destination_smoke_test

**Hints:** `destructive`

**Availability:** requires trusted execution (`DATARHEO_MCP_TRUSTED_EXECUTION=1`, stdio transport only); never available over HTTP.

Run smoke tests against a destination connector.

Sends synthetic test data from the smoke test source to the specified
destination and reports success or failure. The smoke test source generates
data across predefined scenarios covering common destination failure patterns:
type variations, null handling, naming edge cases, schema variations, and
batch sizes.

When the destination has a compatible cache implementation (DuckDB,
Postgres, Snowflake, BigQuery, MotherDuck), readback introspection is
automatically performed after a successful write. The readback produces
stats on the written data: table row counts, column names/types, and
per-column null/non-null counts. Results are included in the response
as `table_statistics` and `tables_not_found`.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `destination_connector_name` | `string` | yes | — | The name of the destination connector to test (e.g. 'destination-snowflake', 'destination-motherduck'). |
| `config` | `object \| string \| null` | no | `null` | The destination configuration as a dict object or JSON string. Must not contain hardcoded secrets; use secret_reference::ENV_VAR_NAME instead. |
| `config_file` | `string \| string \| null` | no | `null` | Path to a YAML or JSON file containing the destination configuration. |
| `config_secret_name` | `string \| null` | no | `null` | The name of the secret containing the destination configuration. |
| `scenarios` | `array<string> \| string` | no | `"fast"` | Which scenarios to run. Use 'fast' (default) for all fast predefined scenarios (excludes large_batch_stream), 'all' for every predefined scenario including large batch, or provide a list of scenario names or a comma-separated string. |
| `custom_scenarios` | `array<object> \| null` | no | `null` | Additional custom test scenarios to inject. Each scenario should define 'name', 'json_schema', and optionally 'records' and 'primary_key'. These are unioned with the predefined scenarios. |
| `docker_image` | `string \| null` | no | `null` | Optional Docker image override for the destination connector (e.g. 'airbyte/destination-snowflake:3.14.0'). |
| `namespace_suffix` | `string \| null` | no | `null` | Optional suffix appended to the auto-generated namespace. Defaults to 'smoke_test' (format: 'zz_deleteme_yyyymmdd_hhmm_{suffix}'). Use this to distinguish concurrent runs. |
| `reuse_namespace` | `string \| null` | no | `null` | Exact namespace to reuse from a previous run. When set, no new namespace is generated. Useful for running a second test against an already-populated namespace. |
| `skip_preflight` | `boolean` | no | `false` | Skip the automatic preflight check that runs basic_types before the requested scenarios. Set to true when you expect basic_types itself to fail or want to save time on repeated runs. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "destination_connector_name": {
      "description": "The name of the destination connector to test (e.g. 'destination-snowflake', 'destination-motherduck').",
      "type": "string"
    },
    "config": {
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
      "description": "The destination configuration as a dict object or JSON string. Must not contain hardcoded secrets; use secret_reference::ENV_VAR_NAME instead."
    },
    "config_file": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "format": "path",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Path to a YAML or JSON file containing the destination configuration."
    },
    "config_secret_name": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "The name of the secret containing the destination configuration."
    },
    "scenarios": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "string"
        }
      ],
      "default": "fast",
      "description": "Which scenarios to run. Use 'fast' (default) for all fast predefined scenarios (excludes large_batch_stream), 'all' for every predefined scenario including large batch, or provide a list of scenario names or a comma-separated string."
    },
    "custom_scenarios": {
      "anyOf": [
        {
          "items": {
            "additionalProperties": true,
            "type": "object"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Additional custom test scenarios to inject. Each scenario should define 'name', 'json_schema', and optionally 'records' and 'primary_key'. These are unioned with the predefined scenarios."
    },
    "docker_image": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Optional Docker image override for the destination connector (e.g. 'airbyte/destination-snowflake:3.14.0')."
    },
    "namespace_suffix": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Optional suffix appended to the auto-generated namespace. Defaults to 'smoke_test' (format: 'zz_deleteme_yyyymmdd_hhmm_{suffix}'). Use this to distinguish concurrent runs."
    },
    "reuse_namespace": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Exact namespace to reuse from a previous run. When set, no new namespace is generated. Useful for running a second test against an already-populated namespace."
    },
    "skip_preflight": {
      "default": false,
      "description": "Skip the automatic preflight check that runs basic_types before the requested scenarios. Set to true when you expect basic_types itself to fail or want to save time on repeated runs.",
      "type": "boolean"
    }
  },
  "required": [
    "destination_connector_name"
  ],
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "description": "Result of a destination smoke test run.",
  "properties": {
    "success": {
      "type": "boolean"
    },
    "destination": {
      "type": "string"
    },
    "namespace": {
      "type": "string"
    },
    "records_delivered": {
      "type": "integer"
    },
    "scenarios_requested": {
      "type": "string"
    },
    "elapsed_seconds": {
      "type": "number"
    },
    "error": {
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
    "preflight_passed": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "table_statistics": {
      "anyOf": [
        {
          "additionalProperties": {
            "description": "Statistics for a single table: row count, column info, and per-column stats.",
            "properties": {
              "table_name": {
                "type": "string"
              },
              "database_name": {
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
              "schema_name": {
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
              "row_count": {
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
              "column_statistics": {
                "items": {
                  "description": "Null/non-null statistics for a single column.",
                  "properties": {
                    "column_name": {
                      "type": "string"
                    },
                    "column_type": {
                      "type": "string"
                    },
                    "null_count": {
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
                    "non_null_count": {
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
                    "total_count": {
                      "anyOf": [
                        {
                          "type": "integer"
                        },
                        {
                          "type": "null"
                        }
                      ],
                      "default": null
                    }
                  },
                  "required": [
                    "column_name",
                    "column_type"
                  ],
                  "type": "object"
                },
                "type": "array"
              }
            },
            "required": [
              "table_name",
              "column_statistics"
            ],
            "type": "object"
          },
          "type": "object"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "tables_not_found": {
      "anyOf": [
        {
          "additionalProperties": {
            "type": "string"
          },
          "type": "object"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "warnings": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "required": [
    "success",
    "destination",
    "namespace",
    "records_delivered",
    "scenarios_requested",
    "elapsed_seconds"
  ],
  "type": "object"
}
```

</details>

<a id="get_source_stream_json_schema"></a>

### get_source_stream_json_schema

**Hints:** `read-only` · `idempotent`

**Availability:** requires trusted execution (`DATARHEO_MCP_TRUSTED_EXECUTION=1`, stdio transport only); never available over HTTP.

List all properties for a specific stream in a source connector.


You can provide `config` as JSON or a Path to a YAML/JSON file.
If a `dict` is provided, it must not contain hardcoded secrets.
Instead, secrets should be provided using environment variables,
and the config should reference them using the format
`secret_reference::ENV_VAR_NAME`.

You can also provide a `config_secret_name` to use a specific
secret name for the configuration. This is useful if you want to
validate a configuration that is stored in a secrets manager.

If `config_secret_name` is provided, it should point to a string
that contains valid JSON or YAML.

If both `config` and `config_secret_name` are provided, the
`config` will be loaded first and then the referenced secret config
will be layered on top of the non-secret config.

For declarative connectors, you can provide a `manifest_path` to
specify a local YAML manifest file instead of using the registry
version. This is useful for testing custom or locally-developed
connector manifests.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `source_connector_name` | `string` | yes | — | The name of the source connector. |
| `stream_name` | `string` | yes | — | The name of the stream. |
| `config` | `object \| string \| null` | no | `null` | The configuration for the source connector as a dict or JSON string. |
| `config_file` | `string \| string \| null` | no | `null` | Path to a YAML or JSON file containing the source connector config. |
| `config_secret_name` | `string \| null` | no | `null` | The name of the secret containing the configuration. |
| `override_execution_mode` | `enum("docker", "python", "yaml", "auto")` | no | `"auto"` | Optionally override the execution method to use for the connector. This parameter is ignored if manifest_path is provided (yaml mode will be used). |
| `manifest_path` | `string \| string \| null` | no | `null` | Path to a local YAML manifest file for declarative connectors. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "source_connector_name": {
      "description": "The name of the source connector.",
      "type": "string"
    },
    "stream_name": {
      "description": "The name of the stream.",
      "type": "string"
    },
    "config": {
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
      "description": "The configuration for the source connector as a dict or JSON string."
    },
    "config_file": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "format": "path",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Path to a YAML or JSON file containing the source connector config."
    },
    "config_secret_name": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "The name of the secret containing the configuration."
    },
    "override_execution_mode": {
      "default": "auto",
      "description": "Optionally override the execution method to use for the connector. This parameter is ignored if manifest_path is provided (yaml mode will be used).",
      "enum": [
        "docker",
        "python",
        "yaml",
        "auto"
      ],
      "type": "string"
    },
    "manifest_path": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "format": "path",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Path to a local YAML manifest file for declarative connectors."
    }
  },
  "required": [
    "source_connector_name",
    "stream_name"
  ],
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "additionalProperties": true,
  "type": "object"
}
```

</details>

<a id="get_stream_previews"></a>

### get_stream_previews

**Hints:** `read-only`

**Availability:** requires trusted execution (`DATARHEO_MCP_TRUSTED_EXECUTION=1`, stdio transport only); never available over HTTP.

Get sample records (previews) from streams in a source connector.

    This operation requires a valid configuration, including any required secrets.
    Returns a dictionary mapping stream names to lists of sample records, or an error
    message string if an error occurred for that stream.
    


You can provide `config` as JSON or a Path to a YAML/JSON file.
If a `dict` is provided, it must not contain hardcoded secrets.
Instead, secrets should be provided using environment variables,
and the config should reference them using the format
`secret_reference::ENV_VAR_NAME`.

You can also provide a `config_secret_name` to use a specific
secret name for the configuration. This is useful if you want to
validate a configuration that is stored in a secrets manager.

If `config_secret_name` is provided, it should point to a string
that contains valid JSON or YAML.

If both `config` and `config_secret_name` are provided, the
`config` will be loaded first and then the referenced secret config
will be layered on top of the non-secret config.

For declarative connectors, you can provide a `manifest_path` to
specify a local YAML manifest file instead of using the registry
version. This is useful for testing custom or locally-developed
connector manifests.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `source_name` | `string` | yes | — | The name of the source connector. |
| `config` | `object \| string \| null` | no | `null` | The configuration for the source connector as a dict or JSON string. |
| `config_file` | `string \| string \| null` | no | `null` | Path to a YAML or JSON file containing the source connector config. |
| `config_secret_name` | `string \| null` | no | `null` | The name of the secret containing the configuration. |
| `streams` | `array<string> \| string \| null` | no | `null` | The streams to get previews for. Use '*' for all streams, or None for selected streams. |
| `limit` | `integer` | no | `10` | The maximum number of sample records to return per stream. |
| `override_execution_mode` | `enum("docker", "python", "yaml", "auto")` | no | `"auto"` | Optionally override the execution method to use for the connector. This parameter is ignored if manifest_path is provided (yaml mode will be used). |
| `manifest_path` | `string \| string \| null` | no | `null` | Path to a local YAML manifest file for declarative connectors. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "source_name": {
      "description": "The name of the source connector.",
      "type": "string"
    },
    "config": {
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
      "description": "The configuration for the source connector as a dict or JSON string."
    },
    "config_file": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "format": "path",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Path to a YAML or JSON file containing the source connector config."
    },
    "config_secret_name": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "The name of the secret containing the configuration."
    },
    "streams": {
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
      "description": "The streams to get previews for. Use '*' for all streams, or None for selected streams."
    },
    "limit": {
      "default": 10,
      "description": "The maximum number of sample records to return per stream.",
      "type": "integer"
    },
    "override_execution_mode": {
      "default": "auto",
      "description": "Optionally override the execution method to use for the connector. This parameter is ignored if manifest_path is provided (yaml mode will be used).",
      "enum": [
        "docker",
        "python",
        "yaml",
        "auto"
      ],
      "type": "string"
    },
    "manifest_path": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "format": "path",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Path to a local YAML manifest file for declarative connectors."
    }
  },
  "required": [
    "source_name"
  ],
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "additionalProperties": {
    "anyOf": [
      {
        "items": {
          "additionalProperties": true,
          "type": "object"
        },
        "type": "array"
      },
      {
        "type": "string"
      }
    ]
  },
  "type": "object"
}
```

</details>

<a id="list_cached_streams"></a>

### list_cached_streams

**Hints:** `read-only` · `idempotent`

**Availability:** requires trusted execution (`DATARHEO_MCP_TRUSTED_EXECUTION=1`, stdio transport only); never available over HTTP.

List all streams available in the default DuckDB cache.


You can provide `config` as JSON or a Path to a YAML/JSON file.
If a `dict` is provided, it must not contain hardcoded secrets.
Instead, secrets should be provided using environment variables,
and the config should reference them using the format
`secret_reference::ENV_VAR_NAME`.

You can also provide a `config_secret_name` to use a specific
secret name for the configuration. This is useful if you want to
validate a configuration that is stored in a secrets manager.

If `config_secret_name` is provided, it should point to a string
that contains valid JSON or YAML.

If both `config` and `config_secret_name` are provided, the
`config` will be loaded first and then the referenced secret config
will be layered on top of the non-secret config.

For declarative connectors, you can provide a `manifest_path` to
specify a local YAML manifest file instead of using the registry
version. This is useful for testing custom or locally-developed
connector manifests.

#### Parameters

*No parameters.*

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {},
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "properties": {
    "result": {
      "items": {
        "description": "Class to hold information about a cached dataset.",
        "properties": {
          "stream_name": {
            "type": "string"
          },
          "table_name": {
            "type": "string"
          },
          "schema_name": {
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
          "stream_name",
          "table_name"
        ],
        "type": "object"
      },
      "type": "array"
    }
  },
  "required": [
    "result"
  ],
  "type": "object",
  "x-fastmcp-wrap-result": true
}
```

</details>

<a id="list_connector_config_secrets"></a>

### list_connector_config_secrets

**Hints:** `read-only` · `idempotent`

**Availability:** requires trusted execution (`DATARHEO_MCP_TRUSTED_EXECUTION=1`, stdio transport only); never available over HTTP.

List all `config_secret_name` options that are known for the given connector.

This can be used to find out which already-created config secret names are available
for a given connector. The return value is a list of secret names, but it will not
return the actual secret values.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `connector_name` | `string` | yes | — | The name of the connector. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "connector_name": {
      "description": "The name of the connector.",
      "type": "string"
    }
  },
  "required": [
    "connector_name"
  ],
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "properties": {
    "result": {
      "items": {
        "type": "string"
      },
      "type": "array"
    }
  },
  "required": [
    "result"
  ],
  "type": "object",
  "x-fastmcp-wrap-result": true
}
```

</details>

<a id="list_dotenv_secrets"></a>

### list_dotenv_secrets

**Hints:** `read-only` · `idempotent`

**Availability:** requires trusted execution (`DATARHEO_MCP_TRUSTED_EXECUTION=1`, stdio transport only); never available over HTTP.

List all environment variable names declared within declared .env files.

    This returns a dictionary mapping the .env file name to a list of environment
    variable names. The values of the environment variables are not returned.
    


You can provide `config` as JSON or a Path to a YAML/JSON file.
If a `dict` is provided, it must not contain hardcoded secrets.
Instead, secrets should be provided using environment variables,
and the config should reference them using the format
`secret_reference::ENV_VAR_NAME`.

You can also provide a `config_secret_name` to use a specific
secret name for the configuration. This is useful if you want to
validate a configuration that is stored in a secrets manager.

If `config_secret_name` is provided, it should point to a string
that contains valid JSON or YAML.

If both `config` and `config_secret_name` are provided, the
`config` will be loaded first and then the referenced secret config
will be layered on top of the non-secret config.

For declarative connectors, you can provide a `manifest_path` to
specify a local YAML manifest file instead of using the registry
version. This is useful for testing custom or locally-developed
connector manifests.

#### Parameters

*No parameters.*

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {},
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "additionalProperties": {
    "items": {
      "type": "string"
    },
    "type": "array"
  },
  "type": "object"
}
```

</details>

<a id="list_source_streams"></a>

### list_source_streams

**Hints:** `read-only` · `idempotent`

**Availability:** requires trusted execution (`DATARHEO_MCP_TRUSTED_EXECUTION=1`, stdio transport only); never available over HTTP.

List all streams available in a source connector.

    This operation (generally) requires a valid configuration, including any required secrets.
    


You can provide `config` as JSON or a Path to a YAML/JSON file.
If a `dict` is provided, it must not contain hardcoded secrets.
Instead, secrets should be provided using environment variables,
and the config should reference them using the format
`secret_reference::ENV_VAR_NAME`.

You can also provide a `config_secret_name` to use a specific
secret name for the configuration. This is useful if you want to
validate a configuration that is stored in a secrets manager.

If `config_secret_name` is provided, it should point to a string
that contains valid JSON or YAML.

If both `config` and `config_secret_name` are provided, the
`config` will be loaded first and then the referenced secret config
will be layered on top of the non-secret config.

For declarative connectors, you can provide a `manifest_path` to
specify a local YAML manifest file instead of using the registry
version. This is useful for testing custom or locally-developed
connector manifests.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `source_connector_name` | `string` | yes | — | The name of the source connector. |
| `config` | `object \| string \| null` | no | `null` | The configuration for the source connector as a dict or JSON string. |
| `config_file` | `string \| string \| null` | no | `null` | Path to a YAML or JSON file containing the source connector config. |
| `config_secret_name` | `string \| null` | no | `null` | The name of the secret containing the configuration. |
| `override_execution_mode` | `enum("docker", "python", "yaml", "auto")` | no | `"auto"` | Optionally override the execution method to use for the connector. This parameter is ignored if manifest_path is provided (yaml mode will be used). |
| `manifest_path` | `string \| string \| null` | no | `null` | Path to a local YAML manifest file for declarative connectors. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "source_connector_name": {
      "description": "The name of the source connector.",
      "type": "string"
    },
    "config": {
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
      "description": "The configuration for the source connector as a dict or JSON string."
    },
    "config_file": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "format": "path",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Path to a YAML or JSON file containing the source connector config."
    },
    "config_secret_name": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "The name of the secret containing the configuration."
    },
    "override_execution_mode": {
      "default": "auto",
      "description": "Optionally override the execution method to use for the connector. This parameter is ignored if manifest_path is provided (yaml mode will be used).",
      "enum": [
        "docker",
        "python",
        "yaml",
        "auto"
      ],
      "type": "string"
    },
    "manifest_path": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "format": "path",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Path to a local YAML manifest file for declarative connectors."
    }
  },
  "required": [
    "source_connector_name"
  ],
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "properties": {
    "result": {
      "items": {
        "type": "string"
      },
      "type": "array"
    }
  },
  "required": [
    "result"
  ],
  "type": "object",
  "x-fastmcp-wrap-result": true
}
```

</details>

<a id="read_source_stream_records"></a>

### read_source_stream_records

**Hints:** `read-only`

**Availability:** requires trusted execution (`DATARHEO_MCP_TRUSTED_EXECUTION=1`, stdio transport only); never available over HTTP.

Get records from a source connector.


You can provide `config` as JSON or a Path to a YAML/JSON file.
If a `dict` is provided, it must not contain hardcoded secrets.
Instead, secrets should be provided using environment variables,
and the config should reference them using the format
`secret_reference::ENV_VAR_NAME`.

You can also provide a `config_secret_name` to use a specific
secret name for the configuration. This is useful if you want to
validate a configuration that is stored in a secrets manager.

If `config_secret_name` is provided, it should point to a string
that contains valid JSON or YAML.

If both `config` and `config_secret_name` are provided, the
`config` will be loaded first and then the referenced secret config
will be layered on top of the non-secret config.

For declarative connectors, you can provide a `manifest_path` to
specify a local YAML manifest file instead of using the registry
version. This is useful for testing custom or locally-developed
connector manifests.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `source_connector_name` | `string` | yes | — | The name of the source connector. |
| `config` | `object \| string \| null` | no | `null` | The configuration for the source connector as a dict or JSON string. |
| `config_file` | `string \| string \| null` | no | `null` | Path to a YAML or JSON file containing the source connector config. |
| `config_secret_name` | `string \| null` | no | `null` | The name of the secret containing the configuration. |
| `stream_name` | `string` | yes | — | The name of the stream to read records from. |
| `max_records` | `integer` | no | `1000` | The maximum number of records to read. |
| `override_execution_mode` | `enum("docker", "python", "yaml", "auto")` | no | `"auto"` | Optionally override the execution method to use for the connector. This parameter is ignored if manifest_path is provided (yaml mode will be used). |
| `manifest_path` | `string \| string \| null` | no | `null` | Path to a local YAML manifest file for declarative connectors. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "source_connector_name": {
      "description": "The name of the source connector.",
      "type": "string"
    },
    "config": {
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
      "description": "The configuration for the source connector as a dict or JSON string."
    },
    "config_file": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "format": "path",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Path to a YAML or JSON file containing the source connector config."
    },
    "config_secret_name": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "The name of the secret containing the configuration."
    },
    "stream_name": {
      "description": "The name of the stream to read records from.",
      "type": "string"
    },
    "max_records": {
      "default": 1000,
      "description": "The maximum number of records to read.",
      "type": "integer"
    },
    "override_execution_mode": {
      "default": "auto",
      "description": "Optionally override the execution method to use for the connector. This parameter is ignored if manifest_path is provided (yaml mode will be used).",
      "enum": [
        "docker",
        "python",
        "yaml",
        "auto"
      ],
      "type": "string"
    },
    "manifest_path": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "format": "path",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Path to a local YAML manifest file for declarative connectors."
    }
  },
  "required": [
    "source_connector_name",
    "stream_name"
  ],
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "properties": {
    "result": {
      "anyOf": [
        {
          "items": {
            "additionalProperties": true,
            "type": "object"
          },
          "type": "array"
        },
        {
          "type": "string"
        }
      ]
    }
  },
  "required": [
    "result"
  ],
  "type": "object",
  "x-fastmcp-wrap-result": true
}
```

</details>

<a id="run_sql_query"></a>

### run_sql_query

**Hints:** `read-only` · `idempotent`

**Availability:** requires trusted execution (`DATARHEO_MCP_TRUSTED_EXECUTION=1`, stdio transport only); never available over HTTP.

Run a SQL query against the default cache.

    The dialect of SQL should match the dialect of the default cache.
    Use `describe_default_cache` to see the cache type.

    For DuckDB-type caches:
    - Use `SHOW TABLES` to list all tables.
    - Use `DESCRIBE <table_name>` to get the schema of a specific table

    For security reasons, only read-only operations are allowed: SELECT, DESCRIBE, SHOW, EXPLAIN.
    


You can provide `config` as JSON or a Path to a YAML/JSON file.
If a `dict` is provided, it must not contain hardcoded secrets.
Instead, secrets should be provided using environment variables,
and the config should reference them using the format
`secret_reference::ENV_VAR_NAME`.

You can also provide a `config_secret_name` to use a specific
secret name for the configuration. This is useful if you want to
validate a configuration that is stored in a secrets manager.

If `config_secret_name` is provided, it should point to a string
that contains valid JSON or YAML.

If both `config` and `config_secret_name` are provided, the
`config` will be loaded first and then the referenced secret config
will be layered on top of the non-secret config.

For declarative connectors, you can provide a `manifest_path` to
specify a local YAML manifest file instead of using the registry
version. This is useful for testing custom or locally-developed
connector manifests.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `sql_query` | `string` | yes | — | The SQL query to execute. |
| `max_records` | `integer` | no | `1000` | Maximum number of records to return. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "sql_query": {
      "description": "The SQL query to execute.",
      "type": "string"
    },
    "max_records": {
      "default": 1000,
      "description": "Maximum number of records to return.",
      "type": "integer"
    }
  },
  "required": [
    "sql_query"
  ],
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "properties": {
    "result": {
      "items": {
        "additionalProperties": true,
        "type": "object"
      },
      "type": "array"
    }
  },
  "required": [
    "result"
  ],
  "type": "object",
  "x-fastmcp-wrap-result": true
}
```

</details>

<a id="sync_source_to_cache"></a>

### sync_source_to_cache

**Availability:** requires trusted execution (`DATARHEO_MCP_TRUSTED_EXECUTION=1`, stdio transport only); never available over HTTP.

Run a sync from a source connector to the default DuckDB cache.


You can provide `config` as JSON or a Path to a YAML/JSON file.
If a `dict` is provided, it must not contain hardcoded secrets.
Instead, secrets should be provided using environment variables,
and the config should reference them using the format
`secret_reference::ENV_VAR_NAME`.

You can also provide a `config_secret_name` to use a specific
secret name for the configuration. This is useful if you want to
validate a configuration that is stored in a secrets manager.

If `config_secret_name` is provided, it should point to a string
that contains valid JSON or YAML.

If both `config` and `config_secret_name` are provided, the
`config` will be loaded first and then the referenced secret config
will be layered on top of the non-secret config.

For declarative connectors, you can provide a `manifest_path` to
specify a local YAML manifest file instead of using the registry
version. This is useful for testing custom or locally-developed
connector manifests.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `source_connector_name` | `string` | yes | — | The name of the source connector. |
| `config` | `object \| string \| null` | no | `null` | The configuration for the source connector as a dict or JSON string. |
| `config_file` | `string \| string \| null` | no | `null` | Path to a YAML or JSON file containing the source connector config. |
| `config_secret_name` | `string \| null` | no | `null` | The name of the secret containing the configuration. |
| `streams` | `array<string> \| string` | no | `"suggested"` | The streams to sync. |
| `override_execution_mode` | `enum("docker", "python", "yaml", "auto")` | no | `"auto"` | Optionally override the execution method to use for the connector. This parameter is ignored if manifest_path is provided (yaml mode will be used). |
| `manifest_path` | `string \| string \| null` | no | `null` | Path to a local YAML manifest file for declarative connectors. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "source_connector_name": {
      "description": "The name of the source connector.",
      "type": "string"
    },
    "config": {
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
      "description": "The configuration for the source connector as a dict or JSON string."
    },
    "config_file": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "format": "path",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Path to a YAML or JSON file containing the source connector config."
    },
    "config_secret_name": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "The name of the secret containing the configuration."
    },
    "streams": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "string"
        }
      ],
      "default": "suggested",
      "description": "The streams to sync."
    },
    "override_execution_mode": {
      "default": "auto",
      "description": "Optionally override the execution method to use for the connector. This parameter is ignored if manifest_path is provided (yaml mode will be used).",
      "enum": [
        "docker",
        "python",
        "yaml",
        "auto"
      ],
      "type": "string"
    },
    "manifest_path": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "format": "path",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Path to a local YAML manifest file for declarative connectors."
    }
  },
  "required": [
    "source_connector_name"
  ],
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "properties": {
    "result": {
      "type": "string"
    }
  },
  "required": [
    "result"
  ],
  "type": "object",
  "x-fastmcp-wrap-result": true
}
```

</details>

<a id="validate_connector_config"></a>

### validate_connector_config

**Hints:** `read-only` · `idempotent`

**Availability:** requires trusted execution (`DATARHEO_MCP_TRUSTED_EXECUTION=1`, stdio transport only); never available over HTTP.

Validate a connector configuration.

    Returns a tuple of (is_valid: bool, message: str).
    


You can provide `config` as JSON or a Path to a YAML/JSON file.
If a `dict` is provided, it must not contain hardcoded secrets.
Instead, secrets should be provided using environment variables,
and the config should reference them using the format
`secret_reference::ENV_VAR_NAME`.

You can also provide a `config_secret_name` to use a specific
secret name for the configuration. This is useful if you want to
validate a configuration that is stored in a secrets manager.

If `config_secret_name` is provided, it should point to a string
that contains valid JSON or YAML.

If both `config` and `config_secret_name` are provided, the
`config` will be loaded first and then the referenced secret config
will be layered on top of the non-secret config.

For declarative connectors, you can provide a `manifest_path` to
specify a local YAML manifest file instead of using the registry
version. This is useful for testing custom or locally-developed
connector manifests.

#### Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `connector_name` | `string` | yes | — | The name of the connector to validate. |
| `config` | `object \| string \| null` | no | `null` | The configuration for the connector as a dict object or JSON string. |
| `config_file` | `string \| string \| null` | no | `null` | Path to a YAML or JSON file containing the connector configuration. |
| `config_secret_name` | `string \| null` | no | `null` | The name of the secret containing the configuration. |
| `override_execution_mode` | `enum("docker", "python", "yaml", "auto")` | no | `"auto"` | Optionally override the execution method to use for the connector. This parameter is ignored if manifest_path is provided (yaml mode will be used). |
| `manifest_path` | `string \| string \| null` | no | `null` | Path to a local YAML manifest file for declarative connectors. |

<details>
<summary>Show input JSON schema</summary>

```json
{
  "additionalProperties": false,
  "properties": {
    "connector_name": {
      "description": "The name of the connector to validate.",
      "type": "string"
    },
    "config": {
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
      "description": "The configuration for the connector as a dict object or JSON string."
    },
    "config_file": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "format": "path",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Path to a YAML or JSON file containing the connector configuration."
    },
    "config_secret_name": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "The name of the secret containing the configuration."
    },
    "override_execution_mode": {
      "default": "auto",
      "description": "Optionally override the execution method to use for the connector. This parameter is ignored if manifest_path is provided (yaml mode will be used).",
      "enum": [
        "docker",
        "python",
        "yaml",
        "auto"
      ],
      "type": "string"
    },
    "manifest_path": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "format": "path",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Path to a local YAML manifest file for declarative connectors."
    }
  },
  "required": [
    "connector_name"
  ],
  "type": "object"
}
```

</details>

<details>
<summary>Show output JSON schema</summary>

```json
{
  "properties": {
    "result": {
      "maxItems": 2,
      "minItems": 2,
      "prefixItems": [
        {
          "type": "boolean"
        },
        {
          "type": "string"
        }
      ],
      "type": "array"
    }
  },
  "required": [
    "result"
  ],
  "type": "object",
  "x-fastmcp-wrap-result": true
}
```

</details>

