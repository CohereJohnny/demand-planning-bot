# Sprint 5 Test Plan

## Testing Objectives
Verify that the MCP Client with Cohere integration:
1. Connects successfully to the MCP server via stdio and HTTP transports
2. Correctly converts MCP tool schemas to Cohere format
3. Implements Cohere's 4-step tool use workflow correctly
4. Handles single, parallel, and multi-step tool calls
5. Maintains conversation state across multiple turns
6. Displays tool calls, results, and citations clearly

## Test Environment Setup

### Prerequisites
- MCP server running (`python server.py --transport stdio` or `--transport streamable-http`)
- Cohere API key configured in `.env`: `COHERE_API_KEY=your_key_here`
- EIA API key configured (for market data tools)
- NewsAPI key configured (for risk assessment tools)

### Test Data
- Brent crude oil price queries
- Geopolitical risk assessments (Strait of Hormuz)
- Supply chain disruption scenarios
- Inventory and financial calculations

---

## Test Cases

### TC1: Client Connection - stdio Transport
**Objective**: Verify client can connect to MCP server via stdio

**Steps**:
1. Start MCP server: `python server.py --transport stdio`
2. In another terminal, start client: `python client.py --transport stdio`
3. Verify client displays startup message and prompt

**Expected Results**:
- Client connects successfully
- Displays "Demand Planning MCP Client (Cohere Command A)"
- Shows available commands (exit, reset)
- Displays interactive prompt

**Status**: ⬜ Not Started

---

### TC2: Client Connection - HTTP Transport
**Objective**: Verify client can connect to MCP server via HTTP

**Steps**:
1. Start MCP server: `python server.py --transport streamable-http --port 8000`
2. In another terminal, start client: `python client.py --transport streamable-http --port 8000`
3. Verify client displays startup message and prompt

**Expected Results**:
- Client connects successfully via HTTP
- Displays startup message
- Shows interactive prompt

**Status**: ⬜ Not Started

---

### TC3: Tool Discovery
**Objective**: Verify client discovers all available MCP tools

**Steps**:
1. Start client connected to server
2. Check logs or debug output for discovered tools

**Expected Results**:
- Client discovers all 10 tools:
  - ping
  - get_market_prices
  - get_geopolitical_risk_assessment
  - simulate_supply_disruption
  - calculate_inventory_requirements
  - calculate_carrying_costs
  - calculate_revenue_impact
  - calculate_roi
  - get_regulatory_updates
  - calculate_compliance_costs

**Status**: ⬜ Not Started

---

### TC4: Schema Conversion
**Objective**: Verify MCP tool schemas are correctly converted to Cohere format

**Steps**:
1. Run unit tests for `cohere_adapter.py`
2. Verify converted schemas match Cohere's expected format

**Expected Results**:
- All schemas have `type: "function"`
- Each function has `name`, `description`, `parameters`
- Parameters include `type`, `properties`, `required` fields
- No schema conversion errors

**Status**: ⬜ Not Started

---

### TC5: Single Tool Call - Market Data
**Objective**: Test single tool call workflow with market data query

**Input**: `What's the current price of Brent crude?`

**Expected Behavior**:
1. Client appends user message to conversation
2. Cohere generates tool call: `get_market_prices(product="brent", timeframe="current")`
3. Client executes tool via MCP server
4. Client displays tool call and result
5. Cohere generates final response with price
6. Client displays response with citation

**Expected Output**:
```
[Tool Call] get_market_prices(product="brent", timeframe="current")
[Tool Result] {"price": 76.45, "currency": "USD", "source": "EIA API"}