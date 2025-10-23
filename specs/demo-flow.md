# Demand Planning Bot - Demo Flow Scripts

**Purpose**: Demonstration scripts showcasing AI-assisted demand planning for Oil & Gas supply chains using the MCP Demand Planning Bot with Cohere Command A Reasoning.

**Target Audience**: Supply chain executives, demand planners, operations managers

---

## Demo Overview

These conversation flows demonstrate:
- 🎯 Real-time market intelligence and risk assessment
- 📊 Supply chain disruption modeling
- 💰 Financial impact analysis and ROI calculations
- 📋 Regulatory compliance management
- 🤖 Multi-step reasoning with tool orchestration
- 💬 Natural conversation with contextual follow-ups

---

## Demo Flow 1: Strategic Q4 Planning Session
**Persona**: Sarah Thompson, Senior Demand Planning Analyst, PetroGlobal Energy  
**Scenario**: Quarterly planning with geopolitical risk considerations  
**Duration**: ~5 minutes  
**Tools Showcased**: Risk assessment, market data, supply disruption, inventory planning, financial analysis

### Opening Context
*"It's mid-October, and Sarah is preparing her Q4 demand forecast. Recent news about Middle East tensions has her concerned about supply chain risks."*

---

### Turn 1: Initial Risk Assessment
**Sarah**: I need to update our Q4 demand forecast. Can you assess the current geopolitical risks in the Strait of Hormuz and their potential impact on our operations?

**Expected Bot Response**:
```
🔍 Assessing geopolitical risks in the Strait of Hormuz...

📊 Risk Assessment Summary:
The Strait of Hormuz currently faces a **medium risk level** with a 30% probability of disruption, based on analysis of 12 recent news articles from the past week.

Key Findings:
- Risk Level: 🟡 Medium (30% probability)
- Threat Indicators: conflict, sanctions, tension, war
- News Sources: 12 articles analyzed from NewsAPI
- Confidence: High (real-time news data)
- Last Updated: October 23, 2025

Impact on Your Operations:
Given that 20% of global oil supply passes through the Strait of Hormuz, a disruption would:
- Spike Brent crude prices by an estimated 12-15% within 30 days
- Force use of longer alternative routes (Cape of Good Hope)
- Increase transit times by 10-14 days
- Raise procurement costs due to supply constraints

💡 Recommendation:
I suggest we model specific disruption scenarios for your Rotterdam and Singapore refineries to quantify the potential impact and determine appropriate inventory buffers.

📋 Data Source: NewsAPI real-time analysis
```

---

### Turn 2: Supply Chain Impact Modeling
**Sarah**: Good point. Let's run a scenario - if there's a 10-day closure of the Strait, what's the impact on our Singapore refinery that processes 250,000 barrels daily?

**Expected Bot Response**:
```
🔄 Simulating 10-day Strait of Hormuz closure impact...

📊 Supply Disruption Analysis:
Singapore Refinery Impact (250,000 barrels/day capacity)

Direct Impact:
- ❌ Barrels Lost: 2,500,000 barrels (10 days × 250,000/day)
- 📍 Region: Singapore (Asia Pacific hub)
- ⏱️ Duration: 10-day closure scenario
- 🚢 Alternative Routes: Available but at increased cost/time

Financial Implications:
- Lost Production Value: ~$150M (at current Brent prices of $60/barrel)
- Alternative Sourcing Premium: +15-20% cost increase
- Additional Transit Time: +12 days via Cape of Good Hope
- Increased Insurance Costs: War risk premium applies

Operational Constraints:
- Current Inventory Buffer: Likely 3-5 days at normal operations
- Gap to Cover: 5-7 additional days needed
- Alternative Suppliers: Middle East alternatives also affected

⚠️ Critical Finding:
Your Singapore operations would face a 5-7 day supply gap even with alternative routing, as most alternatives also originate from the affected region.

💡 Recommendations:
1. Increase safety stock to cover 15-day disruption (2.5x current risk)
2. Pre-position additional inventory at Singapore hub
3. Negotiate spot contracts with West African suppliers as backup
4. Consider temporary processing rate reduction to extend inventory

Would you like me to calculate the specific inventory requirements and associated costs?
```

---

### Turn 3: Inventory Planning
**Sarah**: Yes, calculate the inventory requirements to maintain 95% service level with this elevated risk, assuming 12-day lead time for alternative supplies.

