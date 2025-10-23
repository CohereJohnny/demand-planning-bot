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

## Sprint Progress

### Sprint 1 - ✅ Complete
- Project setup with uv
- Configuration management (environment variables, validation)
- API client utilities (error handling, retries)
- Basic MCP server (stdio + HTTP transports)
- Test tool (`ping`) for verification

### Sprint 2 - ✅ Complete
- Market data tools (EIA API integration)
- Geopolitical risk assessment (NewsAPI integration)
- Error handling and fallback data
- Comprehensive unit tests (26 tests)

### Sprint 3 - ✅ Complete
- Supply chain disruption simulation (4 scenarios)
- Inventory optimization tools (safety stock calculations)
- Carrying cost analysis (storage, insurance, opportunity cost)
- Comprehensive unit tests (54 new tests, 80 total)

### Next Sprint
- Financial analysis tools (ROI, revenue impact)
- Regulatory compliance tools
- Integration testing and documentation

## Available Tools

### `ping` (Test Tool)
Test tool to verify server is working.

**Parameters**:
- `message` (string, optional): Message to echo back

**Returns**: Echo message and server status

**Example**:
```json
{
  "echo": "Hello",
  "status": "Server is running",
  "tools_available": "Sprint 3: Market, risk, supply chain, and inventory tools available"
}
```

---

### `get_market_prices` (Market Data)
Get current or recent oil prices from EIA API. Retrieves spot prices for Brent crude or WTI (West Texas Intermediate) from the U.S. Energy Information Administration. Falls back to simulated data if API is unavailable.

**Parameters**:
- `product` (string, default: "brent"): Oil product type - "brent" for Brent crude or "wti" for WTI
- `timeframe` (string, default: "current"): "current" for latest price, "recent" for last few days

**Returns**: Dictionary with price information
- `price`: Current spot price (float)
- `product`: Product identifier (e.g., "BRENT")
- `currency`: Currency (USD)
- `unit`: Unit of measure (USD per barrel)
- `date`: Price date
- `data_source`: "eia_api" or "fallback"
- `confidence`: Data confidence level ("high" or "medium")

**Example**:
```json
{
  "price": 85.50,
  "product": "BRENT",
  "currency": "USD",
  "unit": "USD per barrel",
  "date": "2025-10-23",
  "data_source": "eia_api",
  "confidence": "high"
}
```

---

### `get_geopolitical_risk_assessment` (Risk Analysis)
Assess geopolitical risks affecting oil supply chains. Analyzes recent news to identify and quantify geopolitical risks that could impact oil supply routes and pricing. Uses NewsAPI for real-time news analysis with keyword-based risk scoring. Falls back to pre-defined scenarios if API is unavailable.

**Parameters**:
- `region` (string, default: "Strait of Hormuz"): Geographic region or chokepoint to assess (e.g., "Strait of Hormuz", "Middle East", "Russia Ukraine")
- `timeframe_days` (integer, default: 7): Number of days of recent news to analyze

**Returns**: Dictionary with risk assessment
- `region`: Region assessed
- `risk_probability`: Probability score (0-100%)
- `risk_level`: "low", "medium", or "high"
- `impact_description`: Detailed impact analysis
- `news_headlines`: Supporting news article titles (list)
- `confidence`: Data confidence level
- `data_source`: "newsapi" or "fallback"

**Example**:
```json
{
  "region": "Strait of Hormuz",
  "risk_probability": 25.0,
  "risk_level": "medium",
  "impact_description": "25% probability of temporary closure...",
  "news_headlines": ["Tensions rise in Persian Gulf", "Iran naval exercises"],
  "confidence": "high",
  "data_source": "newsapi"
}
```

---

### `simulate_supply_disruption` (Supply Chain Simulation)
Simulate the impact of supply chain disruptions on refinery operations. Models scenarios like Strait of Hormuz closure, pipeline outages, port closures, or weather events. Calculates feedstock shortages, cost increases, and timelines. Provides alternative supply routes and mitigation strategies.

**Parameters**:
- `disruption_type` (string, default: "strait_of_hormuz_closure"): Type of disruption
  - `"strait_of_hormuz_closure"`: Major chokepoint closure
  - `"pipeline_outage"`: Crude transport disruption
  - `"port_closure"`: Loading/receiving port closure
  - `"weather_event"`: Hurricane/typhoon
- `affected_refineries` (array, default: ["rotterdam", "singapore"]): List of refineries to analyze
- `duration_days` (integer, default: 14): Expected duration of disruption (1-90 days)

**Returns**: Dictionary with disruption analysis
- `disruption_type`: Type of disruption
- `disruption_name`: Human-readable name
- `description`: Detailed scenario description
- `severity`: "low", "medium", or "high"
- `duration_days`: Expected duration
- `affected_refineries`: Array of refinery impact analyses
  - `refinery`: Refinery name
  - `feedstock_shortage_percentage`: % of feedstock affected
  - `procurement_cost_increase_percentage`: % increase in costs
  - `additional_procurement_cost_usd`: Total additional cost
  - `days_until_impact`: Days before impact felt
  - `mitigation_timeline`: Timeline of events
  - `alternative_routes`: Alternative supply options
