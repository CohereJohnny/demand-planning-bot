# Tasks: Add MCP Client with Cohere Integration

## 1. Setup and Dependencies
- [ ] 1.1 Add `cohere` SDK to pyproject.toml dependencies
- [ ] 1.2 Add `mcp` Python SDK for client capabilities
- [ ] 1.3 Update .env.example with COHERE_API_KEY
- [ ] 1.4 Update README.md with client usage instructions

## 2. MCP Tool Schema Adapter
- [ ] 2.1 Create `src/demand_planning_bot/client/utils/cohere_adapter.py`
- [ ] 2.2 Implement `mcp_tool_to_cohere_schema()` function to convert MCP tool schemas to Cohere format
- [ ] 2.3 Implement `mcp_tools_to_cohere_tools()` function to batch convert all tools
- [ ] 2.4 Add unit tests for schema conversion

## 3. MCP Client Implementation
- [ ] 3.1 Create `src/demand_planning_bot/client/utils/mcp_client.py`
- [ ] 3.2 Implement MCP connection handling (stdio and HTTP transports)
- [ ] 3.3 Implement tool discovery (list available tools from server)
- [ ] 3.4 Implement tool execution (call MCP server tools with parameters)
- [ ] 3.5 Add error handling for connection failures

## 4. Conversation State Management
- [ ] 4.1 Create `src/demand_planning_bot/client/conversation.py`
- [ ] 4.2 Implement `ConversationManager` class
- [ ] 4.3 Implement messages list management (user, assistant, tool messages)
- [ ] 4.4 Implement tool call ID tracking
- [ ] 4.5 Implement conversation reset functionality

## 5. Cohere Integration
- [ ] 5.1 Create `src/demand_planning_bot/client/cohere_client.py`
- [ ] 5.2 Initialize Cohere ClientV2 with API key
- [ ] 5.3 Implement 4-step tool use workflow:
  - [ ] 5.3.1 Step 1: Append user message to conversation
  - [ ] 5.3.2 Step 2: Generate tool calls with Cohere chat API
  - [ ] 5.3.3 Step 3: Execute tools via MCP and append results
  - [ ] 5.3.4 Step 4: Generate final response with citations
- [ ] 5.4 Implement multi-step tool use (agent loop)
- [ ] 5.5 Implement citation extraction and display

## 6. Interactive CLI
- [ ] 6.1 Create `client.py` main entry point
- [ ] 6.2 Implement command-line argument parsing (--transport, --port, --model)
- [ ] 6.3 Implement interactive input loop
- [ ] 6.4 Display tool calls and results with formatting
- [ ] 6.5 Display final AI responses with citations
- [ ] 6.6 Implement exit and reset commands
- [ ] 6.7 Add graceful error handling and user feedback

## 7. Testing
- [ ] 7.1 Test stdio transport connection to MCP server
- [ ] 7.2 Test HTTP transport connection to MCP server
- [ ] 7.3 Test single tool call scenarios
- [ ] 7.4 Test parallel tool calls
- [ ] 7.5 Test multi-step tool use (agent behavior)
- [ ] 7.6 Test conversation history across multiple turns
- [ ] 7.7 Test use case scenarios from `specs/use-case.md`

## 8. Documentation
- [ ] 8.1 Add client usage guide to README.md
- [ ] 8.2 Document Cohere API key setup
- [ ] 8.3 Add example interactions
- [ ] 8.4 Document transport options (stdio vs HTTP)