**Expected Bot Response**:
```
📦 Calculating optimal inventory levels...

Inventory Requirements Analysis:
Based on: 250,000 barrels/day demand, 95% service level, 12-day lead time, high risk factor (30%)

📊 Recommended Safety Stock:
- Current Baseline Need: 3,000,000 barrels (12 days × 250,000/day)
- Safety Stock Addition: +1,856,250 barrels (high risk scenario)
- **Total Inventory Target: 4,856,250 barrels**
- Service Level Achievement: 95% (Z-score: 1.65)

Breakdown:
- Average Daily Demand: 250,000 barrels
- Lead Time: 12 days (alternative route via Cape)
- Risk Factor: High (1.5x multiplier for 30% disruption probability)
- Safety Buffer: 7.4 days additional coverage

💰 Cost Implications:
Let me calculate the carrying costs for this additional inventory...

Additional Inventory Carrying Costs:
- Additional Barrels: 1,856,250
- Current Brent Price: $60.71/barrel
- Monthly Carrying Rate: ~2% of inventory value
- **Monthly Cost: ~$2.26M**
- **3-Month Cost: ~$6.77M** (for Q4 elevated risk period)

Assumptions:
- Storage capacity available at Singapore hub
- Carrying cost includes: storage fees, insurance, capital cost, quality degradation
- Price volatility buffer included

💡 Investment Justification:
To justify this investment, let me calculate the potential revenue loss without this buffer...
```

---

### Turn 4: Financial Justification (Follow-up)
**Sarah**: Show me the ROI - what's the revenue at risk if we don't make this investment?

**Expected Bot Response**:
```
💰 Calculating revenue impact and ROI...

Revenue at Risk Analysis:
Scenario: 10-day stockout during Strait closure without additional inventory

📊 Financial Impact Without Buffer:
- Stockout Duration: 7 days (after existing 3-day buffer exhausted)
- Daily Demand Unmet: 250,000 barrels/day
- Price per Barrel: $60.71
- Customer Impact Factor: 1.2x (20% penalty for breach of contracts)

💸 Total Revenue Impact:
- Direct Revenue Loss: $106.2M (7 days × 250k × $60.71)
- Contract Penalties: $21.2M (20% penalty on unmet contracts)
- Customer Relationship Impact: ~$15M (estimated future business loss)
- **Total Potential Loss: $142.4M**

📈 ROI Calculation:
- Investment: $6.77M (3-month carrying costs for additional inventory)
- Risk Mitigation: $142.4M (potential loss avoided if scenario occurs)
- Probability-Weighted Benefit: $42.7M (30% risk probability × $142.4M)

**ROI Metrics:**
- **Return on Investment: 530%** (probability-weighted)
- **Break-even Probability: 4.8%** (any risk above this justifies investment)
- **Payback Period: Immediate** (if disruption occurs)
- **Risk-Adjusted NPV: +$35.9M** (3-month period, 30% probability)

🎯 Recommendation: **STRONGLY JUSTIFIED**
Even at a 30% disruption probability, the expected value of this investment is highly positive. The carrying costs of $6.77M are dwarfed by the probability-weighted risk mitigation benefit of $42.7M.

Additional Considerations:
- ✅ Meets regulatory prudent investor standards
- ✅ Protects customer relationships and contracts
- ✅ Provides flexibility for opportunistic spot sales if prices spike
- ✅ Can be drawn down post-Q4 if risk subsides

Would you like me to check for any relevant regulatory updates that might affect this decision?
```

---

### Turn 5: Regulatory Compliance Check
**Sarah**: Yes, check for any new maritime or environmental regulations that could impact our plan.

