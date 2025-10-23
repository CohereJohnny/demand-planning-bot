# Proposal: Add MCP Client with Cohere Integration

## Why
Build an MCP client to test the demand planning MCP server using Cohere's Command A model instead of Anthropic's Claude. This provides an alternative LLM integration pattern and demonstrates how the MCP server works with different AI providers.

## What Changes
- Implement MCP client using the Model Context Protocol client SDK
- Integrate with Cohere's Command A model for chat and tool use
- Follow Cohere's tool use workflow (4-step pattern: user message → tool calls → tool results → response)
- Support both stdio and HTTP transports to connect to the MCP server
- Implement state management for multi-turn conversations with tool calls
- Add conversation history tracking and citation support
- Create interactive CLI for testing demand planning workflows
- Add configuration for Cohere API key and MCP server connection

## Impact
- **Affected specs**: Creates new `mcp-client-testing` capability
- **Affected code**: Creates new Python client implementation with:
  - `client.py` - Main MCP client with Cohere integration
  - `conversation.py` - Conversation state and history management
  - `utils/cohere_adapter.py` - Adapter to convert MCP tools to Cohere tool schemas
  - `utils/mcp_client.py` - MCP protocol client utilities
  - Updates to `pyproject.toml` - Add cohere-ai SDK dependency
  - Updates to `.env.example` - Add COHERE_API_KEY
  - Updates to `README.md` - Add client usage instructions

