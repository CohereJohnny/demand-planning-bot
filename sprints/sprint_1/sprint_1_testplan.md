# Sprint 1 Test Plan

## Test Scope
Verify that the MCP server foundation is working correctly with proper configuration management, error handling, and transport support.

## Test Environment
- **Python Version**: 3.11+
- **Package Manager**: uv >= 0.8.13
- **Tools**: MCP Inspector
- **Operating System**: macOS

## Prerequisites
- Project dependencies installed (`uv sync`)
- `.env` file configured with placeholder values (API keys not required for Sprint 1)

---

## Test Cases

### TC-1: Project Setup
**Objective**: Verify project structure is correctly set up

**Steps**:
1. Check directory structure exists (tools/, utils/, tests/)
2. Verify `pyproject.toml` has correct dependencies
3. Run `uv sync` and verify no errors
4. Check `.env.example` exists with all required variables

**Expected Result**: All files and directories present, dependencies install successfully

**Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Passed | ⬜ Failed

---

### TC-2: Configuration Management
**Objective**: Verify configuration loading and validation

**Steps**:
1. Remove `.env` file (if exists)
2. Run server and observe warning messages
3. Create `.env` with valid placeholder values
4. Run server and verify configuration loads successfully
5. Test with DEBUG=true and verify debug logging

**Expected Result**: 
- Missing .env produces warnings but doesn't crash
- Valid .env loads successfully
- Debug mode enables verbose logging

**Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Passed | ⬜ Failed

---

### TC-3: Server Startup (stdio)
**Objective**: Verify server starts correctly with stdio transport

**Steps**:
1. Run: `uv run python server.py --transport stdio`
2. Observe startup logs
3. Verify no errors or exceptions

**Expected Result**: Server starts successfully, logs indicate stdio transport active

**Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Passed | ⬜ Failed

---

### TC-4: Server Startup (HTTP)
**Objective**: Verify server starts correctly with Streamable HTTP transport

**Steps**:
1. Run: `uv run python server.py --transport streamable-http --port 5222`
2. Observe startup logs
3. Verify server is listening on specified port
4. Check no errors or exceptions

**Expected Result**: Server starts successfully, logs indicate HTTP transport active on port 5222

**Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Passed | ⬜ Failed

---

### TC-5: MCP Inspector Connection (stdio)
**Objective**: Verify MCP Inspector can connect via stdio

**Steps**:
1. Run: `npx @modelcontextprotocol/inspector`
2. Configure Inspector:
   - Transport Type: stdio
   - Command: uv
   - Arguments: run python server.py --transport stdio
3. Click "Connect"
4. Navigate to "Tools" tab
5. Click "List Tools"

**Expected Result**: 
- Connection successful
- Test tool appears in tool list
- Tool has proper description

**Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Passed | ⬜ Failed

---

### TC-6: MCP Inspector Connection (HTTP)
**Objective**: Verify MCP Inspector can connect via Streamable HTTP

**Steps**:
1. Start server: `uv run python server.py --transport streamable-http --port 5222`
2. Run: `npx @modelcontextprotocol/inspector`
3. Configure Inspector:
   - Transport Type: Streamable HTTP
   - URL: http://localhost:5222/mcp
4. Click "Connect"
5. Navigate to "Tools" tab
6. Click "List Tools"

**Expected Result**: 
- Connection successful
- Test tool appears in tool list
- Tool has proper description

**Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Passed | ⬜ Failed

---

### TC-7: Test Tool Invocation
**Objective**: Verify test tool can be successfully invoked

**Steps**:
1. Connect MCP Inspector (stdio or HTTP)
2. List tools and select test tool (ping/hello_world)
3. Fill in any required parameters
4. Click "Run"
5. Observe response

**Expected Result**: 
- Tool executes successfully
- Returns structured JSON response
- Response includes expected fields
- No errors in server logs

**Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Passed | ⬜ Failed

---

### TC-8: API Client Error Handling
**Objective**: Verify API client handles errors gracefully

**Steps**:
1. Run unit tests: `uv run pytest tests/test_api_client.py`
2. Verify tests for:
   - Network timeouts
   - Connection failures
   - 4xx errors
   - 5xx errors
   - Rate limiting (429)

**Expected Result**: All unit tests pass, error handling works correctly

**Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Passed | ⬜ Failed

---

### TC-9: Code Quality Checks
**Objective**: Verify code meets quality standards

**Steps**:
1. Run: `uv format --preview-features format --check`
2. Verify all files pass formatting check
3. Review code for type hints
4. Review code for docstrings
5. Check for TODO comments or placeholders

**Expected Result**: 
- All code is properly formatted
- All functions have type hints
- All functions have docstrings
- No TODOs or placeholders

**Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Passed | ⬜ Failed

---

## Test Summary

**Total Test Cases**: 9
**Passed**: 0
**Failed**: 0
**Blocked**: 0
**Not Started**: 9

## Issues Found
*Document any issues discovered during testing*

---

## Sign-off

**Tester**: _____________________
**Date**: _____________________
**Sprint Status**: ⬜ Ready for Review | ⬜ Issues Found | ⬜ Approved

