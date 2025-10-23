# Demand Planning MCP Server

An MCP (Model Context Protocol) server for AI-assisted demand planning in the Oil & Gas supply chain. This demonstration project showcases how AI assistants can help demand planning analysts with forecasting, risk assessment, inventory optimization, and scenario planning.

## Features

- **Market Data**: Real-time oil prices (Brent crude, WTI) via EIA API
- **Geopolitical Risk Assessment**: News-based risk scoring using NewsAPI
- **Supply Chain Simulation**: Model disruption impacts on refinery operations
- **Inventory Optimization**: Safety stock and carrying cost calculations
- **Financial Analysis**: ROI calculations and revenue impact modeling
- **Regulatory Compliance**: IMO regulations and compliance cost estimates

## Prerequisites

- **Python 3.11+**
- **uv >= 0.8.13** (Python package manager)
- **MCP Inspector** (for testing): `npx @modelcontextprotocol/inspector`

### API Keys (Optional for Sprint 1)

- **EIA API** (free): [Register here](https://www.eia.gov/opendata/register.php)
- **NewsAPI** (free tier available): [Register here](https://newsapi.org/register)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd demand-planning-bot
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys (optional for testing)
   ```

## Usage

### Running the Server

#### Option 1: stdio Transport (Local Testing)

Best for local development and testing with MCP Inspector without authentication:

```bash
uv run python server.py --transport stdio
```

#### Option 2: Streamable HTTP Transport (Production-like)

For testing with North platform or authenticated scenarios:

```bash
uv run python server.py --transport streamable-http --port 5222
```

### Command-Line Options

- `--transport {stdio|streamable-http}`: Transport mode (default: streamable-http)
- `--port PORT`: HTTP server port (default: 5222)
- `--debug`: Enable debug logging

### Environment Variables

Configure via `.env` file:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `EIA_API_KEY` | EIA API key for oil price data | No* | - |
| `NEWS_API_KEY` | NewsAPI key for geopolitical news | No* | - |
| `SERVER_SECRET` | Authentication secret for North platform | No | - |
| `PORT` | HTTP server port | No | 5222 |
| `DEBUG` | Enable debug logging (true/false) | No | false |

*Tools will use fallback data if API keys are not provided

## Testing with MCP Inspector

### stdio Mode (No Authentication)

1. Start MCP Inspector:
   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. Configure connection:
   - **Transport Type**: stdio
   - **Command**: `uv`
   - **Arguments**: `run python server.py --transport stdio`

3. Click **Connect**

4. Navigate to **Tools** tab and click **List Tools**

5. Select the `ping` tool and click **Run**

### HTTP Mode (With Optional Authentication)

1. Start the server in a separate terminal:
   ```bash
   uv run python server.py --transport streamable-http
   ```

2. Start MCP Inspector:
   ```bash
   npx @modelcontextprotocol/inspector
   ```

3. Configure connection:
   - **Transport Type**: Streamable HTTP
   - **URL**: `http://localhost:5222/mcp`
   - **Authentication**: (Leave empty for testing without server_secret)

4. Click **Connect**

5. Navigate to **Tools** tab and test tools

## Project Structure

```
demand-planning-bot/
├── server.py                           # Main MCP server entry point
├── src/
│   └── demand_planning_bot/
│       ├── tools/                      # MCP tools (market data, risk, etc.)
│       └── utils/
│           ├── config.py               # Configuration management
│           └── api_client.py           # HTTP client with error handling
├── tests/                              # Unit tests
├── sprints/                            # Sprint planning and documentation
├── openspec/                           # OpenSpec change proposals
├── pyproject.toml                      # Project dependencies
├── .env.example                        # Example environment configuration
└── README.md                           # This file
```

## Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv format --preview-features format
```

### Check Formatting

```bash
uv format --preview-features format --check
```

## Sprint 1 Status

✅ **Completed**:
- Project setup with uv
- Configuration management (environment variables, validation)
- API client utilities (error handling, retries)
- Basic MCP server (stdio + HTTP transports)
- Test tool (`ping`) for verification

🚧 **Next Sprint**:
- Market data tools (EIA API integration)
- Geopolitical risk assessment (NewsAPI integration)
- Error handling and fallback data

## Available Tools

### Sprint 1

- **`ping`**: Test tool to verify server is working
  - Parameters: `message` (string, optional)
  - Returns: Echo message and server status

### Future Sprints

- `get_market_prices`: Retrieve oil prices (Brent, WTI)
- `get_geopolitical_risk_assessment`: Assess regional risks
- `simulate_supply_disruption`: Model disruption impacts
- `calculate_inventory_requirements`: Optimize safety stock
- `calculate_carrying_costs`: Estimate storage costs
- `calculate_revenue_impact`: Calculate stockout losses
- `calculate_roi`: Compute investment ROI
- `get_regulatory_updates`: Retrieve compliance requirements

## Troubleshooting

### Server Won't Start

- Check Python version: `python --version` (must be 3.11+)
- Verify dependencies: `uv sync`
- Check logs for configuration errors

### API Keys Not Working

- Verify API key format in `.env` file
- Check that `.env` is in the project root
- Restart server after changing `.env`
- Server will warn about missing keys but continue with fallback data

### MCP Inspector Connection Issues

**stdio mode**:
- Ensure command is exactly: `uv`
- Arguments: `run python server.py --transport stdio`
- Check server logs for errors

**HTTP mode**:
- Verify server is running: check terminal for "Server will be available at..."
- Confirm URL matches: `http://localhost:5222/mcp`
- Check firewall settings

### Debug Mode

Enable verbose logging:

```bash
uv run python server.py --transport stdio --debug
```

Or set in `.env`:
```
DEBUG=true
```

## Contributing

This is a demonstration project. For changes:

1. Follow the sprint-based workflow in `sprints/`
2. Reference OpenSpec proposals in `openspec/changes/`
3. Maintain test coverage
4. Run formatting before committing

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
- Check `sprints/bug_swatting.md` for known issues
- Review `openspec/project.md` for project conventions
- See `specs/use-case.md` for the interaction scenario

## Acknowledgments

Built with:
- [North MCP Python SDK](https://github.com/cohere-ai/north-mcp-python-sdk)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [EIA API](https://www.eia.gov/opendata/)
- [NewsAPI](https://newsapi.org/)

