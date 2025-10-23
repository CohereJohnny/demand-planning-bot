# Design Document: MCP Server Implementation

## Context
Building a demonstration MCP server for AI-assisted demand planning in the Oil & Gas supply chain. The server will expose tools that enable AI assistants to help analysts with forecasting, risk assessment, inventory optimization, and scenario planning. This is a demo project to showcase MCP server capabilities, not a production system.

**Stakeholders**: Demo audience, potential customers interested in AI-assisted supply chain planning

**Constraints**: 
- Demo-only (no production deployment)
- Must work with limited/free tier API access
- Should demonstrate realistic industry scenarios
- Must be easy to set up and run locally

## Goals / Non-Goals

### Goals
- Create 8 functional MCP tools that align with the use case in `specs/use-case.md`
- Integrate real market data (EIA API) and news data (NewsAPI) for authenticity
- Implement realistic supply chain calculations using industry-appropriate formulas
- Support both authenticated (North platform) and local testing (MCP Inspector) workflows
- Demonstrate graceful error handling and API failure recovery
- Provide clear, structured outputs that AI assistants can easily parse and present

### Non-Goals
- Production-ready deployment or high availability
- Real-time streaming data or WebSocket connections
- Persistent storage or database integration
- User management beyond basic North authentication
- Complex ML models or advanced forecasting algorithms
- Multi-tenancy or role-based access control

## Decisions

### 1. Transport Protocol
**Decision**: Support both Streamable HTTP (default) and stdio transports

**Rationale**: 
- Streamable HTTP is recommended by North SDK for production-like behavior
- stdio is useful for local testing with MCP Inspector without authentication
- Command-line flag allows easy switching between modes

**Alternatives considered**:
- SSE transport: Deprecated in North SDK
- HTTP-only: Would make local testing more complex

### 2. API Integration Strategy
**Decision**: Use real APIs (EIA, NewsAPI) with graceful fallback to mock data

**Rationale**:
- Real APIs provide authenticity and demonstrate actual integration patterns
- Fallback data ensures demo works even with API failures or rate limits
- Hybrid approach balances realism with reliability

**Alternatives considered**:
- Fully mocked data: Less impressive, doesn't demonstrate API integration
- Real APIs only: Fragile, requires perfect network and API availability

### 3. Tool Organization
**Decision**: Organize tools by domain/feature in separate modules

**File Structure**:
```
tools/
  market_data.py      # EIA API integration
  risk_assessment.py  # NewsAPI + risk scoring
  supply_chain.py     # Disruption simulation
  inventory.py        # Inventory calculations
  financial.py        # ROI and cost calculations
  regulatory.py       # Compliance data
```

**Rationale**:
- Clear separation of concerns
- Easy to locate and modify specific tool categories
- Aligns with project conventions (organize by feature/domain)
- Each module stays focused and under 100 lines where possible

**Alternatives considered**:
- Single tools.py file: Would become too large and hard to navigate
- One file per tool: Too granular, lots of boilerplate

### 4. Error Handling Pattern
**Decision**: Implement tiered error handling with fallback data

**Pattern**:
```python
try:
    # Attempt API call
    data = fetch_from_api()
except APIError as e:
    # Log error
    logger.warning(f"API failed: {e}")
    # Return fallback data with metadata
    data = get_fallback_data()
    data['metadata']['source'] = 'fallback'
    data['metadata']['reason'] = 'API unavailable'
```

**Rationale**:
- Demo continues to work even when APIs fail
- Transparent about data sources (real vs fallback)
- Provides debugging information without breaking UX

### 5. Configuration Management
**Decision**: Use environment variables with python-dotenv for local development

**Environment Variables**:
- `EIA_API_KEY`: EIA API key
- `NEWS_API_KEY`: NewsAPI key
- `SERVER_SECRET`: North authentication secret (optional for local testing)
- `DEBUG`: Enable debug logging (true/false)

**Rationale**:
- Standard practice for sensitive configuration
- Easy to configure in different environments
- Works with .env file for local development
- Compatible with North platform deployment

### 6. Data Simulation Approach
**Decision**: Use realistic but simplified models for supply chain simulations

**Simulation Models**:
- Pre-defined scenarios (e.g., Strait of Hormuz closure at 25% probability)
- Fixed refinery locations (Rotterdam, Singapore) with known capacities
- Industry-standard formulas for safety stock and carrying costs
- Reasonable assumptions clearly documented in tool outputs

**Rationale**:
- Produces realistic results without complex modeling
- Fast response times for interactive demo
- Easy to understand and modify
- Aligns with "simplicity first" principle

**Alternatives considered**:
- Complex ML models: Overkill for demo, slow, hard to explain
- Random/arbitrary values: Unrealistic, not industry-appropriate

## Risks / Trade-offs

### Risk: API Rate Limits
**Mitigation**: 
- Implement fallback data for common scenarios
- Log rate limit errors clearly
- Document rate limits in README (EIA: ~5000/hour, NewsAPI: varies)
- Consider caching API responses (future enhancement)

### Risk: API Key Management
**Mitigation**:
- Clear documentation on obtaining free API keys
- Example .env file with placeholder values
- Validation on startup with helpful error messages
- Never commit keys to version control

### Trade-off: Real APIs vs Reliability
**Accepted**: Demo may occasionally fail if APIs are down or rate-limited. This is acceptable for a demonstration project. Fallback data ensures core functionality always works.

### Trade-off: Simplified Models vs Accuracy
**Accepted**: Supply chain simulations use simplified models that produce realistic but not production-accurate results. This is appropriate for a demo focused on showcasing MCP capabilities rather than supply chain optimization accuracy.

## Migration Plan

N/A - This is a new implementation with no existing system to migrate from.

## Open Questions

1. **Should we implement response caching for API calls?**
   - Pro: Reduces API calls, faster responses, more reliable
   - Con: Adds complexity, may show stale data
   - **Decision**: Not for initial implementation. Add if rate limits become an issue.

2. **Should we add authentication to access user identity?**
   - Pro: More realistic demo of North platform features
   - Con: Adds complexity, not required for core use case
   - **Decision**: Implement server_secret for basic auth. User identity access is optional/future.

3. **Should we use async/await for API calls?**
   - Pro: Better performance, non-blocking
   - Con: More complex code, may not be necessary for demo
   - **Decision**: Start with synchronous calls for simplicity. Add async if performance is an issue.