**Expected Bot Response**:
```
📋 Checking regulatory updates...

Relevant Maritime Regulations for Q4 2025:

🌊 IMO Sulfur Regulations (Currently Active):
- IMO 2020: Global 0.50% sulfur cap on marine fuels
- Status: In force
- Impact: Ongoing compliance required for marine transport
- Estimated Cost Impact: 8-12% premium on marine fuel costs

🌍 Carbon Intensity Regulations (Upcoming):
- IMO 2030 Target: 40% reduction in carbon intensity (vs 2008 baseline)
- Status: Implementation phase
- Your Timeline: Compliance required by January 2030
- Recommended Action: Begin tracking now for long-term planning

🇪🇺 EU Emissions Trading System (Active):
- EU ETS for Maritime: Applied to voyages within EU
- Status: Phase-in period (2024-2025)
- Impact on Rotterdam Operations: Direct cost per voyage
- Estimated Impact: €50-80 per ton CO2 for EU-bound vessels

💡 Immediate Q4 Considerations:
1. **Marine Fuel Costs**: Budget for 8-12% premium on alternative routing
2. **EU ETS Compliance**: Factor €50-80/ton CO2 for Rotterdam deliveries
3. **Documentation**: Ensure proper sulfur content certificates for all shipments

Cost Impact on Your Scenario:
- Alternative route (Cape of Good Hope) = +2,500 nautical miles
- Additional fuel consumption: ~400 tons per voyage
- Sulfur-compliant fuel premium: +10% = $40k per voyage
- EU ETS (if Rotterdam-bound): +€30k per voyage
- **Total Regulatory Premium: ~$70k per alternative-route voyage**

For your 10-day disruption scenario with weekly deliveries:
- Affected Voyages: ~1-2 ships
- Additional Regulatory Costs: $70-140k
- ℹ️ This is marginal compared to the $142M revenue risk

📋 Compliance Status: 
✅ No new regulations would block your proposed inventory strategy
⚠️ Factor the voyage premiums into your total Q4 budget
```

---

### Turn 6: Summary and Action Items
**Sarah**: Perfect. Summarize everything for my executive briefing.

**Expected Bot Response**:
```
📊 Executive Summary: Q4 Demand Planning - Strait of Hormuz Risk Mitigation

Prepared for: Sarah Thompson, Senior Demand Planning Analyst
Date: October 23, 2025
Focus: Singapore Refinery (250,000 barrels/day capacity)

🎯 SITUATION:
- Strait of Hormuz faces MEDIUM risk (30% disruption probability)
- 10-day closure scenario would impact 2.5M barrels production
- Current inventory insufficient to maintain service levels during crisis

💰 FINANCIAL ANALYSIS:
| Metric | Value | Impact |
|--------|-------|--------|
| Revenue at Risk | $142.4M | Without mitigation |
| Mitigation Investment | $6.77M | 3-month carrying costs |
| Probability-Weighted Benefit | $42.7M | Expected value |
| ROI | 530% | Highly justified |
| Payback Period | Immediate | If disruption occurs |

📦 RECOMMENDED ACTION:
Increase Singapore safety stock by 1.86M barrels to achieve:
- ✅ 95% service level during disruptions
- ✅ 15-day total coverage (12-day lead time + buffer)
- ✅ Contract compliance protection
- ✅ Customer relationship preservation

💡 IMPLEMENTATION:
1. **Immediate** (Next 2 weeks):
   - Authorize $6.77M for additional inventory
   - Confirm storage capacity at Singapore hub
   - Initiate spot purchases to build buffer

2. **Ongoing** (Q4):
   - Monitor Strait of Hormuz situation weekly
   - Track inventory levels against 4.86M barrel target
   - Review and adjust if risk probability changes

3. **Regulatory**:
   - Maintain sulfur-compliant fuel documentation
   - Budget additional $70-140k for EU ETS/fuel premiums if alternative routing needed

⚖️ RISK vs. REWARD:
- Break-even probability: 4.8% (current risk: 30%)
- **Decision confidence: HIGH**
- Strategic rationale: Prudent risk management with strong ROI

📋 SUPPORTING DATA:
- Geopolitical risk: NewsAPI analysis (12 articles, high confidence)
- Market prices: EIA API (Brent $60.71/barrel as of Oct 20, 2025)
- Calculations: Industry-standard inventory models, IMO regulatory database

🎯 NEXT STEPS:
1. Present to executive committee for budget approval
2. Coordinate with Singapore operations on storage logistics
3. Engage procurement for spot market contracts
4. Set up weekly risk monitoring dashboard

---

✅ **Analysis Complete** - All recommendations backed by real-time data and quantitative modeling.
Would you like me to generate any additional supporting materials or drill into any specific area?
```

---

## Demo Flow 2: Emergency Crisis Response
**Persona**: Mike Rodriguez, Operations Manager, Global Refining Corp  
**Scenario**: Urgent supply disruption requiring immediate action  
**Duration**: ~3 minutes  
**Tools Showcased**: Fast decision support, revenue impact, ROI

