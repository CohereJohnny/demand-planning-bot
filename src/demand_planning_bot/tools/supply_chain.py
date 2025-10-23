"""Supply chain disruption simulation tools for the Demand Planning Bot.

This module provides tools to simulate supply chain disruptions and calculate
their impacts on refinery operations, costs, and timelines.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Literal, Optional

from src.demand_planning_bot.utils.config import Config

logger = logging.getLogger(__name__)


# Disruption scenario models
DISRUPTION_MODELS = {
    "strait_of_hormuz_closure": {
        "name": "Strait of Hormuz Closure",
        "description": (
            "Complete closure of the Strait of Hormuz due to geopolitical tensions. "
            "Approximately 21% of global petroleum liquids pass through this chokepoint. "
            "Impacts Middle East crude exports to Europe and Asia."
        ),
        "affected_regions": ["Middle East", "Persian Gulf"],
        "typical_duration_days": 14,
        "severity": "high",
        "alternative_routes": [
            "Suez Canal via Red Sea (adds 10-14 days, limited capacity)",
            "Cape of Good Hope around Africa (adds 20-30 days)",
            "Increased West African crude procurement",
        ],
    },
    "pipeline_outage": {
        "name": "Pipeline Outage",
        "description": (
            "Major pipeline disruption affecting crude transport from production "
            "to loading terminals or refineries. Can be due to technical failure, "
            "maintenance, or sabotage."
        ),
        "affected_regions": ["Pipeline corridor"],
        "typical_duration_days": 7,
        "severity": "medium",
        "alternative_routes": [
            "Rail transport (higher cost, lower volume)",
            "Trucking (limited capacity, high cost)",
            "Alternative pipeline routes if available",
        ],
    },
    "port_closure": {
        "name": "Port Closure",
        "description": (
            "Temporary closure of a major oil loading or receiving port due to "
            "weather, labor strikes, accidents, or security concerns."
        ),
        "affected_regions": ["Port region"],
        "typical_duration_days": 5,
        "severity": "medium",
        "alternative_routes": [
            "Divert shipments to nearby ports",
            "Wait for port reopening",
            "Storage at alternative locations",
        ],
    },
    "weather_event": {
        "name": "Severe Weather Event",
        "description": (
            "Hurricane, typhoon, or extreme weather affecting offshore production "
            "or shipping routes. Can cause temporary shutdowns of platforms and refineries."
        ),
        "affected_regions": ["Weather-affected region"],
        "typical_duration_days": 3,
        "severity": "low",
        "alternative_routes": [
            "Route around affected areas (adds 3-7 days)",
            "Delay shipments until weather clears",
            "Draw from strategic reserves",
        ],
    },
}

# Refinery data
REFINERY_DATA = {
    "rotterdam": {
        "name": "Rotterdam Refinery",
        "location": "Rotterdam, Netherlands",
        "capacity_barrels_per_day": 400000,
        "primary_feedstock_sources": ["North Sea", "Middle East via Suez", "West Africa"],
        "typical_inventory_days": 30,
        "transit_time_days": {
            "Middle East (Strait of Hormuz)": 21,
            "North Sea": 3,
            "West Africa": 14,
        },
    },
    "singapore": {
        "name": "Singapore Refinery",
        "location": "Singapore",
        "capacity_barrels_per_day": 500000,
        "primary_feedstock_sources": ["Middle East via Strait", "Southeast Asia", "Australia"],
        "typical_inventory_days": 25,
        "transit_time_days": {
            "Middle East (Strait of Hormuz)": 14,
            "Southeast Asia": 5,
            "Australia": 10,
        },
    },
}


def calculate_disruption_impact(
    disruption_type: str, refinery: str, duration_days: int, config: Config
) -> Dict:
    """Calculate the impact of a disruption on a specific refinery.

    Args:
        disruption_type: Type of disruption (e.g., "strait_of_hormuz_closure").
        refinery: Refinery identifier (e.g., "rotterdam", "singapore").
        duration_days: Expected duration of the disruption in days.
        config: Application configuration.

    Returns:
        Dictionary with impact analysis including shortage percentage,
        cost increases, timeline, and mitigation options.
    """
    disruption = DISRUPTION_MODELS.get(disruption_type, {})
    refinery_info = REFINERY_DATA.get(refinery, {})

    if not disruption or not refinery_info:
        logger.warning(
            f"Unknown disruption type or refinery: {disruption_type}, {refinery}"
        )
        return {
            "error": f"Unknown disruption type '{disruption_type}' or refinery '{refinery}'",
        }

    # Calculate feedstock shortage
    # Assumption: For Strait of Hormuz, 40-60% of feedstock typically comes from Middle East
    # For other disruptions, impact depends on specific affected route
    shortage_percentage = 0.0
    cost_increase_percentage = 0.0
    days_until_impact = 0

    if disruption_type == "strait_of_hormuz_closure":
        if refinery == "rotterdam":
            # Rotterdam gets ~50% from Middle East via Suez/Strait
            shortage_percentage = 50.0
            cost_increase_percentage = 25.0  # Alternative routes are more expensive
            days_until_impact = refinery_info["typical_inventory_days"]
        elif refinery == "singapore":
            # Singapore gets ~70% from Middle East via Strait
            shortage_percentage = 70.0
            cost_increase_percentage = 35.0
            days_until_impact = refinery_info["typical_inventory_days"]
    elif disruption_type == "pipeline_outage":
        # Moderate impact, depends on pipeline importance
        shortage_percentage = 30.0
        cost_increase_percentage = 15.0
        days_until_impact = 7
    elif disruption_type == "port_closure":
        # Localized impact, can usually divert
        shortage_percentage = 20.0
        cost_increase_percentage = 10.0
        days_until_impact = 5
    elif disruption_type == "weather_event":
        # Short-term, manageable impact
        shortage_percentage = 15.0
        cost_increase_percentage = 5.0
        days_until_impact = 3

    # Calculate cost impact based on refinery capacity
    daily_capacity = refinery_info["capacity_barrels_per_day"]
    barrels_affected = daily_capacity * (shortage_percentage / 100) * duration_days
    # Assume $80/barrel baseline; cost increase applies to replacement crude
    baseline_cost_per_barrel = 80.0
    additional_cost_per_barrel = baseline_cost_per_barrel * (cost_increase_percentage / 100)
    total_additional_cost = barrels_affected * additional_cost_per_barrel

    # Mitigation timeline
    mitigation_timeline = []
    current_date = datetime.now()
    mitigation_timeline.append(
        {
            "day": 0,
            "date": current_date.strftime("%Y-%m-%d"),
            "event": f"Disruption begins: {disruption['name']}",
        }
    )
    mitigation_timeline.append(
        {
            "day": days_until_impact,
            "date": (current_date + timedelta(days=days_until_impact)).strftime("%Y-%m-%d"),
            "event": f"{refinery_info['name']} begins to feel impact (inventory depleted)",
        }
    )
    mitigation_timeline.append(
        {
            "day": duration_days,
            "date": (current_date + timedelta(days=duration_days)).strftime("%Y-%m-%d"),
            "event": "Disruption ends (expected)",
        }
    )
    recovery_days = duration_days + 14  # Assume 2 weeks to restore normal operations
    mitigation_timeline.append(
        {
            "day": recovery_days,
            "date": (current_date + timedelta(days=recovery_days)).strftime("%Y-%m-%d"),
            "event": "Normal operations restored",
        }
    )

    return {
        "refinery": refinery_info["name"],
        "location": refinery_info["location"],
        "daily_capacity_barrels": daily_capacity,
        "feedstock_shortage_percentage": shortage_percentage,
        "procurement_cost_increase_percentage": cost_increase_percentage,
        "barrels_affected": round(barrels_affected, 0),
        "additional_procurement_cost_usd": round(total_additional_cost, 2),
        "days_until_impact": days_until_impact,
        "mitigation_timeline": mitigation_timeline,
        "alternative_routes": disruption.get("alternative_routes", []),
    }


def get_simulate_supply_disruption_tool(config: Config):
    """Provides an MCP tool to simulate supply chain disruptions.

    Args:
        config: The application configuration.

    Returns:
        A callable MCP tool function.
    """

    def simulate_supply_disruption(
        disruption_type: Literal[
            "strait_of_hormuz_closure", "pipeline_outage", "port_closure", "weather_event"
        ] = "strait_of_hormuz_closure",
        affected_refineries: List[Literal["rotterdam", "singapore"]] = None,
        duration_days: int = 14,
    ) -> Dict:
        """Simulate supply chain disruption and calculate refinery impacts."""
        if affected_refineries is None:
            affected_refineries = ["rotterdam", "singapore"]

        logger.info(
            f"simulate_supply_disruption called: type={disruption_type}, "
            f"refineries={affected_refineries}, duration={duration_days}"
        )

        disruption = DISRUPTION_MODELS.get(disruption_type, {})
        if not disruption:
            return {
                "error": f"Unknown disruption type: {disruption_type}",
                "valid_types": list(DISRUPTION_MODELS.keys()),
            }

        # Calculate impact for each refinery
        refinery_impacts = []
        for refinery in affected_refineries:
            impact = calculate_disruption_impact(
                disruption_type, refinery, duration_days, config
            )
            if "error" not in impact:
                refinery_impacts.append(impact)

        result = {
            "disruption_type": disruption_type,
            "disruption_name": disruption["name"],
            "description": disruption["description"],
            "severity": disruption["severity"],
            "duration_days": duration_days,
            "affected_refineries": refinery_impacts,
            "confidence": "high",
            "assumptions": [
                "Baseline crude oil price: $80/barrel",
                f"Disruption lasts exactly {duration_days} days",
                "Refineries operate at full capacity pre-disruption",
                "Alternative routes available but at higher cost",
                "No strategic reserve releases modeled",
            ],
        }

        logger.info(
            f"Disruption simulation complete: {len(refinery_impacts)} refineries analyzed"
        )
        return result

    return simulate_supply_disruption

