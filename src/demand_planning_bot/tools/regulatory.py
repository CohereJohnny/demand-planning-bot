"""Regulatory compliance tools for the Demand Planning Bot.

This module provides tools to retrieve regulatory updates and calculate
compliance costs for IMO regulations and other environmental requirements.
"""

import logging
from datetime import datetime
from typing import Dict, List, Literal, Optional

from src.demand_planning_bot.utils.config import Config

logger = logging.getLogger(__name__)


# IMO and regulatory database
REGULATIONS_DATABASE = {
    "imo_2020": {
        "id": "imo_2020",
        "name": "IMO 2020 Sulfur Cap",
        "type": "sulfur",
        "description": (
            "Global sulfur cap of 0.5% m/m (mass by mass) for marine fuels, "
            "down from previous 3.5% limit. Applies to all vessels outside "
            "designated Emission Control Areas (ECAs)."
        ),
        "effective_date": "2020-01-01",
        "region": "global",
        "requirements": [
            "Use fuel with sulfur content ≤0.5% m/m",
            "OR install exhaust gas cleaning systems (scrubbers)",
            "Maintain fuel oil record book documentation",
            "Ensure fuel oil bunker delivery notes specify sulfur content",
        ],
        "compliance_strategies": ["low_sulfur_fuel", "scrubbers"],
        "impact": "Significant fuel cost increase or capital expenditure for scrubbers",
    },
    "imo_2030": {
        "id": "imo_2030",
        "name": "IMO 2030 Carbon Intensity Reduction",
        "type": "carbon",
        "description": (
            "40% reduction in carbon intensity (CO2 emissions per transport work) "
            "by 2030 compared to 2008 baseline. Part of IMO's initial GHG strategy."
        ),
        "effective_date": "2030-01-01",
        "region": "global",
        "requirements": [
            "Achieve 40% CO2 intensity reduction vs 2008 baseline",
            "Implement Energy Efficiency Existing Ship Index (EEXI)",
            "Maintain Carbon Intensity Indicator (CII) rating of C or better",
            "Annual reporting and verification",
        ],
        "compliance_strategies": [
            "operational_efficiency",
            "alternative_fuels",
            "carbon_offsets",
        ],
        "impact": "Operational changes, potential fleet upgrades, carbon offset purchases",
    },
    "imo_2050": {
        "id": "imo_2050",
        "name": "IMO 2050 Net Zero Target",
        "type": "carbon",
        "description": (
            "Net-zero GHG emissions by or around 2050. Reduction of total annual "
            "GHG emissions by at least 50% by 2050 compared to 2008."
        ),
        "effective_date": "2050-01-01",
        "region": "global",
        "requirements": [
            "50% reduction in total GHG emissions vs 2008",
            "Phase out of fossil fuels",
            "Adoption of zero/near-zero emission fuels",
            "Significant technological innovation required",
        ],
        "compliance_strategies": [
            "alternative_fuels",
            "electric_propulsion",
            "hydrogen_ammonia",
        ],
        "impact": "Major fleet transformation, significant capital investment required",
    },
    "eca_0.1": {
        "id": "eca_0.1",
        "name": "ECA 0.1% Sulfur Limit",
        "type": "sulfur",
        "description": (
            "Emission Control Areas (ECAs) require 0.1% m/m sulfur content in fuel. "
            "Applies to North American ECA, US Caribbean ECA, North Sea ECA, and Baltic Sea ECA."
        ),
        "effective_date": "2015-01-01",
        "region": "eca_zones",
        "requirements": [
            "Use fuel with sulfur content ≤0.1% m/m in ECA zones",
            "OR install exhaust gas cleaning systems",
            "Switch fuels when entering/exiting ECAs",
        ],
        "compliance_strategies": ["ultra_low_sulfur_fuel", "scrubbers"],
        "impact": "Higher fuel costs in ECA zones, fuel switching logistics",
    },
    "eu_ets": {
        "id": "eu_ets",
        "name": "EU Emissions Trading System",
        "type": "carbon",
        "description": (
            "EU ETS extended to maritime sector. Ships >5000 GT calling at EU ports "
            "must surrender allowances for CO2 emissions. Phase-in: 40% (2024), "
            "70% (2025), 100% (2026)."
        ),
        "effective_date": "2024-01-01",
        "region": "eu",
        "requirements": [
            "Monitor and report CO2 emissions",
            "Surrender EU ETS allowances for emissions",
            "100% of emissions within EU ports and 50% of voyages to/from EU",
            "Comply with MRV (Monitoring, Reporting, Verification) regulation",
        ],
        "compliance_strategies": ["carbon_allowances", "operational_efficiency"],
        "impact": "Direct carbon costs, administrative burden, potential route optimization",
    },
}


