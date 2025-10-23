# Project Context

## Purpose
AI-Assisted Demand Planning Bot for Oil & Gas Supply Chain - **Demo Project**. This MCP (Model Context Protocol) server enables AI assistants to help demand planning analysts like Sarah Thompson forecast demand, assess risks, optimize inventory, and make data-driven decisions for complex supply chain operations in the oil and gas industry.

This is a demonstration project to showcase MCP server capabilities for the oil & gas domain. No production deployment or frontend interface is required.

Key goals:
- Provide real-time market data and geopolitical risk assessments via MCP tools
- Enable advanced analytics for demand pattern recognition
- Support scenario planning for supply chain disruptions
- Deliver actionable insights with ROI calculations
- Ensure compliance awareness for regulatory requirements

## Tech Stack
- **Framework**: North MCP Python SDK (https://github.com/cohere-ai/north-mcp-python-sdk)
- **Language**: Python 3.11+
- **Package Manager**: uv (>=0.8.13)
- **Transport**: Streamable HTTP (recommended) or stdio for local testing
- **Authentication**: North OAuth and server secret support

## Project Conventions

### Code Style
- **File naming**: Use snake_case for Python modules (e.g., `demand_forecast.py`, `risk_assessment.py`)
- **Function naming**: Use snake_case for functions and variables
- **Class naming**: Use PascalCase for classes (e.g., `DemandForecast`, `RiskAssessment`)
- **Type hints**: Use Python type hints for function parameters and return values
- **Error handling**: Implement comprehensive error handling and logging
- **Docstrings**: Use docstrings for all functions and classes
- **Code quality**: Focus on readability over performance; write clear, maintainable code
- **No emojis**: Only use emojis in code if explicitly requested by the user

### Architecture Patterns
- **MCP Tools**: Implement functionality as discrete MCP tools (functions exposed to AI)
- **Function organization**: Keep tools focused and single-purpose (each tool does one thing well)
- **Data sources**: Mock or simulate external data sources for demo purposes
- **Authentication**: Use North authentication to access user identity when needed
- **Transport**: Default to Streamable HTTP for production-like behavior; stdio for local testing
- **File structure**: Organize tools by domain/feature (e.g., `forecast_tools.py`, `risk_tools.py`, `inventory_tools.py`)
- **Simplicity first**: Default to simple implementations (<100 lines of new code) until complexity is proven necessary
- **Stateless**: MCP tools should be stateless; each call is independent

### Configuration Management
- **Environment variables**: Store sensitive data (API keys, secrets) in environment variables
  - `EIA_API_KEY`: API key for U.S. Energy Information Administration
  - `NEWS_API_KEY`: API key for NewsAPI
  - `SERVER_SECRET`: Secret for protecting the MCP server (optional for local testing)
- **Config file**: Consider `.env` file for local development (never commit to git)
- **Example .env**:
  ```
  EIA_API_KEY=your_eia_api_key_here
  NEWS_API_KEY=your_newsapi_key_here
  SERVER_SECRET=your_server_secret_here
  ```
- **.gitignore**: Ensure `.env` and API keys are never committed to version control

### Testing Strategy
- Test MCP tools with the MCP Inspector (`npx @modelcontextprotocol/inspector`)
- Validate tool outputs with realistic Oil & Gas industry scenarios from `specs/use-case.md`
- Test both stdio and Streamable HTTP transports
- Use `uv run pytest` for unit tests of business logic (forecasting, ROI calculations)
- Run `uv format --preview-features format --check` before committing
- Verify tools work end-to-end with North authentication (when applicable)
- **API testing**: Test with real API keys in development; consider mock responses for CI/CD

### Git Workflow
**Sprint-based development** with the following process:

1. **Sprint branches**: Create branch per sprint (e.g., `sprint-1`, `sprint-2`)
2. **Sprint documentation**: 
   - `sprints/sprint_x/sprint_x_tasks.md` - Track tasks and progress
   - `sprints/sprint_x/sprint_x_updates.md` - Ongoing notes and context
   - `sprints/sprint_x/sprint_x_testplan.md` - Test plans
   - `sprints/sprint_x/sprint_x_report.md` - Final summary
3. **Commit conventions**: 
   - `feat:` for new MCP tools/features
   - `fix:` for bug fixes (reference BUG-XXX from `bug_swatting.md`)
   - Commit frequently with clear, descriptive messages
4. **Pull requests**: Create PR for sprint branch, verify checks pass, merge to `main`
5. **Tagging**: Tag merge commits with sprint number (`git tag sprint-x`)
6. **Archiving**: Archive completed sprint directories to `sprints/archive/`
7. **Central logs**: 
   - `sprints/sprintplan.md` - High-level plan for all sprints
   - `sprints/bug_swatting.md` - Critical bug fixes
   - `sprints/tech_debt.md` - Non-critical issues/refactors
   - `sprints/backlog.md` - New feature ideas

## MCP Server Design

### Tool Structure
Each MCP tool represents a discrete capability that the AI can invoke. Tools should:
- Have clear, descriptive names (e.g., `get_geopolitical_risk`, `calculate_inventory_roi`)
- Accept well-defined parameters with type hints
- Return structured data (dicts, lists) that are easy for AI to parse
- Include rich descriptions to help the AI understand when to use them
- Return metadata about assumptions, confidence levels, or data sources

### Example Tool Pattern
```python
@mcp.tool()
def calculate_inventory_roi(
    current_inventory: int,
    proposed_increase: int,
    carrying_cost_per_barrel: float,
    estimated_revenue_loss: float
) -> dict:
    """
    Calculate ROI for proposed inventory increase.
    
    Returns dict with: roi_multiplier, net_benefit, recommendation
    """
    # Implementation
    pass
```

### Transport Modes
- **Streamable HTTP**: Default for demo, mirrors production behavior with North platform
- **stdio**: Use for local testing with MCP Inspector without authentication

### Authentication Strategy
- **Server secret**: Protect the server from unauthorized access
- **User identity**: Access authenticated user's email/profile (optional for demo)
- **OAuth tokens**: Access third-party services on user's behalf (not required for demo)

## Domain Context

### Oil & Gas Supply Chain
This application serves **demand planning analysts** in the oil and gas industry who need to:
- Forecast crude oil and refined product demand across global markets
- Optimize inventory levels for refineries and distribution hubs
- Assess geopolitical risks affecting supply routes (e.g., Strait of Hormuz closures)
- Model supply chain disruptions (pipeline outages, port closures, weather events)
- Calculate carrying costs, ROI, and revenue loss scenarios
- Ensure compliance with regulatory requirements (e.g., IMO sulfur emission regulations)

### Key Concepts
- **Demand forecasting**: Time-series predictions for crude oil and refined products
- **Scenario planning**: Monte Carlo simulations and what-if analysis
- **Inventory optimization**: Safety stock calculations, storage capacity planning
- **Risk assessment**: Geopolitical risk scoring and impact analysis
- **Compliance tracking**: Hazardous materials transportation regulations
- **Market data**: Real-time oil prices (Brent crude), weather forecasts, shipping routes

### User Persona
- **Name**: Sarah Thompson (Senior Demand Planning Analyst at PetroGlobal Energy)
- **Communication style**: Technical, data-driven, prefers concise insights with actionable recommendations
- **Needs**: Real-time data, advanced analytics, scenario modeling, compliance awareness

### Expected MCP Tools (Based on Use Case)
The following tools should be implemented to support the interaction script in `specs/use-case.md`:

1. **`get_market_prices`**: Get current/historical oil prices (Brent, WTI) from EIA API
   - Data source: **EIA API** (real)
   
2. **`get_geopolitical_risk_assessment`**: Retrieve risk analysis for specific regions/routes (e.g., Strait of Hormuz)
   - Data source: **NewsAPI** (real) + risk scoring algorithm (simulated)
   
3. **`simulate_supply_disruption`**: Model impact of disruptions on refinery operations
   - Data source: Simulated disruption models
   
4. **`calculate_inventory_requirements`**: Recommend safety stock adjustments and storage needs
   - Calculation: Industry-standard safety stock formulas
   
5. **`calculate_carrying_costs`**: Estimate storage and inventory holding costs
   - Calculation: Cost per barrel × duration
   
6. **`calculate_revenue_impact`**: Calculate potential revenue loss from stockouts
   - Calculation: Lost sales × fulfillment rate
   
7. **`calculate_roi`**: Compute ROI for inventory or operational decisions
   - Calculation: (benefit - cost) / cost
   
8. **`get_regulatory_updates`**: Retrieve relevant regulatory changes (e.g., IMO emissions)
   - Data source: Static/simulated regulatory database

Each tool should return structured data with:
- Primary result/recommendation
- Supporting calculations/assumptions
- Confidence level or risk factors
- Relevant units and currency
- Data source information (API, simulated, calculated)

## Important Constraints

### Demo-Specific
- **No production deployment**: This is a demonstration project only
- **Hybrid data approach**: Uses real APIs (EIA, NewsAPI) for market/news data; simulates other data sources
- **API key requirements**: Requires valid API keys for EIA and NewsAPI (set via environment variables)
- **Graceful degradation**: Tools should handle API failures gracefully with fallback data or clear error messages
- **Realistic outputs**: All outputs should use realistic, industry-appropriate calculations and units
- **Interactive demo**: Tools should respond quickly to demonstrate MCP capabilities
- **Configuration**: API keys and settings should be managed via environment variables or config file

### Technical
- **MCP Protocol**: Must adhere to MCP server specifications
- **Response format**: Tool outputs should be clear, structured, and AI-readable
- **Type safety**: Use Python type hints for all tool parameters and returns
- **Error handling**: Comprehensive error handling with descriptive messages
  - Handle API failures (rate limits, network errors, invalid keys)
  - Provide fallback data or clear error messages when APIs are unavailable
  - Log API errors for debugging without exposing sensitive information
- **Logging**: Debug mode support for troubleshooting authentication and API issues
- **Rate limiting**: Respect API rate limits (EIA: ~5000 requests/hour, NewsAPI: varies by plan)

### Business Logic
- **Realistic calculations**: ROI, inventory, and risk calculations should use industry-appropriate formulas
- **Explainable results**: Include assumptions and confidence levels in tool outputs
- **Unit consistency**: Support oil & gas industry units (barrels, MMBtu, USD, EUR)
- **Scenario fidelity**: Tools should align with the interaction script in `specs/use-case.md`

### Implementation
- No placeholders or TODOs in production code
- All functionality must be fully implemented
- Error handling is mandatory, not optional
- Tools should work with both authenticated and unauthenticated modes

## External Dependencies

### MCP Framework
- **north-mcp-python-sdk**: Core MCP server implementation with North authentication support
- **MCP Inspector**: Testing tool for local development (`npx @modelcontextprotocol/inspector`)
- **Python 3.11+**: Required runtime
- **uv**: Package manager and build tool (>=0.8.13)

### Data Sources (Hybrid: Real + Simulated)

**Real External APIs:**
- **EIA API**: U.S. Energy Information Administration for Brent crude oil prices
  - Endpoint: `https://api.eia.gov/v2/petroleum/pri/spt/data/?api_key=YOUR_KEY`
  - Provides: Historical and current oil price data (Brent, WTI)
  - Authentication: API key required (set via environment variable `EIA_API_KEY`)
  
- **NewsAPI**: News aggregation for OPEC and geopolitical events
  - Endpoint: `https://newsapi.org/v2/everything?q=OPEC&apiKey=YOUR_KEY`
  - Provides: Recent news articles related to oil markets, OPEC decisions, geopolitical events
  - Authentication: API key required (set via environment variable `NEWS_API_KEY`)

**Simulated/Static Data:**
- **Weather data**: Simulated weather events affecting supply chains
- **Regulatory data**: Static reference data for IMO regulations and compliance
- **Shipping data**: Mock port status and route information
- **Supply chain models**: Pre-defined disruption scenarios and refinery capacity data

### Python Libraries (Planned)
- **pytest**: Unit testing framework
- **requests** or **httpx**: HTTP client for API calls to EIA and NewsAPI
- **python-dotenv**: Load environment variables from .env file
- **typing**: Type hint support (built-in)
- **datetime**: Time/date handling (built-in)
- **json**: JSON serialization (built-in)
- **os**: Environment variable access for API keys (built-in)
- Additional libraries as needed for calculations (numpy, pandas - optional)

### Development Tools
- **North platform**: For testing authenticated MCP server interactions
- **Bearer token generation**: Utility for local authentication testing
- **Debug logging**: Built-in North SDK debug mode for troubleshooting
