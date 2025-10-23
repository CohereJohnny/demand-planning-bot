# Sprint 4 Tasks

## Goals
Implement financial analysis and regulatory compliance tools. By the end of this sprint, we should have four fully functional MCP tools that calculate revenue impacts, ROI, retrieve regulatory updates, and estimate compliance costs.

## Tasks

### 1. Revenue Impact Calculation Tool
- [ ] 1.1 Create `src/demand_planning_bot/tools/financial.py`
- [ ] 1.2 Define revenue impact models
  - [ ] Stockout cost calculations
  - [ ] Lost revenue per barrel formulas
  - [ ] Customer satisfaction impact factors
  - [ ] Market share loss considerations
- [ ] 1.3 Implement revenue impact calculation logic
  - [ ] Calculate direct revenue loss from stockouts
  - [ ] Calculate opportunity cost of lost sales
  - [ ] Consider penalty clauses and contract violations
  - [ ] Include customer retention impact
- [ ] 1.4 Implement `calculate_revenue_impact` tool
  - [ ] Tool decorator and registration
  - [ ] Parameters: stockout_days, daily_demand, price_per_barrel, customer_impact_factor
  - [ ] Type hints for all parameters
  - [ ] Clear tool description for AI
- [ ] 1.5 Return structured response
  - [ ] Direct revenue loss (USD)
  - [ ] Opportunity cost (USD)
  - [ ] Penalty costs (USD)
  - [ ] Customer impact assessment
  - [ ] Total revenue impact (USD)
  - [ ] Assumptions and confidence level

### 2. ROI Calculation Tool
- [ ] 2.1 Implement ROI calculation formulas in `financial.py`
  - [ ] Standard ROI formula: (Benefit - Cost) / Cost * 100
  - [ ] Payback period calculations
  - [ ] Net present value (NPV) considerations
  - [ ] Risk-adjusted returns
- [ ] 2.2 Implement `calculate_roi` tool
  - [ ] Tool decorator and registration
  - [ ] Parameters: investment_cost, expected_benefit, time_period_months, discount_rate
  - [ ] Type hints for all parameters
  - [ ] Clear tool description for AI
- [ ] 2.3 Return structured response
  - [ ] ROI percentage
  - [ ] Payback period (months)
  - [ ] Net benefit (USD)
  - [ ] NPV (if applicable)
  - [ ] Recommendation (good/marginal/poor investment)
  - [ ] Assumptions

### 3. Regulatory Updates Tool
- [ ] 3.1 Create `src/demand_planning_bot/tools/regulatory.py`
- [ ] 3.2 Define IMO regulations database
  - [ ] IMO 2020 sulfur cap (0.5% m/m)
  - [ ] Upcoming IMO 2030 carbon intensity targets
  - [ ] EU ETS (Emissions Trading System) compliance
  - [ ] Regional sulfur requirements
- [ ] 3.3 Implement regulatory filtering logic
  - [ ] Filter by regulation type
  - [ ] Filter by effective date
  - [ ] Filter by region
  - [ ] Calculate time to compliance deadlines
- [ ] 3.4 Implement `get_regulatory_updates` tool
  - [ ] Tool decorator and registration
  - [ ] Parameters: regulation_type, region, effective_after_date
  - [ ] Type hints for all parameters
  - [ ] Clear tool description for AI
- [ ] 3.5 Return structured response
  - [ ] List of applicable regulations
  - [ ] Regulation details (name, description, effective date)
  - [ ] Compliance deadlines
  - [ ] Requirements summary
  - [ ] Impact on operations
  - [ ] Data source notes

### 4. Compliance Costs Calculator
- [ ] 4.1 Implement compliance cost models in `regulatory.py`
  - [ ] Fuel switching costs (low sulfur fuel premium)
  - [ ] Scrubber installation costs
  - [ ] Carbon offset costs (per ton CO2)
  - [ ] Monitoring and reporting costs
- [ ] 4.2 Implement `calculate_compliance_costs` tool
  - [ ] Tool decorator and registration
  - [ ] Parameters: regulation_type, compliance_strategy, annual_fuel_consumption, vessel_count
  - [ ] Type hints for all parameters
  - [ ] Clear tool description for AI
- [ ] 4.3 Return structured response
  - [ ] Total annual compliance cost (USD)
  - [ ] Cost breakdown by category
  - [ ] One-time vs. recurring costs
  - [ ] Cost per barrel impact
  - [ ] Compliance strategy analysis
  - [ ] Assumptions

### 5. Server Integration
- [ ] 5.1 Register new tools in `server.py`
  - [ ] Import financial and regulatory modules
  - [ ] Register `calculate_revenue_impact` tool
  - [ ] Register `calculate_roi` tool
  - [ ] Register `get_regulatory_updates` tool
  - [ ] Register `calculate_compliance_costs` tool
- [ ] 5.2 Update server startup logging
  - [ ] Log total tools registered (now 10 tools)
  - [ ] Log tool categories

### 6. Unit Tests
- [ ] 6.1 Create `tests/test_financial.py`
  - [ ] Test revenue impact calculations
  - [ ] Test stockout cost models
  - [ ] Test calculate_revenue_impact tool
  - [ ] Test ROI formula calculations
  - [ ] Test payback period calculations
  - [ ] Test calculate_roi tool
  - [ ] Test edge cases (zero cost, negative ROI)
- [ ] 6.2 Create `tests/test_regulatory.py`
  - [ ] Test regulatory database structure
  - [ ] Test filtering logic (by type, date, region)
  - [ ] Test get_regulatory_updates tool
  - [ ] Test compliance cost models
  - [ ] Test calculate_compliance_costs tool
  - [ ] Test different compliance strategies
- [ ] 6.3 Run all tests
  - [ ] Execute `uv run pytest`
  - [ ] Verify all tests pass
  - [ ] Check test coverage

### 7. Documentation Updates
- [ ] 7.1 Update README.md
  - [ ] Add new tools to "Available Tools" section
  - [ ] Document parameters and return values
  - [ ] Add usage examples with JSON responses
  - [ ] Update sprint progress section
- [ ] 7.2 Add inline documentation
  - [ ] Docstrings for all new functions
  - [ ] Type hints throughout
  - [ ] Comments for formulas and calculations

### 8. Integration Testing
- [ ] 8.1 Test tool integration
  - [ ] Start server and verify all tools load
  - [ ] Verify 10 tools registered
- [ ] 8.2 Test use case scenario
  - [ ] Follow interaction script from specs/use-case.md (lines 43-52)
  - [ ] Verify tool chain: disruption → revenue impact → ROI
  - [ ] Verify regulatory updates and compliance costs
  - [ ] Verify outputs align with use case expectations
- [ ] 8.3 Test complete workflow
  - [ ] Risk assessment → disruption → inventory → carrying costs → ROI
  - [ ] Regulatory updates → compliance costs
  - [ ] End-to-end data flow validation

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
- [ ] calculate_revenue_impact tool works correctly
- [ ] calculate_roi tool works correctly
- [ ] get_regulatory_updates tool works correctly
- [ ] calculate_compliance_costs tool works correctly
- [ ] Tools return structured, AI-readable responses
- [ ] Can demo use case scenario from specs/use-case.md (lines 43-52)

### Gaps/Issues
*To be filled in during sprint review*

### Next Steps
*To be filled in during sprint review*

## Progress Notes

*Add progress notes, observations, code snippets, or commit references below*

---

### Day 1
*Notes to be added during sprint execution*