def filter_regulations(
    regulation_type: Optional[str] = None,
    region: Optional[str] = None,
    effective_after: Optional[str] = None,
) -> List[Dict]:
    """Filter regulations based on criteria.

    Args:
        regulation_type: Type of regulation ("sulfur", "carbon", or None for all).
        region: Region ("global", "eu", "eca_zones", or None for all).
        effective_after: ISO date string (YYYY-MM-DD). Only return regulations
                        effective on or after this date.

    Returns:
        List of regulation dictionaries matching criteria.
    """
    filtered = []

    for reg_id, reg_data in REGULATIONS_DATABASE.items():
        # Filter by type
        if regulation_type and reg_data["type"] != regulation_type:
            continue

        # Filter by region
        if region and reg_data["region"] != region:
            continue

        # Filter by effective date
        if effective_after:
            try:
                filter_date = datetime.fromisoformat(effective_after)
                reg_date = datetime.fromisoformat(reg_data["effective_date"])
                if reg_date < filter_date:
                    continue
            except ValueError:
                logger.warning(f"Invalid date format: {effective_after}")
                continue

        # Calculate days until effective/since effective
        reg_date = datetime.fromisoformat(reg_data["effective_date"])
        today = datetime.now()
        days_difference = (reg_date - today).days

        # Add compliance deadline info
        reg_with_deadline = {
            **reg_data,
            "days_until_effective": days_difference if days_difference > 0 else 0,
            "is_active": days_difference <= 0,
            "status": "active" if days_difference <= 0 else "upcoming",
        }

        filtered.append(reg_with_deadline)

    return filtered


def calculate_compliance_cost(
    regulation_type: str,
    compliance_strategy: str,
    annual_fuel_consumption_tons: float,
    vessel_count: int = 1,
) -> Dict:
    """Calculate estimated compliance costs.

    Args:
        regulation_type: Type of regulation ("sulfur" or "carbon").
        compliance_strategy: Strategy to use.
        annual_fuel_consumption_tons: Annual fuel consumption in metric tons.
        vessel_count: Number of vessels in fleet.

    Returns:
        Dictionary with cost breakdown.
    """
    costs = {
        "one_time_capex": 0.0,
        "annual_recurring_cost": 0.0,
        "cost_per_ton_fuel": 0.0,
        "total_annual_cost_per_vessel": 0.0,
        "total_fleet_annual_cost": 0.0,
    }

    if regulation_type == "sulfur":
        if compliance_strategy == "low_sulfur_fuel":
            # Low Sulfur Fuel Oil (LSFO) premium: ~$150-200/ton vs HSFO
            lsfo_premium_per_ton = 175.0
            costs["cost_per_ton_fuel"] = lsfo_premium_per_ton
            costs["annual_recurring_cost"] = (
                annual_fuel_consumption_tons * lsfo_premium_per_ton
            )
            costs["one_time_capex"] = 0  # No capital expenditure

        elif compliance_strategy == "ultra_low_sulfur_fuel":
            # Ultra Low Sulfur Fuel (ULSF) for ECAs: ~$250-300/ton premium
            ulsf_premium_per_ton = 275.0
            costs["cost_per_ton_fuel"] = ulsf_premium_per_ton
            costs["annual_recurring_cost"] = (
                annual_fuel_consumption_tons * ulsf_premium_per_ton
            )
            costs["one_time_capex"] = 0

        elif compliance_strategy == "scrubbers":
            # Scrubber installation: ~$2-5M per vessel
            scrubber_capex_per_vessel = 3500000.0
            costs["one_time_capex"] = scrubber_capex_per_vessel * vessel_count

            # Scrubber maintenance: ~$200k/year per vessel
            scrubber_maintenance_per_vessel = 200000.0
            costs["annual_recurring_cost"] = (
                scrubber_maintenance_per_vessel * vessel_count
            )

            # Can continue using cheaper HSFO, saving ~$175/ton
            # (but show as recurring cost saving, not additional cost)
            costs["annual_recurring_cost"] = scrubber_maintenance_per_vessel

    elif regulation_type == "carbon":
        if compliance_strategy == "carbon_offsets":
            # Carbon offsets: ~$50-100 per ton CO2
            # Fuel produces ~3.1 tons CO2 per ton fuel
            co2_per_ton_fuel = 3.1
            carbon_offset_price_per_ton_co2 = 75.0
            total_co2_tons = annual_fuel_consumption_tons * co2_per_ton_fuel

            costs["cost_per_ton_fuel"] = (
                carbon_offset_price_per_ton_co2 * co2_per_ton_fuel
            )
            costs["annual_recurring_cost"] = (
                total_co2_tons * carbon_offset_price_per_ton_co2
            )
            costs["one_time_capex"] = 0

        elif compliance_strategy == "carbon_allowances":
            # EU ETS allowances: ~€80-100 per ton CO2 (~$85-110 USD)
            # Assume 100% phase-in (2026 onwards)
            co2_per_ton_fuel = 3.1
            eu_ets_price_per_ton_co2 = 95.0
            total_co2_tons = annual_fuel_consumption_tons * co2_per_ton_fuel

            costs["cost_per_ton_fuel"] = eu_ets_price_per_ton_co2 * co2_per_ton_fuel
            costs["annual_recurring_cost"] = total_co2_tons * eu_ets_price_per_ton_co2
            costs["one_time_capex"] = 0

        elif compliance_strategy == "operational_efficiency":
            # Operational efficiency improvements: ~$500k-1M per vessel (technology, training)
            efficiency_capex_per_vessel = 750000.0
            costs["one_time_capex"] = efficiency_capex_per_vessel * vessel_count

            # Ongoing monitoring and optimization: ~$100k/year per vessel
            efficiency_recurring_per_vessel = 100000.0
            costs["annual_recurring_cost"] = efficiency_recurring_per_vessel

        elif compliance_strategy == "alternative_fuels":
            # Alternative fuels (LNG, methanol, ammonia): significant premium
            # LNG premium: ~$200-300/ton vs conventional fuel
            alt_fuel_premium_per_ton = 250.0
            costs["cost_per_ton_fuel"] = alt_fuel_premium_per_ton
            costs["annual_recurring_cost"] = (
                annual_fuel_consumption_tons * alt_fuel_premium_per_ton
            )

            # Fuel system conversion: ~$5-10M per vessel
            conversion_capex_per_vessel = 7500000.0
            costs["one_time_capex"] = conversion_capex_per_vessel * vessel_count

    # Calculate totals
    costs["total_annual_cost_per_vessel"] = (
        costs["annual_recurring_cost"] / vessel_count if vessel_count > 0 else 0
    )
    costs["total_fleet_annual_cost"] = costs["annual_recurring_cost"] * vessel_count

    # Round all values
    for key in costs:
        costs[key] = round(costs[key], 2)

    return costs


