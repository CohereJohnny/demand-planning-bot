# Demand Planning Server Specification

## ADDED Requirements

### Requirement: MCP Server Foundation
The system SHALL provide an MCP server using the North Python MCP SDK that exposes tools for AI-assisted demand planning in the Oil & Gas supply chain.

#### Scenario: Server starts with stdio transport
- **WHEN** the server is started with `--transport stdio` flag
- **THEN** the server SHALL initialize successfully
- **AND** the server SHALL be accessible via stdio for local testing with MCP Inspector

#### Scenario: Server starts with Streamable HTTP transport
- **WHEN** the server is started with `--transport streamable-http` flag
- **THEN** the server SHALL initialize successfully on the configured port
- **AND** the server SHALL be accessible via HTTP for North platform integration

#### Scenario: Server requires valid configuration
- **WHEN** required environment variables are missing (EIA_API_KEY, NEWS_API_KEY)
- **THEN** the server SHALL log a warning
- **AND** the server SHALL continue startup with fallback data enabled

### Requirement: Market Data Tools
The system SHALL provide tools to retrieve current and historical oil prices using the EIA API.

#### Scenario: Get current Brent crude prices
- **WHEN** the `get_market_prices` tool is called with product="brent" and timeframe="current"
- **THEN** the system SHALL query the EIA API for Brent crude spot prices
- **AND** the system SHALL return a structured response with price, date, currency, and data source

#### Scenario: Handle EIA API failure gracefully
- **WHEN** the `get_market_prices` tool is called and the EIA API is unavailable
- **THEN** the system SHALL return fallback price data
- **AND** the response SHALL include metadata indicating fallback source
- **AND** the system SHALL log the API error for debugging

### Requirement: Geopolitical Risk Assessment
The system SHALL provide tools to assess geopolitical risks affecting oil supply chains using news data and risk scoring.

#### Scenario: Assess Strait of Hormuz closure risk
- **WHEN** the `get_geopolitical_risk_assessment` tool is called with region="Strait of Hormuz"
- **THEN** the system SHALL query NewsAPI for relevant geopolitical news
- **AND** the system SHALL calculate a risk probability based on news sentiment and keywords
- **AND** the system SHALL return structured risk data with probability, impact description, and confidence level

#### Scenario: Handle NewsAPI failure gracefully
- **WHEN** the `get_geopolitical_risk_assessment` tool is called and NewsAPI is unavailable
- **THEN** the system SHALL return pre-defined risk scenarios as fallback data
- **AND** the response SHALL include metadata indicating fallback source
- **AND** the system SHALL log the API error for debugging

### Requirement: Supply Chain Disruption Simulation
The system SHALL provide tools to simulate the impact of supply chain disruptions on refinery operations.

#### Scenario: Simulate Strait of Hormuz closure impact
- **WHEN** the `simulate_supply_disruption` tool is called with disruption="hormuz_closure" and refineries=["rotterdam", "singapore"]
- **THEN** the system SHALL calculate feedstock shortage percentages for each refinery
- **AND** the system SHALL calculate procurement cost increases due to alternative routes
- **AND** the system SHALL return structured data with impacts per refinery, assumptions, and time horizons

#### Scenario: Support multiple disruption types
- **WHEN** the tool is called with different disruption types (pipeline_outage, port_closure, weather_event)
- **THEN** the system SHALL apply appropriate simulation models for each disruption type
- **AND** the system SHALL return type-specific impact metrics

### Requirement: Inventory Optimization Calculations
The system SHALL provide tools to calculate inventory requirements and carrying costs.

#### Scenario: Calculate safety stock requirements
- **WHEN** the `calculate_inventory_requirements` tool is called with current_inventory, demand_forecast, and risk_level
- **THEN** the system SHALL calculate recommended safety stock increase percentage
- **AND** the system SHALL calculate additional storage capacity needed in barrels
- **AND** the system SHALL return recommendations with supporting rationale and industry formulas used

