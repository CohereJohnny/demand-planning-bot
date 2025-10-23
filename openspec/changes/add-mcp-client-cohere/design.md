# Design: MCP Client with Cohere Integration

## Context
We need to test the demand planning MCP server with an AI assistant that can invoke tools via the Model Context Protocol. The standard MCP client examples use Anthropic's Claude, but we want to demonstrate integration with Cohere's Command A model to showcase LLM provider flexibility.

**Key challenges:**
- Cohere's tool use API differs from Anthropic's format
- MCP tool schemas need to be converted to Cohere's JSON Schema format
- Cohere uses a 4-step workflow (user → tool_plan + tool_calls → tool results → response)
- State management is required for multi-turn conversations with tool calls
- Both stdio and HTTP transports must be supported

**Stakeholders:**
- Developers testing the MCP server
- Users evaluating Cohere vs Anthropic for MCP integrations

## Goals / Non-Goals

**Goals:**
- Demonstrate MCP server functionality with Cohere Command A model
- Provide interactive CLI for testing demand planning workflows from `specs/use-case.md`
- Support both stdio and HTTP transports
- Handle Cohere's tool use workflow correctly (4-step pattern)
- Generate citations from tool results

**Non-Goals:**
- Production-grade client with advanced features (streaming, error recovery)
- Multi-user support or concurrent sessions
- Client-side caching or optimization
- Web UI or non-CLI interface
- Support for LLMs other than Cohere

## Decisions

### Decision 1: Use Cohere's V2 Chat API with tool use
**Rationale:** The V2 API provides the latest tool use capabilities including:
- Automatic tool_plan generation (reasoning about which tools to call)
- Multi-step tool use (agent-like behavior)
- Fine-grained citations from tool results
- Support for parallel tool calls

**Alternatives considered:**
- V1 API: Lacks modern tool use features and citations
- Custom tool calling wrapper: Would require reimplementing Cohere's tool use logic

### Decision 2: Convert MCP tool schemas to Cohere format at runtime
**Rationale:** MCP tools expose their schemas dynamically. We need an adapter that:
- Fetches tool schemas from the MCP server
- Converts them to Cohere's JSON Schema format
- Maps parameter types and descriptions correctly

**Implementation approach:**
```python
def mcp_tool_to_cohere_schema(mcp_tool: dict) -> dict:
    """Convert MCP tool schema to Cohere tool schema format."""
    return {
        "type": "function",
        "function": {
            "name": mcp_tool["name"],
            "description": mcp_tool["description"],
            "parameters": {
                "type": "object",
                "properties": mcp_tool["inputSchema"]["properties"],
                "required": mcp_tool["inputSchema"].get("required", [])
            }
        }
    }
```

**Alternatives considered:**
- Static tool definitions: Would require manual sync between server and client
- Runtime schema generation: Too complex, MCP already provides schemas

### Decision 3: Implement 4-step conversation loop
**Rationale:** Cohere's tool use follows a specific workflow:
1. **User message** → append to messages list
2. **Generate tool calls** → model returns tool_plan and tool_calls
3. **Execute tools** → call MCP server, append results to messages
4. **Generate response** → model synthesizes final answer with citations

This loop may repeat multiple times for multi-step reasoning.

**State management:**
- Maintain `messages` list with all conversation turns
- Track tool call IDs to match results with calls
- Support appending assistant messages with `tool_plan` and `tool_calls`
- Support appending tool messages with `tool_call_id` and `content`

**Alternatives considered:**
- Single-shot tool calling: Doesn't support multi-step reasoning
- Custom state machine: Cohere's pattern is proven and well-documented

### Decision 4: Use MCP Python SDK for protocol handling
**Rationale:** The official MCP Python SDK handles:
- Protocol negotiation and initialization
- Transport abstraction (stdio, HTTP)
- Tool schema discovery and invocation
- Error handling and reconnection

**Dependencies:**
- `mcp` Python package (official MCP client SDK)
- `cohere` Python package (Cohere AI SDK)

**Alternatives considered:**
- Raw protocol implementation: Too complex, error-prone
- Custom MCP wrapper: Reinventing the wheel

### Decision 5: Interactive CLI with command history
**Rationale:** For testing, we need a CLI that:
- Accepts user queries interactively
- Displays tool calls and results for transparency
- Shows final AI responses with citations
- Supports conversation history (multi-turn)
- Allows exit/reset commands

**User experience:**
```
$ python client.py --transport stdio

Demand Planning MCP Client (Cohere Command A)
Type 'exit' to quit, 'reset' to clear history

You: What's the current price of Brent crude?

[Tool Call] get_market_prices(product="brent", timeframe="current")
[Tool Result] {"price": 76.45, "currency": "USD", "source": "EIA API"}