### Crisis Context
*"It's Monday morning. Mike just received news that their primary crude supplier's pipeline has ruptured and will be offline for 7 days. His European refinery has only 3 days of inventory."*

---

### Turn 1: Immediate Impact Assessment
**Mike**: URGENT - Our main supplier's pipeline is down for 7 days. We have 3 days of inventory for our 150,000 barrel/day refinery. What are my options?

**Expected Bot Response**:
```
🚨 URGENT: Supply Disruption - Immediate Analysis

Current Situation:
- ❌ Supply Interruption: 7 days
- 📦 Current Inventory: 3 days (450,000 barrels)
- 🏭 Daily Demand: 150,000 barrels/day
- ⏰ Supply Gap: 4 days (7 needed - 3 available)
- 🔴 Shortfall: 600,000 barrels

⏱️ Timeline:
- Day 1-3: Normal operations (existing inventory)
- **Day 4-7: CRITICAL GAP - 600,000 barrels needed**

💰 Revenue at Risk (without action):
Calculating immediate financial impact...

If No Action Taken:
- Lost Production: 600,000 barrels (4 days of stoppage)
- Current Brent Price: $60.71/barrel
- **Direct Revenue Loss: $36.4M**
- Contract Penalties: ~$7.3M (estimated 20%)
- Customer Impact: Additional relationship damage
- **Total Impact: $43.7M+**

🎯 IMMEDIATE OPTIONS:

**Option 1: Emergency Spot Market Purchase**
- Source: 600,000 barrels from spot market
- Estimated Premium: 15-20% above current prices (+$9/barrel)
- Cost: ~$42.3M (600k × $70.50/barrel with premium)
- Timeline: Can arrange within 48 hours if you act NOW
- ✅ Maintains full operations

**Option 2: Partial Production Cut**
- Reduce to 112,500 barrels/day (75% capacity)
- Extends inventory to cover 6 of 7 days
- Shortfall reduced to 150,000 barrels
- Revenue Impact: ~$9.1M + penalties
- ⚠️ Still need spot purchase but smaller

**Option 3: Full Shutdown Days 4-7**
- Zero production for 4 days
- Revenue Loss: $43.7M+ (calculated above)
- ❌ Highest financial and relationship damage
- ❌ NOT RECOMMENDED

📞 RECOMMENDED IMMEDIATE ACTIONS:
1. **NOW**: Call spot market brokers for 600k barrel emergency purchase
2. **Hour 1**: Notify customers of potential impacts (transparency)
3. **Hour 2**: Confirm pricing and arrange logistics (priority shipping)
4. **Day 1**: Execute contracts and schedule deliveries
5. **Day 2**: First emergency shipments arrive (target: 300k barrels)

⏰ TIME IS CRITICAL: Spot market prices may increase as word spreads. Act in the next 2-4 hours for best pricing.

Would you like me to calculate the ROI for the emergency purchase versus accepting the shutdown?
```

---

### Turn 2: Quick ROI Decision Support
**Mike**: Yes, show me the numbers on the emergency purchase ROI.

