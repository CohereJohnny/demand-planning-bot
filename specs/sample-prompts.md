# Sample Prompts for Demand Planning Assistant Testing

## Category 1: Basic Information Queries

### Market Data
```
What is the current price of Brent crude oil?
```
**Expected**: Single tool call to `get_market_prices`, concise price with date and citation.

```
Show me the current prices for both Brent and WTI.
```
**Expected**: Parallel tool calls, comparative data presentation.

```
What were oil prices over the past week?
```
**Expected**: Tool call with timeframe="recent", trend analysis if data available.

---

## Category 2: Risk Assessment

### Geopolitical Risks
```
What are the current geopolitical risks in the Strait of Hormuz?
```
**Expected**: Tool call to `get_geopolitical_risk_assessment`, risk level with supporting evidence, news headlines.

```
Are there any supply chain risks I should be aware of in the Middle East?
```
**Expected**: Risk assessment with specific regions, confidence level, threat indicators.

```
How does the situation in the Persian Gulf affect our oil supply security?
```
**Expected**: Risk assessment + context about supply routes, potential impact explanation.

---

## Category 3: Supply Chain Disruption Analysis

### Scenario Modeling
```
If the Strait of Hormuz closes for 7 days, what would be the impact on a refinery processing 100,000 barrels per day?
```
**Expected**: `simulate_supply_disruption` call, quantified barrels lost, financial impact, alternative route suggestions.

```
Model a 10-day pipeline outage affecting our Rotterdam refinery with 400,000 barrel daily capacity.
```
**Expected**: Supply disruption simulation with specific parameters, impact metrics.

```
What happens if there's a 2-week disruption to our Singapore operations processing 250,000 barrels daily?
```
**Expected**: Simulation + impact analysis with multiple metrics (volume lost, cost impact).

---

## Category 4: Inventory Planning

### Safety Stock Calculations
```
Calculate inventory requirements for 150,000 barrels daily demand with 95% service level and 10-day lead time.
```
**Expected**: `calculate_inventory_requirements` with clear parameters, specific barrel recommendation.

```
How much safety stock should I maintain for our European operations if we face medium risk and need 99% service level?
```
**Expected**: Inventory calculation with risk factor adjustment, justification for recommendation.

```
What inventory levels would you recommend to maintain operations during a potential Strait of Hormuz closure?
```
**Expected**: Multi-step: risk assessment → disruption modeling → inventory calculation → final recommendation.

---

## Category 5: Financial Analysis

### Cost Calculations
```
What are the carrying costs for storing an additional 2 million barrels at $75 per barrel per month?
```
**Expected**: `calculate_carrying_costs` with breakdown of monthly/annual costs.

```
Calculate the revenue impact if we have a 5-day stockout with 100,000 barrels daily demand at current market prices.
```
**Expected**: Market price lookup + revenue impact calculation, total loss quantified.

```
What's the ROI for investing $3 million to increase inventory capacity, expecting $800,000 annual savings?
```
**Expected**: `calculate_roi` with ROI percentage, payback period, recommendation.

---

## Category 6: Regulatory Compliance

### Compliance Updates
```
Are there any new sulfur emission regulations affecting maritime fuel shipments?
```
**Expected**: `get_regulatory_updates` filtered by regulation_type="sulfur", relevant regulations listed.

```
What are the upcoming carbon regulations for global shipping?
```
**Expected**: Regulatory updates for carbon/GHG, effective dates, regional scope.

```
How much would it cost to comply with IMO sulfur caps using low-sulfur fuel for a fleet of 5 vessels consuming 10,000 tons annually?
```
**Expected**: Regulatory updates + `calculate_compliance_costs` with specific strategy and fleet parameters.

---

## Category 7: Comprehensive Multi-Step Workflows

