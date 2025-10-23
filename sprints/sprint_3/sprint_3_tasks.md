# Sprint 3 Tasks

## Goals
Implement supply chain disruption simulation and inventory optimization tools. By the end of this sprint, we should have three fully functional MCP tools that model supply disruptions, calculate inventory requirements, and estimate carrying costs.

## Tasks

### 1. Supply Chain Disruption Simulation Tool
- [ ] 1.1 Create `src/demand_planning_bot/tools/supply_chain.py`
- [ ] 1.2 Define disruption models
  - [ ] Strait of Hormuz closure scenario
  - [ ] Pipeline outage scenarios
  - [ ] Port closure scenarios  
  - [ ] Weather event scenarios
- [ ] 1.3 Define refinery data
  - [ ] Rotterdam refinery capacity and location
  - [ ] Singapore refinery capacity and location
  - [ ] Alternative refineries (optional)
- [ ] 1.4 Implement disruption impact calculation
  - [ ] Calculate feedstock shortage percentages
  - [ ] Calculate procurement cost increases
  - [ ] Calculate timeline for impact
  - [ ] Consider alternative supply routes
- [ ] 1.5 Implement `simulate_supply_disruption` tool
  - [ ] Tool decorator and registration
  - [ ] Parameters: disruption_type, affected_refineries, duration_days
  - [ ] Type hints for all parameters
  - [ ] Clear tool description for AI
- [ ] 1.6 Return structured response
  - [ ] Disruption type and description
  - [ ] Impact per refinery (shortages, costs)
  - [ ] Timeline and duration
  - [ ] Alternative routes and mitigation options
  - [ ] Assumptions and confidence level

### 2. Inventory Requirements Calculation Tool  
- [ ] 2.1 Create `src/demand_planning_bot/tools/inventory.py`
- [ ] 2.2 Implement safety stock calculation formulas
  - [ ] Industry-standard formulas (e.g., z-score method)
  - [ ] Consider lead time and demand variability
  - [ ] Risk-adjusted safety stock
- [ ] 2.3 Implement storage capacity calculations
  - [ ] Convert safety stock to barrels
  - [ ] Calculate additional capacity needed
  - [ ] Consider existing inventory levels
- [ ] 2.4 Implement `calculate_inventory_requirements` tool
  - [ ] Tool decorator and registration
  - [ ] Parameters: current_inventory, demand_forecast, risk_level, lead_time
  - [ ] Type hints for all parameters
  - [ ] Clear tool description for AI
- [ ] 2.5 Return structured response
  - [ ] Recommended safety stock increase (%)
  - [ ] Additional storage capacity (barrels)
  - [ ] Rationale and formulas used
  - [ ] Risk mitigation benefits
  - [ ] Assumptions and confidence level

### 3. Carrying Costs Calculation Tool
- [ ] 3.1 Implement carrying cost formulas in `inventory.py`
  - [ ] Storage costs (per barrel per month)
  - [ ] Insurance costs
  - [ ] Opportunity cost calculations
  - [ ] Total carrying cost
- [ ] 3.2 Implement `calculate_carrying_costs` tool
  - [ ] Tool decorator and registration
  - [ ] Parameters: inventory_increase, duration_months, cost_per_barrel_month
  - [ ] Type hints for all parameters
  - [ ] Clear tool description for AI
- [ ] 3.3 Return structured response
  - [ ] Total carrying cost (USD)
  - [ ] Cost breakdown by category
  - [ ] Monthly vs. total costs
  - [ ] Currency and time period
  - [ ] Assumptions

### 4. Server Integration
- [ ] 4.1 Register new tools in `server.py`
  - [ ] Import supply_chain and inventory modules
  - [ ] Register `simulate_supply_disruption` tool
  - [ ] Register `calculate_inventory_requirements` tool
  - [ ] Register `calculate_carrying_costs` tool
- [ ] 4.2 Update server startup logging
  - [ ] Log total tools registered
  - [ ] Log tool categories

### 5. Unit Tests
- [ ] 5.1 Create `tests/test_supply_chain.py`
  - [ ] Test disruption model data
  - [ ] Test impact calculations
  - [ ] Test simulate_supply_disruption tool logic
  - [ ] Test different disruption scenarios
  - [ ] Test refinery impact calculations
- [ ] 5.2 Create `tests/test_inventory.py`
  - [ ] Test safety stock formulas
  - [ ] Test storage capacity calculations
  - [ ] Test calculate_inventory_requirements tool
  - [ ] Test carrying cost calculations
  - [ ] Test calculate_carrying_costs tool
- [ ] 5.3 Run all tests
  - [ ] Execute `uv run pytest`
  - [ ] Verify all tests pass
  - [ ] Check test coverage

### 6. Documentation Updates
- [ ] 6.1 Update README.md
  - [ ] Add new tools to "Available Tools" section
  - [ ] Document parameters and return values
  - [ ] Add usage examples with JSON responses
  - [ ] Update sprint progress section
- [ ] 6.2 Add inline documentation
  - [ ] Docstrings for all new functions
  - [ ] Type hints throughout
  - [ ] Comments for formulas and calculations

### 7. Integration Testing
- [ ] 7.1 Test tool integration
  - [ ] Start server and verify all tools load
  - [ ] Verify 6 tools registered (ping, market, risk, disruption, inventory x2)
- [ ] 7.2 Test use case scenario
  - [ ] Follow interaction script from specs/use-case.md (lines 32-42)
  - [ ] Verify tool chain: risk → disruption → inventory → costs
  - [ ] Verify outputs align with use case expectations
- [ ] 7.3 Test tool orchestration
  - [ ] Use risk assessment output to inform disruption simulation
  - [ ] Use disruption output to inform inventory requirements
  - [ ] Use inventory requirements to calculate carrying costs
  - [ ] Verify data flows between tools

### 8. Code Quality
- [ ] 8.1 Run code formatting
  - [ ] Execute `uv format`
  - [ ] Verify all files formatted
- [ ] 8.2 Review type hints
  - [ ] All functions have parameter types
  - [ ] All functions have return types
- [ ] 8.3 Review docstrings
  - [ ] All public functions documented
  - [ ] Tool descriptions are AI-friendly
- [ ] 8.4 Remove TODO comments

### 9. Sprint Review
- [ ] 9.1 Verify all tasks completed
- [ ] 9.2 Test end-to-end scenarios
- [ ] 9.3 Document any gaps or issues
- [ ] 9.4 Prepare sprint report

## Sprint Review

*To be completed at the end of the sprint*

### Demo Readiness
- [ ] simulate_supply_disruption tool works correctly
- [ ] calculate_inventory_requirements tool works correctly
- [ ] calculate_carrying_costs tool works correctly
- [ ] Tools return structured, AI-readable responses
- [ ] Can demo use case scenario from specs/use-case.md (lines 32-42)

### Gaps/Issues
*To be filled in during sprint review*

### Next Steps
*To be filled in during sprint review*

## Progress Notes

*Add progress notes, observations, code snippets, or commit references below*

---

### Day 1
*Notes to be added during sprint execution*