**Expected Bot Response**:
```
💰 Emergency Purchase ROI Analysis

Investment Analysis:
- Emergency Purchase: 600,000 barrels @ $70.50/barrel (15% premium)
- Total Investment: $42.3M
- Timeline: Immediate (48-hour execution)

Revenue Protection:
- Revenue Preserved: $36.4M (600k barrels × $60.71/barrel)
- Penalties Avoided: $7.3M (contract breach penalties)
- Customer Relationships: Preserved (priceless)
- **Total Benefit: $43.7M**

📊 ROI Calculation:
- Net Benefit: $1.4M ($43.7M benefit - $42.3M cost)
- **ROI: 3.3%** (positive but thin margin)
- Break-even: Achieved (benefit > cost)
- Payback: Immediate (upon production)

⚖️ DECISION FACTORS:

Financial:
- ✅ Positive ROI (saves $1.4M vs. shutdown)
- ✅ Avoids penalty cascade (future contract implications)
- ✅ Maintains cash flow from ongoing operations

Strategic:
- ✅✅ Preserves customer trust and contracts
- ✅✅ Maintains workforce productivity
- ✅ Demonstrates operational resilience
- ✅ Avoids reputation damage

Hidden Costs of Shutdown:
- Restart costs: ~$500k (equipment, QA, safety checks)
- Lost productivity: ~$1M (workforce idle time)
- Supply chain disruption: Ripple effects
- **Real shutdown cost: $45M+** (not just $43.7M)

🎯 CLEAR RECOMMENDATION: **EXECUTE EMERGENCY PURCHASE**

Adjusted ROI with Hidden Costs:
- True Cost of Shutdown: $45M+
- Emergency Purchase Cost: $42.3M
- **Net Savings: $2.7M+**
- **True ROI: 6.4%+**

📞 NEXT STEPS (PRIORITY ORDER):
1. ✅ Authorize $42.3M emergency procurement (NOW)
2. ✅ Contact top 3 spot market suppliers (within 1 hour)
3. ✅ Arrange expedited shipping (premium freight acceptable)
4. ✅ Brief customers proactively (maintain transparency)
5. ⏸️ Put production cut plans on standby (backup if procurement fails)

⏰ Decision Window: Next 2 hours for optimal pricing
📞 Escalate to CFO: Yes (amount exceeds standard authorization)

🔒 CONFIDENCE LEVEL: **HIGH** - Emergency purchase is financially and strategically sound.
```

---

## Demo Flow 3: Multi-Region Strategic Planning
**Persona**: Jennifer Chen, VP Supply Chain Strategy, EuroAsia Energy  
**Scenario**: Comparative analysis for multi-region inventory strategy  
**Duration**: ~4 minutes  
**Tools Showcased**: Parallel analysis, comparison, strategic decision support

### Turn 1: Multi-Region Risk Assessment
**Jennifer**: I need to compare geopolitical risks and inventory strategies for our Rotterdam and Singapore operations. Show me current risk levels for both regions.

**Expected Bot Response**:
```
🌍 Multi-Region Risk Assessment

Analyzing geopolitical risks for your key operational regions...

📊 Regional Risk Comparison:

**Europe (Rotterdam Hub):**
- Primary Risk: Russia-Ukraine situation, North Sea weather
- Risk Level: 🟢 Low-Medium (15-20% disruption probability)
- Supply Routes: North Sea, North Africa, transatlantic
- Key Concerns: Winter weather, EU energy policy
- Supply Diversity: High (multiple sources, short routes)

**Asia-Pacific (Singapore Hub):**
- Primary Risk: Strait of Hormuz, South China Sea tensions
- Risk Level: 🟡 Medium (30% disruption probability)
- Supply Routes: Middle East (Strait of Hormuz), Indonesia, Australia
- Key Concerns: Geopolitical tensions, typhoon season
- Supply Diversity: Medium-High (concentrated in Middle East)

🎯 Comparative Analysis:

| Factor | Rotterdam | Singapore | Winner |
|--------|-----------|-----------|--------|
| Risk Level | 15-20% | 30% | Rotterdam |
| Supply Route Length | Shorter | Longer | Rotterdam |
| Alternative Routes | Many | Limited | Rotterdam |
| Weather Risk | Winter storms | Typhoons | Tie |
| Political Stability | Higher | Medium | Rotterdam |
| Market Proximity | EU market | Asia growth | Context-dependent |

💡 Strategic Implications:
- Singapore requires **higher safety stock** due to elevated risk (30% vs 15-20%)
- Rotterdam can operate with **lower buffers** but needs winter weather contingency
- Combined portfolio: **Diversified risk** (different threat vectors)

Would you like me to calculate optimal inventory levels for each region based on these risk profiles?
```

---

### Turn 2: Parallel Inventory Calculations
**Jennifer**: Yes, calculate inventory requirements for both. Rotterdam processes 400,000 barrels/day and Singapore does 250,000. Both need 95% service level.

