# Implementation Tasks

## 1. Project Setup
- [ ] 1.1 Initialize project with uv (`uv init`)
- [ ] 1.2 Create `pyproject.toml` with dependencies (north-mcp-python-sdk, requests/httpx, python-dotenv, pytest)
- [ ] 1.3 Create project directory structure (tools/, utils/, tests/)
- [ ] 1.4 Create `.env.example` with required environment variables
- [ ] 1.5 Update `.gitignore` to exclude `.env`, `__pycache__/`, `.pytest_cache/`, etc.
- [ ] 1.6 Create `README.md` with setup instructions and API key requirements

## 2. Core Infrastructure
- [ ] 2.1 Create `utils/config.py` for environment variable management
- [ ] 2.2 Create `utils/api_client.py` for HTTP client utilities with error handling
- [ ] 2.3 Implement configuration loader with validation for required API keys
- [ ] 2.4 Add logging configuration with debug mode support

## 3. MCP Server Setup
- [ ] 3.1 Create `server.py` with NorthMCPServer initialization
- [ ] 3.2 Configure server name, port, and authentication (server_secret)
- [ ] 3.3 Add command-line argument parsing for transport selection (stdio vs http)
- [ ] 3.4 Implement graceful startup and shutdown handlers
- [ ] 3.5 Add debug mode flag for troubleshooting

## 4. Market Data Tools (EIA API)
- [ ] 4.1 Implement `get_market_prices` tool in `tools/market_data.py`
- [ ] 4.2 Add EIA API client with authentication
- [ ] 4.3 Parse EIA API responses for Brent crude and WTI prices
- [ ] 4.4 Add error handling for API failures with fallback data
- [ ] 4.5 Add rate limiting awareness
- [ ] 4.6 Include data source attribution in responses
- [ ] 4.7 Write unit tests for market data tools

## 5. Geopolitical Risk Tools (NewsAPI)
- [ ] 5.1 Implement `get_geopolitical_risk_assessment` tool in `tools/risk_assessment.py`
- [ ] 5.2 Add NewsAPI client with authentication
- [ ] 5.3 Query NewsAPI for OPEC and geopolitical news
- [ ] 5.4 Implement risk scoring algorithm based on news sentiment/keywords
- [ ] 5.5 Add error handling for API failures with fallback data
- [ ] 5.6 Include confidence levels and assumptions in output
- [ ] 5.7 Write unit tests for risk assessment tools

## 6. Supply Chain Simulation Tools
- [x] 6.1 Implement `simulate_supply_disruption` tool in `tools/supply_chain.py`
- [x] 6.2 Create simulated disruption models (Strait of Hormuz closure, pipeline outages, port closures)
- [x] 6.3 Calculate impact on refinery operations (feedstock shortage percentages)
- [x] 6.4 Calculate procurement cost increases due to alternative routes
- [x] 6.5 Include realistic refinery locations (Rotterdam, Singapore, etc.)
- [x] 6.6 Write unit tests for supply chain simulation

## 7. Inventory Optimization Tools
- [x] 7.1 Implement `calculate_inventory_requirements` tool in `tools/inventory.py`
- [x] 7.2 Calculate safety stock adjustments using industry formulas
- [x] 7.3 Calculate storage capacity requirements (barrels)
- [x] 7.4 Implement `calculate_carrying_costs` tool
- [x] 7.5 Calculate storage and holding costs over time periods
- [x] 7.6 Include unit conversions and currency support
- [x] 7.7 Write unit tests for inventory calculations

## 8. Financial Calculation Tools
- [x] 8.1 Implement `calculate_revenue_impact` tool in `tools/financial.py`
- [x] 8.2 Calculate potential revenue loss from stockouts
- [x] 8.3 Implement order fulfillment rate assumptions
- [x] 8.4 Implement `calculate_roi` tool
- [x] 8.5 Calculate ROI multiplier for inventory investments
- [x] 8.6 Include net benefit calculations
- [x] 8.7 Write unit tests for financial calculations

## 9. Regulatory Compliance Tools
- [x] 9.1 Implement `get_regulatory_updates` tool in `tools/regulatory.py`
- [x] 9.2 Create static reference data for IMO regulations
- [x] 9.3 Add sulfur emission compliance cost calculations
- [x] 9.4 Include effective dates and compliance requirements
- [x] 9.5 Write unit tests for regulatory tools

## 10. Integration Testing
- [ ] 10.1 Test server startup with stdio transport
- [ ] 10.2 Test server startup with Streamable HTTP transport
- [ ] 10.3 Test all tools with MCP Inspector
- [ ] 10.4 Validate tool outputs against `specs/use-case.md` scenarios
- [ ] 10.5 Test authentication with server secret
- [ ] 10.6 Test API key validation and error messages
- [ ] 10.7 Test graceful degradation when APIs are unavailable

## 11. Documentation
- [ ] 11.1 Document all MCP tools with descriptions and parameter details
- [ ] 11.2 Add inline docstrings for all functions
- [ ] 11.3 Create testing guide with MCP Inspector examples
- [ ] 11.4 Document API key acquisition process (EIA, NewsAPI)
- [ ] 11.5 Add troubleshooting section for common issues

## 12. Code Quality
- [ ] 12.1 Run `uv format --preview-features format` on all Python files
- [ ] 12.2 Add type hints to all function parameters and returns
- [ ] 12.3 Run pytest and ensure all tests pass
- [ ] 12.4 Review error messages for clarity and helpfulness
- [ ] 12.5 Remove any TODO comments or placeholders

