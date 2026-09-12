---
title: datarheo-mcp — MCP server
sidebar_label: Overview
description: "PyDataRheo connector management and data integration server for discovering,"
---

# `datarheo-mcp`

**Version:** `3.2.0`  

PyDataRheo connector management and data integration server for discovering,
deploying, and running Airbyte connectors.

Use this server for:
- Discovering connectors from the Airbyte registry (sources and destinations)
- Deploying sources, destinations, and connections to Airbyte Cloud
- Running cloud syncs and monitoring sync status
- Managing custom connector definitions in Airbyte Cloud
- Local connector execution for data extraction without cloud deployment
- Listing and describing environment variables for connector configuration

Operational modes:
- Cloud operations: Deploy and manage connectors on Airbyte Cloud (use request
  headers when connecting to a hosted MCP server, or DATARHEO_CLOUD_CLIENT_ID +
  DATARHEO_CLOUD_CLIENT_SECRET (or DATARHEO_CLOUD_BEARER_TOKEN), and optionally
  DATARHEO_CLOUD_WORKSPACE_ID, for local or stdio connections). When no workspace
  ID is configured, the server uses the authenticated user's default workspace;
  when no organization ID is configured, the organization is derived from the
  resolved workspace, whether it came from configuration or the user's default.
  Only call list_cloud_workspaces or list_cloud_organizations if that fails or
  the user wants a different one. If multiple organizations or workspaces are
  returned, ask the user to choose explicitly; never select automatically.
- Local operations: Run connectors locally for data extraction (requires
  DATARHEO_PROJECT_DIR for artifact storage)

Safety features:
- Safe mode (default): Restricts destructive operations to objects created in
  the current session
- Read-only mode: Disables all write operations for cloud resources

## Totals

- **Tools:** 64
- **Prompts:** 1
- **Resources:** 2

## Modules

| Module | Tools | Prompts | Resources |
| --- | ---: | ---: | ---: |
| [`agents`](./agents.md) | 5 | 0 | 0 |
| [`cloud`](./cloud.md) | 40 | 0 | 0 |
| [`interactive`](./interactive.md) | 3 | 0 | 0 |
| [`local`](./local.md) | 12 | 0 | 0 |
| [`prompts`](./prompts.md) | 0 | 1 | 0 |
| [`registry`](./registry.md) | 4 | 0 | 0 |
| [`misc`](./misc.md) | 0 | 0 | 2 |

> These pages are generated from the live `fastmcp inspect` report. Regenerate with `poe mcp-docs-md`.