**Expected Bot Response**:
```
📦 Multi-Region Inventory Strategy

Calculating optimal inventory for both operations in parallel...

**Rotterdam Refinery Analysis:**
Capacity: 400,000 barrels/day | Risk Level: Medium-Low (18%) | Target: 95% service level

Recommended Inventory:
- Base Lead Time Demand: 4,800,000 barrels (12-day lead time × 400k/day)
- Safety Stock: +1,654,080 barrels (medium risk multiplier)
- **Total Target: 6,454,080 barrels**
- Coverage: ~16 days total

Carrying Costs (3 months):
- Additional Inventory: 1,654,080 barrels
- Price: $60.71/barrel
- **Quarterly Cost: $6.02M**

---

**Singapore Refinery Analysis:**
Capacity: 250,000 barrels/day | Risk Level: Medium-High (30%) | Target: 95% service level

Recommended Inventory:
- Base Lead Time Demand: 3,000,000 barrels (12-day lead time × 250k/day)
- Safety Stock: +1,856,250 barrels (high risk multiplier)
- **Total Target: 4,856,250 barrels**
- Coverage: ~19 days total

Carrying Costs (3 months):
- Additional Inventory: 1,856,250 barrels
- Price: $60.71/barrel
- **Quarterly Cost: $6.77M**

---

📊 **PORTFOLIO SUMMARY:**

| Metric | Rotterdam | Singapore | Combined |
|--------|-----------|-----------|----------|
| Daily Capacity | 400,000 bbls | 250,000 bbls | 650,000 bbls |
| Total Inventory | 6.45M bbls | 4.86M bbls | 11.31M bbls |
| Additional Stock | 1.65M bbls | 1.86M bbls | 3.51M bbls |
| Q4 Cost | $6.02M | $6.77M | **$12.79M** |
| Coverage Days | 16 days | 19 days | Avg: 17 days |
| Risk Mitigation | ✅ Adequate | ✅✅ Strong | ✅ Diversified |

💰 **TOTAL Q4 INVESTMENT: $12.79M**

🎯 Strategic Advantages of This Allocation:
1. **Risk-Appropriate**: Higher buffer for higher-risk Singapore
2. **Portfolio Diversification**: Different risk vectors, different coverages
3. **Operational Flexibility**: Can shift between regions if needed
4. **Market Responsiveness**: Can capitalize on spot opportunities at either hub

📈 Expected Benefits:
- Revenue Protection: ~$250M across both facilities
- Service Level Achievement: 95% at both locations
- Customer Satisfaction: Maintained during disruptions
- Strategic Flexibility: Enhanced operational resilience

Would you like me to calculate the combined ROI and compare different allocation strategies?
```

---

### Turn 3: Strategic Allocation Analysis
**Jennifer**: Show me the ROI and suggest if we should allocate differently based on risk levels.

**Expected Bot Response**:
```
💰 Multi-Region ROI Analysis & Strategic Allocation

Current Allocation ROI:
- Total Investment: $12.79M (Q4 carrying costs)
- Combined Revenue at Risk: $246M (weighted by probabilities)
- Probability-Weighted Benefit: $61.8M
- **Portfolio ROI: 383%** (excellent)
- Risk-Adjusted NPV: +$49M

---

🎲 Alternative Allocation Strategies:

**Strategy 1: CURRENT (Risk-Proportional)**
- Rotterdam: 16 days coverage | Singapore: 19 days coverage
- Investment: $12.79M
- Risk Coverage: Matched to threat levels
- ✅ Recommended: Yes (current strategy is optimal)

**Strategy 2: EQUAL COVERAGE (17 days both)**
- Rotterdam: 17 days | Singapore: 17 days
- Investment: $12.52M (saves $270k)
- Risk Coverage: Over-insured Rotterdam, under-insured Singapore
- ⚠️ Risk: Singapore shortfall during crisis
- Verdict: **NOT RECOMMENDED** (penny-wise, pound-foolish)

**Strategy 3: HEAVY ASIA (focus on higher risk)**
- Rotterdam: 14 days | Singapore: 22 days
- Investment: $13.21M (+$420k)
- Risk Coverage: Excellent Singapore, acceptable Rotterdam
- ✅ Viable if: Asia growth justifies premium
- Verdict: **VIABLE ALTERNATIVE** for aggressive Asia strategy

**Strategy 4: COST MINIMIZATION (reduce both)**
- Rotterdam: 14 days | Singapore: 16 days
- Investment: $10.18M (saves $2.61M)
- Risk Coverage: Below optimal for both
- ⚠️ Risk: Service level drops to ~92%
- Verdict: **RISKY** - savings not worth service degradation

---

📊 Comparative Analysis:

| Strategy | Cost | Risk Coverage | Service Level | Recommendation |
|----------|------|---------------|---------------|----------------|
| Current (Risk-Match) | $12.79M | Optimal | 95% both | ✅✅ **BEST** |
| Equal Coverage | $12.52M | Suboptimal | 94% Sing | ⚠️ Risky |
| Heavy Asia | $13.21M | Strong Asia | 96% Sing | ✅ If growth-focused |
| Cost Minimize | $10.18M | Below target | 92% both | ❌ Not recommended |

🎯 **RECOMMENDATION: Stick with Current Strategy**

Rationale:
1. **Risk-Appropriate**: Matches investment to threat levels
2. **Cost-Efficient**: Not over-insuring low-risk regions
3. **Service Level**: Achieves 95% target at both locations
4. **Flexibility**: Provides operational headroom without waste
5. **ROI**: Strong 383% return validates allocation

💡 Strategic Insights:
- Rotterdam's lower risk allows for leaner operations (competitive advantage)
- Singapore's higher buffer protects your fastest-growing market (Asia-Pacific)
- Portfolio effect: Uncorrelated risks provide natural diversification
- You're appropriately balancing cost vs. risk vs. growth

🔄 Rebalancing Triggers:
Monitor and rebalance if:
- ⬆️ Rotterdam risk increases above 25% (add 2-3 days coverage)
- ⬇️ Singapore risk drops below 20% (can reduce by 2 days)
- 📈 Asia growth accelerates (consider Strategy 3: Heavy Asia)
- 💵 Capital constraints (reduce Singapore first to 17 days if needed)

✅ **DECISION: Approve current $12.79M allocation** - Strategy is sound and well-justified.

Next Steps:
1. Present to finance for Q4 budget approval
2. Coordinate with regional ops on storage logistics
3. Set up quarterly rebalancing review
4. Monitor risk indicators monthly
```

