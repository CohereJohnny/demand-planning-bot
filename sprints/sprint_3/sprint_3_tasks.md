# Sprint 3 Tasks

## Goals
Implement supply chain disruption simulation and inventory optimization tools. By the end of this sprint, we should have three fully functional MCP tools that model supply disruptions, calculate inventory requirements, and estimate carrying costs.

## Tasks

### 1. Supply Chain Disruption Simulation Tool
- [x] 1.1 Create `src/demand_planning_bot/tools/supply_chain.py`
- [x] 1.2 Define disruption models
  - [x] Strait of Hormuz closure scenario
  - [x] Pipeline outage scenarios
  - [x] Port closure scenarios  
  - [x] Weather event scenarios
- [x] 1.3 Define refinery data
  - [x] Rotterdam refinery capacity and location
  - [x] Singapore refinery capacity and location
  - [x] Alternative refineries (optional)
- [x] 1.4 Implement disruption impact calculation
  - [x] Calculate feedstock shortage percentages
  - [x] Calculate procurement cost increases
  - [x] Calculate timeline for impact
  - [x] Consider alternative supply routes
- [x] 1.5 Implement `simulate_supply_disruption` tool
  - [x] Tool decorator and registration
  - [x] Parameters: disruption_type, affected_refineries, duration_days
  - [x] Type hints for all parameters
  - [x] Clear tool description for AI
- [x] 1.6 Return structured response
  - [x] Disruption type and description
  - [x] Impact per refinery (shortages, costs)
  - [x] Timeline and duration
  - [x] Alternative routes and mitigation options
  - [x] Assumptions and confidence level

### 2. Inventory Requirements Calculation Tool  
- [x] 2.1 Create `src/demand_planning_bot/tools/inventory.py`
- [x] 2.2 Implement safety stock calculation formulas
  - [x] Industry-standard formulas (e.g., z-score method)
  - [x] Consider lead time and demand variability
  - [x] Risk-adjusted safety stock
- [x] 2.3 Implement storage capacity calculations
  - [x] Convert safety stock to barrels
  - [x] Calculate additional capacity needed
  - [x] Consider existing inventory levels
- [x] 2.4 Implement `calculate_inventory_requirements` tool
  - [x] Tool decorator and registration
  - [x] Parameters: current_inventory, demand_forecast, risk_level, lead_time
  - [x] Type hints for all parameters
  - [x] Clear tool description for AI
- [x] 2.5 Return structured response
  - [x] Recommended safety stock increase (%)
  - [x] Additional storage capacity (barrels)
  - [x] Rationale and formulas used
  - [x] Risk mitigation benefits
  - [x] Assumptions and confidence level

### 3. Carrying Costs Calculation Tool
- [x] 3.1 Implement carrying cost formulas in `inventory.py`
  - [x] Storage costs (per barrel per month)
  - [x] Insurance costs
  - [x] Opportunity cost calculations
  - [x] Total carrying cost
- [x] 3.2 Implement `calculate_carrying_costs` tool
  - [x] Tool decorator and registration
  - [x] Parameters: inventory_increase, duration_months, cost_per_barrel_month
  - [x] Type hints for all parameters
  - [x] Clear tool description for AI
- [x] 3.3 Return structured response
  - [x] Total carrying cost (USD)
  - [x] Cost breakdown by category
  - [x] Monthly vs. total costs
  - [x] Currency and time period
  - [x] Assumptions

### 4. Server Integration
- [x] 4.1 Register new tools in `server.py`
  - [x] Import supply_chain and inventory modules
  - [x] Register `simulate_supply_disruption` tool
  - [x] Register `calculate_inventory_requirements` tool
  - [x] Register `calculate_carrying_costs` tool
- [x] 4.2 Update server startup logging
  - [x] Log total tools registered
  - [x] Log tool categories

### 5. Unit Tests
- [x] 5.1 Create `tests/test_supply_chain.py`
  - [x] Test disruption model data
  - [x] Test impact calculations
  - [x] Test simulate_supply_disruption tool logic
  - [x] Test different disruption scenarios
  - [x] Test refinery impact calculations
- [x] 5.2 Create `tests/test_inventory.py`
  - [x] Test safety stock formulas
  - [x] Test storage capacity calculations
  - [x] Test calculate_inventory_requirements tool
  - [x] Test carrying cost calculations
  - [x] Test calculate_carrying_costs tool
- [x] 5.3 Run all tests
  - [x] Execute `uv run pytest`
  - [x] Verify all tests pass
  - [x] Check test coverage

### 6. Documentation Updates
- [x] 6.1 Update README.md
  - [x] Add new tools to "Available Tools" section
  - [x] Document parameters and return values
  - [x] Add usage examples with JSON responses
  - [x] Update sprint progress section
- [x] 6.2 Add inline documentation
  - [x] Docstrings for all new functions
  - [x] Type hints throughout
  - [x] Comments for formulas and calculations

### 7. Integration Testing
- [x] 7.1 Test tool integration
  - [x] Start server and verify all tools load
  - [x] Verify 6 tools registered (ping, market, risk, disruption, inventory x2)
- [x] 7.2 Test use case scenario
  - [x] Follow interaction script from specs/use-case.md (lines 32-42)
  - [x] Verify tool chain: risk → disruption → inventory → costs
  - [x] Verify outputs align with use case expectations
- [x] 7.3 Test tool orchestration
  - [x] Use risk assessment output to inform disruption simulation
  - [x] Use disruption output to inform inventory requirements
  - [x] Use inventory requirements to calculate carrying costs
  - [x] Verify data flows between tools

### 8. Code Quality
- [x] 8.1 Run code formatting
  - [x] Execute `uv format`
  - [x] Verify all files formatted
- [x] 8.2 Review type hints
  - [x] All functions have parameter types
  - [x] All functions have return types
- [x] 8.3 Review docstrings
  - [x] All public functions documented
  - [x] Tool descriptions are AI-friendly
- [x] 8.4 Remove TODO comments

### 9. Sprint Review
- [x] 9.1 Verify all tasks completed
- [x] 9.2 Test end-to-end scenarios
- [x] 9.3 Document any gaps or issues
- [x] 9.4 Prepare sprint report

## Sprint Review

*To be completed at the end of the sprint*

### Demo Readiness
- [x] simulate_supply_disruption tool works correctly
- [x] calculate_inventory_requirements tool works correctly
- [x] calculate_carrying_costs tool works correctly
- [x] Tools return structured, AI-readable responses
- [x] Can demo use case scenario from specs/use-case.md (lines 32-42)

### Gaps/Issues
**None** - All objectives completed successfully.

- All 126 tasks completed
- All 80 unit tests passing (26 from Sprint 2 + 54 from Sprint 3)
- Full documentation added to README

### Next Steps
**Ready for Sprint 4**: Financial & Regulatory Tools

Upcoming:
- `calculate_revenue_impact` tool
- `calculate_roi` tool
- `get_regulatory_updates` tool
- `calculate_compliance_costs` tool

## Progress Notes

*Add progress notes, observations, code snippets, or commit references below*

---

### Sprint 3 Execution (October 23, 2025)
- All 126 tasks completed in single session
- Implemented 3 tools with full functionality
- Added 54 unit tests (all passing)
- Updated comprehensive documentation
- Tools support use case scenario (lines 32-42)

**Commits**:
- Sprint 3 planning documentation
- Tool implementation (supply chain + inventory)
- Unit tests with comprehensive coverage
- Code formatting
- README documentation updates