#### Scenario: Calculate carrying costs
- **WHEN** the `calculate_carrying_costs` tool is called with inventory_increase, cost_per_barrel, and duration
- **THEN** the system SHALL calculate total carrying costs
- **AND** the system SHALL break down costs by category (storage, insurance, opportunity cost)
- **AND** the system SHALL return results with currency and time period clearly specified

### Requirement: Financial Impact Analysis
The system SHALL provide tools to calculate revenue impact and ROI for operational decisions.

#### Scenario: Calculate revenue loss from stockouts
- **WHEN** the `calculate_revenue_impact` tool is called with demand, fulfillment_rate, and price_per_unit
- **THEN** the system SHALL calculate potential revenue loss
- **AND** the system SHALL include assumptions about order fulfillment and stockout scenarios
- **AND** the system SHALL return monetary impact with currency and confidence level

#### Scenario: Calculate ROI for inventory investment
- **WHEN** the `calculate_roi` tool is called with investment_cost and expected_benefit
- **THEN** the system SHALL calculate ROI multiplier
- **AND** the system SHALL calculate net benefit
- **AND** the system SHALL return a recommendation (invest/don't invest) with supporting rationale

### Requirement: Regulatory Compliance Information
The system SHALL provide tools to retrieve regulatory updates affecting oil & gas operations.

#### Scenario: Get IMO sulfur emission regulations
- **WHEN** the `get_regulatory_updates` tool is called with regulation_type="emissions"
- **THEN** the system SHALL return current IMO sulfur emission regulations
- **AND** the system SHALL include effective dates and compliance cost estimates
- **AND** the system SHALL specify impact on marine fuel shipments

#### Scenario: Support multiple regulation types
- **WHEN** the tool is called with different regulation types (emissions, transportation, storage)
- **THEN** the system SHALL return relevant regulations for each type
- **AND** the system SHALL include compliance requirements and cost implications

### Requirement: Error Handling and Resilience
The system SHALL handle errors gracefully and provide clear feedback when issues occur.

#### Scenario: Invalid API key configuration
- **WHEN** an API key is invalid or expired
- **THEN** the system SHALL log a descriptive error message
- **AND** the system SHALL fall back to simulated data
- **AND** tool responses SHALL include metadata indicating fallback mode

#### Scenario: Network connectivity issues
- **WHEN** network connectivity to external APIs is lost
- **THEN** the system SHALL timeout requests after a reasonable period
- **AND** the system SHALL fall back to cached or simulated data
- **AND** the system SHALL log network errors for troubleshooting

#### Scenario: Rate limit exceeded
- **WHEN** API rate limits are exceeded (EIA or NewsAPI)
- **THEN** the system SHALL log the rate limit error
- **AND** the system SHALL fall back to cached or simulated data
- **AND** the response SHALL indicate the data source used

### Requirement: Authentication and Security
The system SHALL support authentication using North server secrets.

#### Scenario: Authenticated request with valid secret
- **WHEN** a request includes a valid server_secret in the authorization header
- **THEN** the system SHALL authenticate the request successfully
- **AND** the system SHALL process the tool call normally

#### Scenario: Unauthenticated local testing
- **WHEN** the server runs in stdio mode for local testing
- **THEN** the system SHALL allow tool calls without authentication
- **AND** the system SHALL function normally for development purposes

### Requirement: Tool Response Format
The system SHALL return tool responses in a structured, AI-readable format.

#### Scenario: Tool response includes metadata
- **WHEN** any tool is called successfully
- **THEN** the response SHALL include the primary result or recommendation
- **AND** the response SHALL include supporting calculations or assumptions
- **AND** the response SHALL include confidence level or risk factors
- **AND** the response SHALL include data source information (API, calculated, simulated)
- **AND** the response SHALL use appropriate units (barrels, USD, EUR, MMBtu)

#### Scenario: Tool response is parseable by AI
- **WHEN** a tool returns structured data
- **THEN** the data SHALL be formatted as a dictionary or list
- **AND** the data SHALL use consistent key names across tools
- **AND** the data SHALL include clear labels and descriptions