def get_get_regulatory_updates_tool(config: Config):
    """Provides an MCP tool to retrieve regulatory updates.

    Args:
        config: The application configuration.

    Returns:
        A callable MCP tool function.
    """

    def get_regulatory_updates(
        regulation_type: Optional[Literal["sulfur", "carbon"]] = None,
        region: Optional[Literal["global", "eu", "eca_zones"]] = None,
        effective_after_date: Optional[str] = None,
    ) -> Dict:
        """Get regulatory updates and compliance requirements for maritime fuel regulations.

        Retrieves information about IMO sulfur caps, carbon intensity targets, EU ETS,
        and other environmental regulations affecting oil and gas supply chains. Helps
        identify upcoming compliance requirements and deadlines.

        Args:
            regulation_type: Filter by regulation type.
                            "sulfur" = sulfur content regulations (IMO 2020, ECAs)
                            "carbon" = carbon/GHG regulations (IMO 2030, IMO 2050, EU ETS)
                            None = all regulations
            region: Filter by geographic scope.
                   "global" = worldwide regulations
                   "eu" = EU-specific regulations
                   "eca_zones" = Emission Control Area regulations
                   None = all regions
            effective_after_date: Only return regulations effective on or after this date.
                                 Format: YYYY-MM-DD (e.g., "2024-01-01")

        Returns:
            Dictionary with regulatory information including:
            - regulations: List of applicable regulations
            - count: Number of regulations found
            - filters_applied: Summary of filters used
        """
        logger.info(
            f"get_regulatory_updates called: type={regulation_type}, "
            f"region={region}, effective_after={effective_after_date}"
        )

        # Filter regulations
        regulations = filter_regulations(
            regulation_type=regulation_type,
            region=region,
            effective_after=effective_after_date,
        )

        result = {
            "regulations": regulations,
            "count": len(regulations),
            "filters_applied": {
                "regulation_type": regulation_type or "all",
                "region": region or "all",
                "effective_after": effective_after_date or "no date filter",
            },
            "data_source": "simulated_regulatory_database",
            "note": "Regulatory data is for demonstration purposes. Consult official IMO and regional authority sources for compliance.",
            "confidence": "high",
        }

        logger.info(f"Retrieved {len(regulations)} regulations")
        return result

    return get_regulatory_updates


