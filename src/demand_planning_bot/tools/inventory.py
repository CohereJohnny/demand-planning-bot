"""Inventory optimization tools for the Demand Planning Bot.

This module provides tools to calculate inventory requirements (safety stock)
and carrying costs for inventory investments.
"""

import logging
import math
from typing import Dict, Literal

from src.demand_planning_bot.utils.config import Config

logger = logging.getLogger(__name__)


def calculate_safety_stock(
    demand_std_dev: float, lead_time_days: float, service_level: float = 0.95
) -> float:
    """Calculate safety stock using the z-score method.

    Formula: Safety Stock = z × σ × √L
    where:
        z = z-score for desired service level (e.g., 1.65 for 95%, 1.96 for 97.5%)
        σ = standard deviation of demand
        L = lead time in days

    Args:
        demand_std_dev: Standard deviation of daily demand (barrels).
        lead_time_days: Lead time for procurement in days.
        service_level: Desired service level (probability of not stocking out),
                      default 0.95 (95%).

    Returns:
        Safety stock quantity in barrels.
    """
    # Z-scores for common service levels
    z_scores = {
        0.90: 1.28,
        0.95: 1.65,
        0.975: 1.96,
        0.99: 2.33,
        0.999: 3.09,
    }

    # Find closest service level
    z = z_scores.get(service_level, 1.65)  # Default to 95%

    safety_stock = z * demand_std_dev * math.sqrt(lead_time_days)
    return safety_stock


def calculate_carrying_cost_components(
    inventory_barrels: float, duration_months: int, cost_per_barrel_month: float
) -> Dict:
    """Calculate carrying cost components for inventory.

    Args:
        inventory_barrels: Additional inventory to hold (barrels).
        duration_months: How long to hold the inventory (months).
        cost_per_barrel_month: Cost to store per barrel per month (USD).

    Returns:
        Dictionary with cost breakdown.
    """
    # Storage cost (physical warehousing)
    storage_cost_per_barrel_month = cost_per_barrel_month * 0.4  # 40% of total
    storage_cost = inventory_barrels * storage_cost_per_barrel_month * duration_months

    # Insurance cost (risk protection)
    insurance_cost_per_barrel_month = cost_per_barrel_month * 0.2  # 20% of total
    insurance_cost = (
        inventory_barrels * insurance_cost_per_barrel_month * duration_months
    )

    # Opportunity cost (capital tied up)
    # Assume $80/barrel * 5% annual rate / 12 months = $0.33/barrel/month
    opportunity_cost_per_barrel_month = cost_per_barrel_month * 0.4  # 40% of total
    opportunity_cost = (
        inventory_barrels * opportunity_cost_per_barrel_month * duration_months
    )

    total_cost = storage_cost + insurance_cost + opportunity_cost

    return {
        "storage_cost": round(storage_cost, 2),
        "insurance_cost": round(insurance_cost, 2),
        "opportunity_cost": round(opportunity_cost, 2),
        "total_carrying_cost": round(total_cost, 2),
    }