### Full Demand Planning Session
```
I need to update our Q4 forecast. Can you assess geopolitical risks in the Strait of Hormuz, model potential disruptions, and recommend inventory levels?
```
**Expected**: 
1. Risk assessment (geopolitical_risk_assessment)
2. Supply disruption modeling (simulate_supply_disruption)
3. Inventory recommendations (calculate_inventory_requirements)
4. Financial justification (carrying_costs + revenue_impact)
5. Structured summary with action items

### Investment Justification
```
We're considering increasing safety stock by 1.5 million barrels to mitigate supply risks. Can you help me build a business case?
```
**Expected**:
1. Current risk assessment
2. Carrying cost calculation for additional inventory
3. Revenue impact calculation for potential stockouts without additional stock
4. ROI calculation comparing investment vs. risk mitigation
5. Recommendation with confidence level

### Crisis Response
```
Our primary supplier just announced a 10-day shutdown. We have 150,000 barrels daily demand and 5 days of inventory. What should we do?
```
**Expected**:
1. Immediate impact assessment (gap: 10 days needed - 5 days available = 5-day shortfall)
2. Disruption simulation for quantification
3. Revenue impact if no action taken
4. Emergency inventory acquisition recommendation
5. Alternative supplier or route suggestions
6. Urgency indicator in response

---

## Category 8: Clarification Scenarios

### Ambiguous Requests
```
What's the risk situation?
```
**Expected**: Clarifying question - "Which region or supply route are you concerned about?"

```
Calculate inventory needs.
```
**Expected**: Request for critical parameters - "To calculate inventory requirements, I need: daily demand volume, lead time, and desired service level."

```
How much will it cost?
```
**Expected**: Clarification - "What cost are you looking to estimate? Options include: carrying costs, compliance costs, or revenue impact from disruptions."

---

## Category 9: Edge Cases & Error Handling

### Out of Scope
```
What's the weather forecast for Singapore next week?
```
**Expected**: Polite refusal - "I specialize in Oil & Gas supply chain and demand planning. For weather forecasts, I recommend checking [weather service]."

```
Can you help me with my personal investment portfolio?
```
**Expected**: Scope clarification - "I focus on Oil & Gas supply chain analysis. For personal investment advice, please consult a financial advisor."

### Missing Data
```
Get me oil prices.
```
**Expected**: Clarification - "I can get current oil prices. Which product would you like: Brent crude or WTI?"

---

## Category 10: Complex Reasoning

### Trade-offs Analysis
```
Should I increase inventory or accept higher stockout risk? Current prices are at 5-year highs.
```
**Expected**:
1. Market price confirmation (get_market_prices)
2. Carrying cost calculation at current high prices
3. Revenue impact calculation for stockout scenarios
4. Trade-off analysis with recommendation
5. Sensitivity analysis (e.g., "if prices drop by 20%...")

### Multi-Region Planning
```
Compare inventory strategies for our Rotterdam and Singapore refineries considering regional risks and costs.
```
**Expected**:
1. Geopolitical risk assessment for both regions (Europe vs. Asia)
2. Supply disruption modeling for each
3. Inventory requirements calculation for both
4. Comparative cost analysis
5. Region-specific recommendations in table format

---

## Category 11: Follow-up & Context Awareness

### Building on Previous Context
```
[First] What's the current risk in the Strait of Hormuz?
[Then] How would a 7-day closure affect our operations?
[Then] What inventory levels do you recommend?
[Finally] Show me the ROI for that inventory investment.
```
**Expected**: Each follow-up should build on previous context, maintaining conversation continuity, referring back to earlier calculations.

---

## Testing Checklist

Use these prompts to verify:
- ✅ Tool selection accuracy
- ✅ Data source citations
- ✅ Multi-step reasoning
- ✅ Parallel tool calls
- ✅ Clarification requests when needed
- ✅ Scope boundary enforcement
- ✅ Confidence level communication
- ✅ Output formatting consistency
- ✅ Context retention across turns
- ✅ Error handling gracefully

---

**Note**: These prompts are designed to test both happy paths and edge cases. For production testing, randomize the order and combine prompts to create realistic conversation flows.

