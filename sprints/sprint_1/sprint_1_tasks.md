# Sprint 1 Tasks

## Goals
Set up project structure, core utilities, and basic MCP server functionality. By the end of this sprint, we should have a working MCP server that can be connected to via MCP Inspector in both stdio and HTTP modes.

## Tasks

### 1. Project Setup
- [ ] 1.1 Initialize project with uv (`uv init`)
- [ ] 1.2 Create `pyproject.toml` with dependencies
  - north-mcp-python-sdk (git+ssh://git@github.com/cohere-ai/north-mcp-python-sdk.git)
  - requests or httpx
  - python-dotenv
  - pytest
- [ ] 1.3 Create project directory structure
  - [ ] Create `tools/` directory
  - [ ] Create `utils/` directory
  - [ ] Create `tests/` directory
- [ ] 1.4 Install dependencies with `uv sync`

### 2. Configuration Management
- [ ] 2.1 Create `.env.example` with required environment variables
  - EIA_API_KEY
  - NEWS_API_KEY
  - SERVER_SECRET
  - DEBUG
- [ ] 2.2 Create `utils/config.py` for environment variable management
  - [ ] Implement config loading with python-dotenv
  - [ ] Validate required environment variables
  - [ ] Provide helpful error messages for missing keys
  - [ ] Add type hints and docstrings
- [ ] 2.3 Add logging configuration
  - [ ] Support DEBUG environment variable
  - [ ] Configure appropriate log levels
  - [ ] Format log messages clearly

### 3. API Client Utilities
- [ ] 3.1 Create `utils/api_client.py` for HTTP client utilities
  - [ ] Implement generic API client with error handling
  - [ ] Handle network errors (timeouts, connection failures)
  - [ ] Handle API errors (4xx, 5xx responses)
  - [ ] Handle rate limiting (429 responses)
  - [ ] Add retry logic with exponential backoff
  - [ ] Add type hints and docstrings
- [ ] 3.2 Write unit tests for API client utilities

### 4. MCP Server Implementation
- [ ] 4.1 Create `server.py` with NorthMCPServer initialization
  - [ ] Import NorthMCPServer from north_mcp_python_sdk
  - [ ] Configure server name: "Demand Planning Server"
  - [ ] Configure default port (e.g., 5222)
- [ ] 4.2 Add command-line argument parsing
  - [ ] Add `--transport` flag (choices: stdio, streamable-http)
  - [ ] Add `--port` flag for HTTP port configuration
  - [ ] Add `--debug` flag for debug mode
- [ ] 4.3 Implement server startup logic
  - [ ] Load configuration from environment
  - [ ] Initialize server with appropriate transport
  - [ ] Handle server_secret for authenticated mode
  - [ ] Add startup logging messages
- [ ] 4.4 Create a simple test tool to verify server works
  - [ ] Implement `ping` or `hello_world` tool
  - [ ] Add tool description and parameters
  - [ ] Return simple structured response
- [ ] 4.5 Test server startup
  - [ ] Test with stdio transport
  - [ ] Test with streamable-http transport
  - [ ] Verify tool appears in MCP Inspector

### 5. Documentation
- [ ] 5.1 Create `README.md` with setup instructions
  - [ ] Project description and purpose
  - [ ] Prerequisites (Python 3.11+, uv, API keys)
  - [ ] Installation steps
  - [ ] How to obtain API keys (EIA, NewsAPI)
  - [ ] How to configure .env file
  - [ ] How to run the server (stdio and HTTP modes)
  - [ ] How to test with MCP Inspector
- [ ] 5.2 Document project structure
  - [ ] Explain directory organization
  - [ ] Describe purpose of each module
- [ ] 5.3 Add inline documentation
  - [ ] Docstrings for all functions
  - [ ] Type hints for all parameters and returns
  - [ ] Comments for complex logic

### 6. Testing & Validation
- [ ] 6.1 Test server with MCP Inspector (stdio mode)
  - [ ] Start server with `--transport stdio`
  - [ ] Connect with MCP Inspector
  - [ ] List tools and verify test tool appears
  - [ ] Call test tool and verify response
- [ ] 6.2 Test server with MCP Inspector (HTTP mode)
  - [ ] Start server with `--transport streamable-http`
  - [ ] Configure MCP Inspector for HTTP connection
  - [ ] List tools and verify test tool appears
  - [ ] Call test tool and verify response
- [ ] 6.3 Test configuration validation
  - [ ] Test startup with missing .env file (should warn but continue)
  - [ ] Test with invalid configuration
  - [ ] Verify helpful error messages
- [ ] 6.4 Run unit tests
  - [ ] Execute `uv run pytest`
  - [ ] Verify all tests pass
  - [ ] Check test coverage for utilities

### 7. Code Quality
- [ ] 7.1 Run code formatting
  - [ ] Execute `uv format --preview-features format`
  - [ ] Verify all files are properly formatted
- [ ] 7.2 Review code for type hints
  - [ ] Ensure all functions have type hints
  - [ ] Fix any type hint issues
- [ ] 7.3 Review code for docstrings
  - [ ] Ensure all functions have docstrings
  - [ ] Verify docstrings are clear and helpful
- [ ] 7.4 Remove any TODO comments or placeholders

## Sprint Review

*To be completed at the end of the sprint*

### Demo Readiness
- [ ] Server can be started in both stdio and HTTP modes
- [ ] MCP Inspector can connect and list tools
- [ ] Configuration management works correctly
- [ ] Documentation is clear and complete

### Gaps/Issues
*To be filled in during sprint review*

### Next Steps
*To be filled in during sprint review*

## Progress Notes

*Add progress notes, observations, code snippets, or commit references below*

---

### Day 1
*Notes to be added during sprint execution*