def get_calculate_inventory_requirements_tool(config: Config):
    """Provides an MCP tool to calculate inventory requirements.

    Args:
        config: The application configuration.

    Returns:
        A callable MCP tool function.
    """

    def calculate_inventory_requirements(
        current_inventory_barrels: float = 500000,
        daily_demand_barrels: float = 50000,
        demand_std_dev_barrels: float = 5000,
        lead_time_days: float = 21,
        risk_level: Literal["low", "medium", "high"] = "medium",
    ) -> Dict:
        """Calculate inventory requirements based on demand and risk."""
        logger.info(
            f"calculate_inventory_requirements called: current={current_inventory_barrels}, "
            f"demand={daily_demand_barrels}, lead_time={lead_time_days}, risk={risk_level}"
        )

        # Adjust service level based on risk
        service_level_map = {
            "low": 0.95,  # 95% service level (z=1.65)
            "medium": 0.975,  # 97.5% service level (z=1.96)
            "high": 0.99,  # 99% service level (z=2.33)
        }
        service_level = service_level_map[risk_level]

        # Calculate safety stock
        safety_stock = calculate_safety_stock(
            demand_std_dev=demand_std_dev_barrels,
            lead_time_days=lead_time_days,
            service_level=service_level,
        )

        # Calculate days of supply in current inventory
        days_of_supply = current_inventory_barrels / daily_demand_barrels

        # Calculate additional storage needed
        # Baseline: maintain lead time + safety stock
        baseline_inventory = (daily_demand_barrels * lead_time_days) + safety_stock
        additional_storage = max(0, baseline_inventory - current_inventory_barrels)

        # Calculate percentage increase
        if current_inventory_barrels > 0:
            increase_percentage = (additional_storage / current_inventory_barrels) * 100
        else:
            increase_percentage = 0

        result = {
            "current_inventory_barrels": round(current_inventory_barrels, 0),
            "current_days_of_supply": round(days_of_supply, 1),
            "daily_demand_barrels": round(daily_demand_barrels, 0),
            "lead_time_days": lead_time_days,
            "risk_level": risk_level,
            "service_level_percentage": service_level * 100,
            "recommended_safety_stock_barrels": round(safety_stock, 0),
            "additional_storage_needed_barrels": round(additional_storage, 0),
            "safety_stock_increase_percentage": round(increase_percentage, 1),
            "rationale": (
                f"To maintain {service_level * 100:.1f}% service level under {risk_level} "
                f"risk conditions with {lead_time_days} day lead time, an additional "
                f"{round(additional_storage, 0)} barrels of safety stock is recommended. "
                f"This ensures sufficient buffer against demand variability and supply disruptions."
            ),
            "formula_used": "Safety Stock = z × σ × √L (z-score method)",
            "assumptions": [
                "Demand follows normal distribution",
                f"Standard deviation of demand: {demand_std_dev_barrels} barrels/day",
                "Lead time is constant",
                "No supply disruptions beyond modeled risk",
                "Safety stock covers demand variability during lead time",
            ],
            "confidence": "high",
        }

        logger.info(
            f"Inventory calculation complete: {round(safety_stock, 0)} barrels safety stock recommended"
        )
        return result

    return calculate_inventory_requirements


def get_calculate_carrying_costs_tool(config: Config):
    """Provides an MCP tool to calculate inventory carrying costs.

    Args:
        config: The application configuration.

    Returns:
        A callable MCP tool function.
    """

    def calculate_carrying_costs(
        inventory_increase_barrels: float = 100000,
        duration_months: int = 3,
        cost_per_barrel_month: float = 1.5,
    ) -> Dict:
        """Calculate carrying costs for additional inventory."""
        logger.info(
            f"calculate_carrying_costs called: inventory={inventory_increase_barrels}, "
            f"duration={duration_months}, cost_per_barrel={cost_per_barrel_month}"
        )

        # Calculate cost components
        costs = calculate_carrying_cost_components(
            inventory_barrels=inventory_increase_barrels,
            duration_months=duration_months,
            cost_per_barrel_month=cost_per_barrel_month,
        )

        monthly_cost = costs["total_carrying_cost"] / duration_months

        result = {
            "inventory_increase_barrels": round(inventory_increase_barrels, 0),
            "duration_months": duration_months,
            "cost_per_barrel_month": cost_per_barrel_month,
            "currency": "USD",
            "storage_cost_usd": costs["storage_cost"],
            "insurance_cost_usd": costs["insurance_cost"],
            "opportunity_cost_usd": costs["opportunity_cost"],
            "total_carrying_cost_usd": costs["total_carrying_cost"],
            "monthly_carrying_cost_usd": round(monthly_cost, 2),
            "cost_breakdown": {
                "storage_percentage": 40,
                "insurance_percentage": 20,
                "opportunity_cost_percentage": 40,
            },
            "assumptions": [
                "Storage cost: 40% of total (physical warehousing)",
                "Insurance cost: 20% of total (risk protection)",
                "Opportunity cost: 40% of total (capital at 5% annual rate)",
                f"Cost per barrel per month: ${cost_per_barrel_month}",
                "Assumes existing storage infrastructure available",
                "No major capital investments required for additional capacity",
            ],
        }

        logger.info(
            f"Carrying cost calculation complete: ${costs['total_carrying_cost']:.2f} total"
        )
        return result

    return calculate_carrying_costs
