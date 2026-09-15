# prompts module

MCP primitives registered by the `prompts` module of the `datarheo-mcp` server: **0** tool(s), **1** prompt(s), **0** resource(s).

## Prompts (1)

<a id="test-my-tools"></a>

### test-my-tools

Test all available MCP tools to confirm they are working properly

#### Arguments

| Name | Required | Description |
| --- | --- | --- |
| `scope` | no | Optional free-form text to focus or constrain testing. This can be a single word, a sentence, or a paragraph describing the desired scope or constraints.  Provide as a JSON string matching the following schema: {"anyOf":[{"type":"string"},{"type":"null"}],"description":"Optional free-form text to focus or constrain testing. This can be a single word, a sentence, or a paragraph describing the desired scope or constraints."} |