def get_calculate_compliance_costs_tool(config: Config):
    """Provides an MCP tool to calculate regulatory compliance costs.

    Args:
        config: The application configuration.

    Returns:
        A callable MCP tool function.
    """

    def calculate_compliance_costs(
        regulation_type: Literal["sulfur", "carbon"] = "sulfur",
        compliance_strategy: str = "low_sulfur_fuel",
        annual_fuel_consumption_tons: float = 10000,
        vessel_count: int = 1,
    ) -> Dict:
        """Calculate estimated costs for regulatory compliance strategies.

        Estimates capital expenditures and recurring costs for different compliance
        approaches to sulfur and carbon regulations. Helps evaluate the financial
        impact of regulatory compliance options.

        Args:
            regulation_type: Type of regulation.
                            "sulfur" = sulfur content compliance (IMO 2020, ECAs)
                            "carbon" = carbon/GHG compliance (IMO 2030, EU ETS)
            compliance_strategy: Strategy to achieve compliance.
                                For sulfur: "low_sulfur_fuel", "ultra_low_sulfur_fuel", "scrubbers"
                                For carbon: "carbon_offsets", "carbon_allowances",
                                           "operational_efficiency", "alternative_fuels"
            annual_fuel_consumption_tons: Annual fuel consumption per vessel (metric tons).
            vessel_count: Number of vessels in fleet.

        Returns:
            Dictionary with compliance cost analysis including:
            - one_time_capex: One-time capital expenditure
            - annual_recurring_cost: Annual recurring costs per vessel
            - cost_per_ton_fuel: Additional cost per ton of fuel
            - total_annual_cost_per_vessel: Total annual cost per vessel
            - total_fleet_annual_cost: Total annual cost for entire fleet
            - assumptions: Calculation assumptions
        """
        logger.info(
            f"calculate_compliance_costs called: type={regulation_type}, "
            f"strategy={compliance_strategy}, consumption={annual_fuel_consumption_tons}t, "
            f"vessels={vessel_count}"
        )

        # Validate inputs
        if regulation_type not in ["sulfur", "carbon"]:
            return {
                "error": "regulation_type must be 'sulfur' or 'carbon'",
                "provided": regulation_type,
            }

        # Define valid strategies per regulation type
        valid_strategies = {
            "sulfur": ["low_sulfur_fuel", "ultra_low_sulfur_fuel", "scrubbers"],
            "carbon": [
                "carbon_offsets",
                "carbon_allowances",
                "operational_efficiency",
                "alternative_fuels",
            ],
        }

        if compliance_strategy not in valid_strategies[regulation_type]:
            return {
                "error": f"Invalid strategy for {regulation_type} compliance",
                "provided": compliance_strategy,
                "valid_strategies": valid_strategies[regulation_type],
            }

        # Calculate costs
        costs = calculate_compliance_cost(
            regulation_type=regulation_type,
            compliance_strategy=compliance_strategy,
            annual_fuel_consumption_tons=annual_fuel_consumption_tons,
            vessel_count=vessel_count,
        )

        result = {
            "regulation_type": regulation_type,
            "compliance_strategy": compliance_strategy,
            "annual_fuel_consumption_tons": annual_fuel_consumption_tons,
            "vessel_count": vessel_count,
            "currency": "USD",
            **costs,
            "cost_per_barrel_impact": round(
                costs["cost_per_ton_fuel"] / 7.33, 2
            ),  # ~7.33 barrels per ton
            "assumptions": [
                f"Regulation type: {regulation_type}",
                f"Compliance strategy: {compliance_strategy}",
                f"Annual fuel consumption: {annual_fuel_consumption_tons:,.0f} tons per vessel",
                f"Fleet size: {vessel_count} vessel(s)",
                "Cost estimates based on industry averages (2024-2025 market conditions)",
                "Actual costs vary by vessel type, trade routes, and market conditions",
            ],
            "confidence": "medium",
            "note": "Cost estimates are for demonstration purposes. Consult compliance specialists for detailed analysis.",
        }

        logger.info(
            f"Compliance costs calculated: ${costs['total_fleet_annual_cost']:,.2f} annual fleet cost"
        )
        return result

    return calculate_compliance_costs