- `confidence`: "high"
- `assumptions`: List of modeling assumptions

**Example**:
```json
{
  "disruption_type": "strait_of_hormuz_closure",
  "disruption_name": "Strait of Hormuz Closure",
  "severity": "high",
  "duration_days": 14,
  "affected_refineries": [
    {
      "refinery": "Rotterdam Refinery",
      "feedstock_shortage_percentage": 50.0,
      "procurement_cost_increase_percentage": 25.0,
      "additional_procurement_cost_usd": 140000000.0,
      "days_until_impact": 30,
      "alternative_routes": [
        "Suez Canal via Red Sea (adds 10-14 days)",
        "Cape of Good Hope (adds 20-30 days)"
      ]
    }
  ]
}
```

---

### `calculate_inventory_requirements` (Inventory Optimization)
Calculate recommended inventory levels and safety stock based on demand forecasts, risk levels, and lead times. Uses industry-standard formulas (z-score method) to determine optimal safety stock to mitigate supply chain risks while minimizing stockout probability.

**Parameters**:
- `current_inventory_barrels` (number, default: 500000): Current inventory on hand
- `daily_demand_barrels` (number, default: 50000): Average daily demand
- `demand_std_dev_barrels` (number, default: 5000): Standard deviation of daily demand
- `lead_time_days` (number, default: 21): Procurement lead time in days
- `risk_level` (string, default: "medium"): Assessed risk level
  - `"low"`: 95% service level (z=1.65)
  - `"medium"`: 97.5% service level (z=1.96)
  - `"high"`: 99% service level (z=2.33)

**Returns**: Dictionary with inventory recommendations
- `current_inventory_barrels`: Current inventory level
- `current_days_of_supply`: Days of supply at current inventory
- `recommended_safety_stock_barrels`: Recommended safety stock
- `additional_storage_needed_barrels`: Additional inventory needed
- `safety_stock_increase_percentage`: % increase recommended
- `service_level_percentage`: Target service level
- `rationale`: Explanation of recommendation
- `formula_used`: "Safety Stock = z × σ × √L (z-score method)"
- `assumptions`: List of calculation assumptions
- `confidence`: "high"

**Example**:
```json
{
  "current_inventory_barrels": 500000,
  "current_days_of_supply": 10.0,
  "daily_demand_barrels": 50000,
  "lead_time_days": 21,
  "risk_level": "high",
  "service_level_percentage": 99.0,
  "recommended_safety_stock_barrels": 53439,
  "additional_storage_needed_barrels": 603439,
  "safety_stock_increase_percentage": 120.7,
  "rationale": "To maintain 99.0% service level under high risk conditions...",
  "formula_used": "Safety Stock = z × σ × √L (z-score method)"
}
```

---

### `calculate_carrying_costs` (Financial Analysis)
Calculate the total cost of holding additional inventory over a period. Includes storage costs (warehousing), insurance costs (risk protection), and opportunity costs (capital tied up). Helps evaluate the financial impact of inventory investments for risk mitigation.

**Parameters**:
- `inventory_increase_barrels` (number, default: 100000): Additional inventory to hold
- `duration_months` (integer, default: 3): How long to hold the inventory (1-24 months)
- `cost_per_barrel_month` (number, default: 1.5): Cost to store one barrel for one month (USD)
  - Industry typical: $1.00-$2.00/barrel/month

**Returns**: Dictionary with cost analysis
- `inventory_increase_barrels`: Additional inventory quantity
- `duration_months`: Holding period
- `cost_per_barrel_month`: Unit cost rate
- `storage_cost_usd`: Physical warehousing cost (40% of total)
- `insurance_cost_usd`: Risk protection cost (20% of total)
- `opportunity_cost_usd`: Capital tied up cost (40% of total)
- `total_carrying_cost_usd`: Total cost
- `monthly_carrying_cost_usd`: Average monthly cost
- `cost_breakdown`: Percentage breakdown by category
- `assumptions`: List of cost assumptions

**Example**:
```json
{
  "inventory_increase_barrels": 100000,
  "duration_months": 3,
  "cost_per_barrel_month": 1.5,
  "storage_cost_usd": 180000.00,
  "insurance_cost_usd": 90000.00,
  "opportunity_cost_usd": 180000.00,
  "total_carrying_cost_usd": 450000.00,
  "monthly_carrying_cost_usd": 150000.00,
  "cost_breakdown": {
    "storage_percentage": 40,
    "insurance_percentage": 20,
    "opportunity_cost_percentage": 40
  }
}
```

---

### Future Tools (Sprint 4)

- `calculate_revenue_impact`: Calculate potential revenue loss from stockouts
- `calculate_roi`: Compute ROI for inventory or operational decisions
- `get_regulatory_updates`: Retrieve IMO compliance requirements
- `calculate_compliance_costs`: Estimate costs for regulatory compliance

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