---

## Demo Flow 4: Regulatory Compliance Planning
**Persona**: David Park, Environmental Compliance Officer, Pacific Maritime Energy  
**Scenario**: Planning for upcoming regulatory changes  
**Duration**: ~3 minutes  
**Tools Showcased**: Regulatory updates, compliance costs

### Turn 1: Regulatory Landscape Scan
**David**: We're planning our 2026 budget. What are the upcoming carbon and sulfur regulations that will affect our fleet of 8 vessels?

**Expected Bot Response**:
```
📋 Regulatory Compliance Scan - 2026 Budget Planning

Analyzing current and upcoming regulations affecting maritime fuel operations...

🌊 SULFUR REGULATIONS (Currently Active):

**IMO 2020 - Global Sulfur Cap:**
- Requirement: Max 0.50% sulfur content in marine fuels (global)
- Status: ✅ Currently enforced worldwide
- Your Impact: Ongoing compliance costs
- ECAs (Emission Control Areas): 0.10% limit in specific zones

**Compliance Status for Your Fleet (8 vessels):**
- Current Strategy: Required to specify
- Options:
  1. Low-Sulfur Fuel Oil (LSFO) - 0.50% compliant
  2. Ultra-Low-Sulfur Fuel (ULSF) - 0.10% for ECAs
  3. Scrubbers - allows continued use of HSFO

---

🌍 CARBON/GHG REGULATIONS (Active & Upcoming):

**IMO 2023 - Carbon Intensity Indicator (CII):**
- Status: ✅ Currently active
- Requirement: Annual carbon intensity rating (A-E scale)
- Impact: Poor ratings (D/E) may face restrictions
- Your Action: Must report and improve ratings

**IMO 2030 - Carbon Intensity Target:**
- Requirement: 40% reduction vs. 2008 baseline
- Status: ⚠️ Implementation phase (5 years away)
- Your Timeline: Begin planning now
- Recommended: Gradual improvements to avoid shock in 2030

**EU ETS for Maritime (Active 2024-2026):**
- Coverage: All voyages within EU, 50% of international voyages
- Status: ✅ Phase-in period (2024-2026)
- Mechanism: Pay for CO2 emissions via allowance purchases
- Current Price: €50-80 per ton CO2
- **Your Exposure: Depends on EU route frequency**

**IMO 2050 - Net Zero Target:**
- Requirement: Net-zero GHG emissions by 2050
- Status: Long-term planning horizon
- Your Action: Start evaluating alternative fuels

---

💰 **ESTIMATED 2026 BUDGET IMPACTS:**

For Your 8-Vessel Fleet:
Assuming average fuel consumption: 10,000 tons/vessel/year = 80,000 tons total

**Sulfur Compliance:**
- Low-Sulfur Fuel Premium: +$50-100/ton vs. HSFO
- Annual Cost: $4.0M - $8.0M (premium only)
- OR Scrubbers: $4M-6M upfront per vessel = $32-48M capital

**Carbon Compliance (EU ETS):**
- CO2 Emissions: ~250,000 tons CO2/year (typical for 80k tons fuel)
- EU Exposure: Estimate 40% of voyages = 100,000 tons CO2
- Allowance Cost: €60/ton × 100,000 tons = €6M
- **2026 Budget Impact: ~$6.5M** (at current exchange rates)

**CII Compliance:**
- Efficiency Improvements: $500k-1M/vessel for upgrades
- Total: $4M-8M (one-time or staged)
- Operational Changes: Speed reduction, route optimization (revenue impact)

---

📊 **2026 TOTAL COMPLIANCE BUDGET:**

| Category | Low Estimate | High Estimate | Recommended |
|----------|--------------|---------------|-------------|
| Sulfur (ongoing) | $4.0M | $8.0M | $6.0M |
| EU ETS (ongoing) | $5.5M | $7.5M | $6.5M |
| CII Improvements | $4.0M | $8.0M | $6.0M |
| **TOTAL 2026** | **$13.5M** | **$23.5M** | **$18.5M** |

Scrubber Alternative (if considering):
- Capital: $32M-48M (upfront)
- Payback: 3-5 years
- Risk: Future regulations may limit scrubber use

🎯 RECOMMENDATIONS FOR 2026 BUDGET:
1. **Immediate**: Budget $18.5M for compliance (mid-range estimate)
2. **Strategic**: Evaluate scrubber investment (separate analysis needed)
3. **Operational**: Implement CII improvement programs now (staged approach)
4. **Planning**: Begin alternative fuel feasibility studies for 2030+

Would you like me to calculate the costs for specific compliance strategies (e.g., scrubbers vs. low-sulfur fuel)?
```

