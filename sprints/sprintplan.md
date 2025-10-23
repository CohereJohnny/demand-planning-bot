# Sprint Plan: Demand Planning MCP Server

## Project Overview
Implement a demonstration MCP (Model Context Protocol) server for AI-assisted demand planning in the Oil & Gas supply chain using the North Python MCP SDK. The server will expose 8 tools that enable AI assistants to help analysts with forecasting, risk assessment, inventory optimization, and scenario planning.

**OpenSpec Change**: `add-mcp-server-implementation`

## Sprint Breakdown

### Sprint 1: Foundation & Core Infrastructure
**Goal**: Set up project structure, core utilities, and basic MCP server

**Deliverables**:
- Project initialized with uv and dependencies
- Basic MCP server running with stdio and HTTP transports
- Configuration management (environment variables, API key validation)
- HTTP client utilities with error handling
- Project documentation (README, .env.example)

**Duration**: ~3-5 days

**Success Criteria**:
- Server starts successfully in both stdio and HTTP modes
- Configuration loader validates API keys and logs helpful messages
- MCP Inspector can connect to the server
- README documents setup process

---

### Sprint 2: Market Data & Risk Assessment Tools
**Goal**: Implement tools for market data and geopolitical risk assessment

**Deliverables**:
- `get_market_prices` tool with EIA API integration
- `get_geopolitical_risk_assessment` tool with NewsAPI integration
- Error handling and fallback data for both APIs
- Unit tests for market data and risk assessment tools
- Rate limiting awareness and API response caching

**Duration**: ~4-6 days

**Success Criteria**:
- Tools successfully fetch real data from EIA and NewsAPI
- Graceful degradation when APIs are unavailable
- Tools return structured, AI-readable responses
- Can demo the interaction from specs/use-case.md lines 28-32

---

### Sprint 3: Supply Chain & Inventory Tools
**Goal**: Implement supply chain simulation and inventory optimization tools

**Deliverables**:
- `simulate_supply_disruption` tool with disruption models
- `calculate_inventory_requirements` tool
- `calculate_carrying_costs` tool
- Realistic refinery data (Rotterdam, Singapore, etc.)
- Unit tests for supply chain and inventory calculations

**Duration**: ~4-6 days

**Success Criteria**:
- Supply disruption simulations produce realistic impacts
- Inventory calculations use industry-standard formulas
- Tools handle multiple disruption types and refinery locations
- Can demo the interaction from specs/use-case.md lines 32-40

---

### Sprint 4: Financial, Regulatory & Integration
**Goal**: Complete remaining tools and perform end-to-end testing

**Deliverables**:
- `calculate_revenue_impact` tool
- `calculate_roi` tool
- `get_regulatory_updates` tool
- Comprehensive integration testing with MCP Inspector
- Complete documentation (tool descriptions, testing guide)
- Code quality improvements (formatting, type hints, docstrings)

**Duration**: ~3-5 days

**Success Criteria**:
- All 8 tools implemented and tested
- Full use case scenario (specs/use-case.md) can be demonstrated
- All unit tests pass
- Code is properly formatted and documented
- Demo-ready presentation

---

## Total Timeline
**Estimated**: 14-22 days (2-4 weeks)

## Dependencies & Prerequisites
- Python 3.11+
- uv >= 0.8.13
- EIA API key (free tier: https://www.eia.gov/opendata/register.php)
- NewsAPI key (free tier: https://newsapi.org/register)
- MCP Inspector (`npx @modelcontextprotocol/inspector`)

## Risk Factors
1. **API Rate Limits**: May hit rate limits during testing
   - Mitigation: Implement fallback data, cache responses
   
2. **API Availability**: External APIs may be down or slow
   - Mitigation: Graceful degradation, comprehensive error handling
   
3. **Scope Creep**: Temptation to add features beyond core requirements
   - Mitigation: Stick to OpenSpec requirements, use backlog for new ideas

## Success Metrics
- ✅ All 8 MCP tools implemented and functional
- ✅ Can demonstrate complete use case from specs/use-case.md
- ✅ Server works with both stdio and HTTP transports
- ✅ Graceful error handling for all API failures
- ✅ Clear documentation for setup and usage
- ✅ Code quality: formatted, typed, tested

## Notes
- This is a **demo project** - prioritize working functionality over production polish
- Follow "simplicity first" principle - avoid over-engineering
- Each sprint should produce demonstrable, testable progress
- Use sprint_x_updates.md to track blockers and decisions

