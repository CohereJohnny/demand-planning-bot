# Proposal: Add MCP Server Implementation

## Why
Build a demonstration MCP (Model Context Protocol) server for AI-assisted demand planning in the Oil & Gas supply chain. This server will enable AI assistants to help demand planning analysts with forecasting, risk assessment, inventory optimization, and scenario planning using real market data and simulated supply chain models.

## What Changes
- Implement MCP server using North Python MCP SDK (https://github.com/cohere-ai/north-mcp-python-sdk)
- Create 8 MCP tools to support the use case interaction script (`specs/use-case.md`)
- Integrate with EIA API for real-time oil price data (Brent crude, WTI)
- Integrate with NewsAPI for geopolitical news and OPEC updates
- Implement simulated supply chain disruption models
- Add authentication support using North server secret
- Support both Streamable HTTP and stdio transports
- Add configuration management for API keys and environment variables
- Implement comprehensive error handling and graceful API failure fallbacks

## Impact
- **Affected specs**: Creates new `demand-planning-server` capability
- **Affected code**: Creates new Python codebase with:
  - `server.py` - Main MCP server entry point
  - `tools/market_data.py` - Market price tools (EIA API integration)
  - `tools/risk_assessment.py` - Geopolitical risk tools (NewsAPI integration)
  - `tools/supply_chain.py` - Supply disruption simulation tools
  - `tools/inventory.py` - Inventory optimization calculation tools
  - `tools/financial.py` - ROI and cost calculation tools
  - `tools/regulatory.py` - Regulatory compliance tools
  - `utils/api_client.py` - HTTP client utilities for external APIs
  - `utils/config.py` - Configuration and environment variable management
  - `pyproject.toml` - Project dependencies
  - `.env.example` - Example environment configuration
  - `.gitignore` - Ensure API keys are not committed
  - `README.md` - Setup and usage instructions