---

## Demo Facilitation Notes

### Setup Checklist
- [ ] Verify MCP server is running (`uv run python server.py`)
- [ ] Verify client is working (`uv run python client.py`)
- [ ] Check API keys are configured (COHERE_API_KEY, EIA_API_KEY, NEWS_API_KEY)
- [ ] Test with ping command to verify tool connectivity
- [ ] Prepare to show tool calls and citations in real-time

### Demo Tips

**Pacing**:
- Flow 1 (Strategic): 5-6 minutes - Best for comprehensive showcase
- Flow 2 (Emergency): 3 minutes - Best for impact/urgency demonstration
- Flow 3 (Multi-Region): 4-5 minutes - Best for complexity handling
- Flow 4 (Regulatory): 3 minutes - Best for specialized use cases

**What to Highlight**:
- 🎯 **Tool Orchestration**: Watch how the bot chains multiple tools together
- 💬 **Natural Conversation**: Note the context retention across turns
- 📊 **Data Grounding**: Point out citations to EIA API, NewsAPI, calculations
- 🤖 **Reasoning**: Show the "thinking" and step-by-step logic
- 💰 **Business Value**: Emphasize ROI, risk mitigation, financial justification

**Customization**:
- Adjust company names, refinery locations to match audience
- Modify dollar amounts for different company sizes
- Focus on different tools based on audience interests (risk, financial, regulatory)
- Add or remove turns based on time available

### Technical Details to Mention

**For Technical Audiences**:
- Built on Model Context Protocol (MCP) - emerging standard
- Cohere Command A Reasoning model for advanced multi-step reasoning
- Real-time data from EIA (Energy Information Administration) and NewsAPI
- Tool schemas dynamically discovered from MCP server
- Async tool execution for performance

**For Business Audiences**:
- AI assistant with access to 10 specialized supply chain tools
- Real-time market intelligence (not static data)
- Industry-standard calculations for inventory, ROI, risk
- Transparent reasoning - shows work and cites sources
- Customizable for your specific operations

---

**End of Demo Flows**

*These scripts demonstrate the full capabilities of the Demand Planning Bot across various scenarios and personas. Each flow is designed to be modular - pick the ones most relevant to your audience.*

