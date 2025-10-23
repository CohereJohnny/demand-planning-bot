# Sprint 2 Tasks

## Goals
Implement market data and geopolitical risk assessment tools with real API integrations (EIA and NewsAPI). By the end of this sprint, we should have two fully functional MCP tools that can retrieve real-time oil prices and assess geopolitical risks affecting supply chains.

## Tasks

### 1. EIA API Integration
- [ ] 1.1 Create `src/demand_planning_bot/tools/market_data.py`
- [ ] 1.2 Implement EIA API client class
  - [ ] Authentication with API key
  - [ ] Endpoint for Brent crude spot prices
  - [ ] Endpoint for WTI prices
  - [ ] Response parsing and data transformation
- [ ] 1.3 Add error handling specific to EIA API
  - [ ] Invalid API key detection
  - [ ] Rate limit handling
  - [ ] Data availability checks
- [ ] 1.4 Create fallback data for market prices
  - [ ] Realistic historical price ranges
  - [ ] Multiple products (Brent, WTI)
  - [ ] Metadata indicating fallback source

### 2. Market Data MCP Tool
- [ ] 2.1 Implement `get_market_prices` tool
  - [ ] Tool decorator and registration
  - [ ] Parameters: product (Brent/WTI), timeframe (current/historical)
  - [ ] Type hints for all parameters
  - [ ] Clear tool description for AI
- [ ] 2.2 Integrate with EIA API client
  - [ ] Call EIA API with proper parameters
  - [ ] Handle API responses
  - [ ] Format data for AI consumption
- [ ] 2.3 Implement fallback logic
  - [ ] Detect API failures
  - [ ] Switch to fallback data
  - [ ] Include metadata about data source
- [ ] 2.4 Return structured response
  - [ ] Price value and currency
  - [ ] Date/timestamp
  - [ ] Product name
  - [ ] Data source (API or fallback)
  - [ ] Confidence level

### 3. NewsAPI Integration
- [ ] 3.1 Create `src/demand_planning_bot/tools/risk_assessment.py`
- [ ] 3.2 Implement NewsAPI client class
  - [ ] Authentication with API key
  - [ ] Query for OPEC-related news
  - [ ] Query for region-specific geopolitical news
  - [ ] Response parsing
- [ ] 3.3 Add error handling specific to NewsAPI
  - [ ] Invalid API key detection
  - [ ] Rate limit handling
  - [ ] Query result validation
- [ ] 3.4 Implement risk scoring algorithm
  - [ ] Keyword-based sentiment analysis
  - [ ] Threat level keywords (conflict, sanctions, closure, etc.)
  - [ ] Calculate risk probability (0-100%)
  - [ ] Assign confidence levels

### 4. Geopolitical Risk Assessment MCP Tool
- [ ] 4.1 Implement `get_geopolitical_risk_assessment` tool
  - [ ] Tool decorator and registration
  - [ ] Parameters: region (Strait of Hormuz, etc.), timeframe
  - [ ] Type hints for all parameters
  - [ ] Clear tool description for AI
- [ ] 4.2 Integrate with NewsAPI client
  - [ ] Query news for specified region
  - [ ] Parse and analyze news articles
  - [ ] Calculate risk scores
- [ ] 4.3 Create fallback data for risk scenarios
  - [ ] Pre-defined risk scenarios (Strait of Hormuz, pipeline disruptions)
  - [ ] Realistic probability values
  - [ ] Impact descriptions
  - [ ] Metadata indicating fallback source
- [ ] 4.4 Implement fallback logic
  - [ ] Detect API failures
  - [ ] Switch to fallback scenarios
  - [ ] Include metadata about data source
- [ ] 4.5 Return structured response
  - [ ] Risk probability (percentage)
  - [ ] Impact description
  - [ ] Supporting news headlines
  - [ ] Confidence level
  - [ ] Data source (API or fallback)

### 5. Server Integration
- [ ] 5.1 Register new tools in `server.py`
  - [ ] Import market_data and risk_assessment modules
  - [ ] Register `get_market_prices` tool
  - [ ] Register `get_geopolitical_risk_assessment` tool
- [ ] 5.2 Update server startup logging
  - [ ] Log registered tools count
  - [ ] Verify tool descriptions

### 6. Unit Tests
- [ ] 6.1 Create `tests/test_market_data.py`
  - [ ] Test EIA API client with mock responses
  - [ ] Test get_market_prices tool logic
  - [ ] Test fallback data mechanism
  - [ ] Test error handling
- [ ] 6.2 Create `tests/test_risk_assessment.py`
  - [ ] Test NewsAPI client with mock responses
  - [ ] Test risk scoring algorithm
  - [ ] Test get_geopolitical_risk_assessment tool logic
  - [ ] Test fallback data mechanism
  - [ ] Test error handling
- [ ] 6.3 Run all tests
  - [ ] Execute `uv run pytest`
  - [ ] Verify all tests pass
  - [ ] Check test coverage

### 7. Documentation Updates
- [ ] 7.1 Update README.md
  - [ ] Add new tools to "Available Tools" section
  - [ ] Update tool descriptions with parameters
  - [ ] Add examples of tool usage
- [ ] 7.2 Update .env.example if needed
  - [ ] Verify all environment variables documented
- [ ] 7.3 Add inline documentation
  - [ ] Docstrings for all new functions
  - [ ] Type hints throughout
  - [ ] Comments for complex logic

### 8. Integration Testing
- [ ] 8.1 Test with real API keys
  - [ ] Configure .env with actual EIA_API_KEY
  - [ ] Configure .env with actual NEWS_API_KEY
  - [ ] Start server and verify tools load
- [ ] 8.2 Test with MCP Inspector
  - [ ] Connect via stdio transport
  - [ ] List tools and verify new tools appear
  - [ ] Call get_market_prices with Brent crude
  - [ ] Call get_geopolitical_risk_assessment for Strait of Hormuz
  - [ ] Verify structured responses
- [ ] 8.3 Test fallback scenarios
  - [ ] Remove API keys from .env
  - [ ] Restart server
  - [ ] Call tools and verify fallback data returned
  - [ ] Check metadata indicates fallback source
- [ ] 8.4 Test use case scenario
  - [ ] Follow interaction script from specs/use-case.md (lines 28-32)
  - [ ] Verify tools can support the conversation flow

### 9. Code Quality
- [ ] 9.1 Run code formatting
  - [ ] Execute `uv format`
  - [ ] Verify all files formatted
- [ ] 9.2 Review type hints
  - [ ] All functions have parameter types
  - [ ] All functions have return types
- [ ] 9.3 Review docstrings
  - [ ] All public functions documented
  - [ ] Tool descriptions are AI-friendly
- [ ] 9.4 Remove TODO comments

### 10. Sprint Review
- [ ] 10.1 Verify all tasks completed
- [ ] 10.2 Test end-to-end scenarios
- [ ] 10.3 Document any gaps or issues
- [ ] 10.4 Prepare sprint report

## Sprint Review

*To be completed at the end of the sprint*

### Demo Readiness
- [ ] get_market_prices tool works with real EIA API
- [ ] get_geopolitical_risk_assessment tool works with real NewsAPI
- [ ] Both tools gracefully fall back when APIs unavailable
- [ ] Tools return structured, AI-readable responses
- [ ] Can demo use case scenario from specs/use-case.md

### Gaps/Issues
*To be filled in during sprint review*

### Next Steps
*To be filled in during sprint review*

## Progress Notes

*Add progress notes, observations, code snippets, or commit references below*

---

### Day 1
*Notes to be added during sprint execution*

