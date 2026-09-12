# Agents

Notes for AI agents working in this repository.

## Naming

This project is **PyDataRheo**. The import package is `datarheo`, the PyPI distribution is
`pydatarheo`, and the CLI entry points are `pydatarheo` / `pydr` and `datarheo-mcp`.

References to **Airbyte** are deliberate and should not be renamed. They name external systems
that PyDataRheo integrates with: the Airbyte protocol and its message classes, the `airbyte-cdk`
/ `airbyte-api` / `airbyte-protocol-models-pdv2` packages, the public connector registry, and the
Airbyte Cloud API. Renaming those would either break imports or make the documentation wrong.

Everything that names *this* project uses the DataRheo name: exception classes (`DataRheoError`
and friends), environment variables (`DATARHEO_*`), cache metadata columns (`_datarheo_raw_id`,
`_datarheo_extracted_at`, `_datarheo_meta`), and the default cache schema (`datarheo_raw`).

## MCP UI Development

When adding or changing MCP tools that return UI elements:

- Name UI-first tools with a `show_` prefix.
- Return bounded agent-readable text plus structured UI content.
- Make any capped agent preview explicit, because the agent cannot see the user-facing UI.
- Verify the server-side payload contract.
- Capture human-reviewable evidence with MCPJam or Goose Desktop when retesting is requested,
  including the rendered widget and any important UI interaction.
