"""Unit tests for regulatory compliance tools."""

import pytest

from src.demand_planning_bot.tools.regulatory import (
    REGULATIONS_DATABASE,
    calculate_compliance_cost,
    filter_regulations,
    get_calculate_compliance_costs_tool,
    get_get_regulatory_updates_tool,
)
from src.demand_planning_bot.utils.config import Config


@pytest.fixture
def mock_config():
    """Create a mock configuration for testing."""
    config = Config(
        eia_api_key=None,
        news_api_key=None,
        server_secret=None,
        port=5222,
        debug=True,
    )
    return config


class TestRegulationsDatabase:
    """Test the regulatory database structure."""

    def test_database_not_empty(self):
        """Test that regulatory database is not empty."""
        assert len(REGULATIONS_DATABASE) > 0

    def test_all_regulations_have_required_fields(self):
        """Test that all regulations have required fields."""
        required_fields = [
            "id",
            "name",
            "type",
            "description",
            "effective_date",
            "region",
            "requirements",
            "compliance_strategies",
            "impact",
        ]

        for reg_id, reg_data in REGULATIONS_DATABASE.items():
            for field in required_fields:
                assert field in reg_data, f"Regulation {reg_id} missing field: {field}"

    def test_regulation_types(self):
        """Test that regulations have valid types."""
        valid_types = ["sulfur", "carbon"]

        for reg_id, reg_data in REGULATIONS_DATABASE.items():
            assert reg_data["type"] in valid_types, (
                f"Invalid type for {reg_id}: {reg_data['type']}"
            )

    def test_regulation_regions(self):
        """Test that regulations have valid regions."""
        valid_regions = ["global", "eu", "eca_zones"]

        for reg_id, reg_data in REGULATIONS_DATABASE.items():
            assert reg_data["region"] in valid_regions, (
                f"Invalid region for {reg_id}: {reg_data['region']}"
            )

    def test_compliance_strategies_not_empty(self):
        """Test that all regulations have compliance strategies."""
        for reg_id, reg_data in REGULATIONS_DATABASE.items():
            assert len(reg_data["compliance_strategies"]) > 0, (
                f"No compliance strategies for {reg_id}"
            )


class TestFilterRegulations:
    """Test regulation filtering logic."""

    def test_filter_all_regulations(self):
        """Test retrieving all regulations with no filters."""
        filtered = filter_regulations()
        assert len(filtered) == len(REGULATIONS_DATABASE)

    def test_filter_by_sulfur_type(self):
        """Test filtering by sulfur type."""
        filtered = filter_regulations(regulation_type="sulfur")

        assert len(filtered) > 0
        for reg in filtered:
            assert reg["type"] == "sulfur"

    def test_filter_by_carbon_type(self):
        """Test filtering by carbon type."""
        filtered = filter_regulations(regulation_type="carbon")

        assert len(filtered) > 0
        for reg in filtered:
            assert reg["type"] == "carbon"

    def test_filter_by_global_region(self):
        """Test filtering by global region."""
        filtered = filter_regulations(region="global")

        assert len(filtered) > 0
        for reg in filtered:
            assert reg["region"] == "global"

    def test_filter_by_eu_region(self):
        """Test filtering by EU region."""
        filtered = filter_regulations(region="eu")

        assert len(filtered) > 0
        for reg in filtered:
            assert reg["region"] == "eu"

    def test_filter_by_eca_region(self):
        """Test filtering by ECA zones."""
        filtered = filter_regulations(region="eca_zones")

        assert len(filtered) > 0
        for reg in filtered:
            assert reg["region"] == "eca_zones"

    def test_filter_by_effective_date(self):
        """Test filtering by effective date."""
        # Filter for regulations effective after 2025
        filtered = filter_regulations(effective_after="2025-01-01")

        assert len(filtered) > 0
        for reg in filtered:
            assert reg["effective_date"] >= "2025-01-01"

    def test_filter_combination(self):
        """Test filtering with multiple criteria."""
        # Global carbon regulations effective after 2025
        filtered = filter_regulations(
            regulation_type="carbon", region="global", effective_after="2025-01-01"
        )

        for reg in filtered:
            assert reg["type"] == "carbon"
            assert reg["region"] == "global"
            assert reg["effective_date"] >= "2025-01-01"

    def test_filtered_regulations_have_status(self):
        """Test that filtered regulations have status and deadline info."""
        filtered = filter_regulations()

        assert len(filtered) > 0
        for reg in filtered:
            assert "days_until_effective" in reg
            assert "is_active" in reg
            assert "status" in reg
            assert reg["status"] in ["active", "upcoming"]


class TestCalculateComplianceCost:
    """Test compliance cost calculations."""

    def test_low_sulfur_fuel_cost(self):
        """Test compliance cost for low sulfur fuel strategy."""
        costs = calculate_compliance_cost(
            regulation_type="sulfur",
            compliance_strategy="low_sulfur_fuel",
            annual_fuel_consumption_tons=10000,
            vessel_count=1,
        )

        # Should have fuel cost premium, no capex
        assert costs["one_time_capex"] == 0
        assert costs["cost_per_ton_fuel"] > 0
        assert costs["annual_recurring_cost"] > 0

    def test_scrubbers_cost(self):
        """Test compliance cost for scrubbers strategy."""
        costs = calculate_compliance_cost(
            regulation_type="sulfur",
            compliance_strategy="scrubbers",
            annual_fuel_consumption_tons=10000,
            vessel_count=2,
        )

        # Should have high capex ($2-5M per vessel), moderate recurring
        assert costs["one_time_capex"] > 0
        assert costs["one_time_capex"] > 1000000  # At least $1M per vessel
        assert costs["annual_recurring_cost"] > 0

    def test_carbon_offsets_cost(self):
        """Test compliance cost for carbon offsets strategy."""
        costs = calculate_compliance_cost(
            regulation_type="carbon",
            compliance_strategy="carbon_offsets",
            annual_fuel_consumption_tons=10000,
            vessel_count=1,
        )

        # Should have cost per ton CO2, no capex
        assert costs["one_time_capex"] == 0
        assert costs["cost_per_ton_fuel"] > 0
        assert costs["annual_recurring_cost"] > 0

    def test_alternative_fuels_cost(self):
        """Test compliance cost for alternative fuels strategy."""
        costs = calculate_compliance_cost(
            regulation_type="carbon",
            compliance_strategy="alternative_fuels",
            annual_fuel_consumption_tons=10000,
            vessel_count=1,
        )

        # Should have high capex (conversion) and fuel premium
        assert costs["one_time_capex"] > 0
        assert costs["one_time_capex"] > 5000000  # Fuel system conversion
        assert costs["cost_per_ton_fuel"] > 0
        assert costs["annual_recurring_cost"] > 0

    def test_fleet_scaling(self):
        """Test that costs scale with fleet size."""
        costs_1_vessel = calculate_compliance_cost(
            regulation_type="sulfur",
            compliance_strategy="scrubbers",
            annual_fuel_consumption_tons=10000,
            vessel_count=1,
        )

        costs_3_vessels = calculate_compliance_cost(
            regulation_type="sulfur",
            compliance_strategy="scrubbers",
            annual_fuel_consumption_tons=10000,
            vessel_count=3,
        )

        # Capex should scale with vessel count
        assert costs_3_vessels["one_time_capex"] == pytest.approx(
            costs_1_vessel["one_time_capex"] * 3, rel=0.01
        )

    def test_fuel_consumption_scaling(self):
        """Test that recurring costs scale with fuel consumption."""
        costs_10k_tons = calculate_compliance_cost(
            regulation_type="sulfur",
            compliance_strategy="low_sulfur_fuel",
            annual_fuel_consumption_tons=10000,
            vessel_count=1,
        )

        costs_20k_tons = calculate_compliance_cost(
            regulation_type="sulfur",
            compliance_strategy="low_sulfur_fuel",
            annual_fuel_consumption_tons=20000,
            vessel_count=1,
        )

        # Recurring costs should scale with fuel consumption
        assert costs_20k_tons["annual_recurring_cost"] == pytest.approx(
            costs_10k_tons["annual_recurring_cost"] * 2, rel=0.01
        )


class TestGetRegulatoryUpdatesTool:
    """Test the get_regulatory_updates MCP tool."""

    def test_tool_creation(self, mock_config):
        """Test that tool can be created."""
        tool = get_get_regulatory_updates_tool(mock_config)
        assert callable(tool)

    def test_default_parameters(self, mock_config):
        """Test tool with default parameters (all regulations)."""
        tool = get_get_regulatory_updates_tool(mock_config)
        result = tool()

        assert "regulations" in result
        assert "count" in result
        assert "filters_applied" in result
        assert "data_source" in result
        assert "confidence" in result

        assert result["count"] == len(REGULATIONS_DATABASE)

    def test_filter_by_sulfur(self, mock_config):
        """Test filtering by sulfur type."""
        tool = get_get_regulatory_updates_tool(mock_config)
        result = tool(regulation_type="sulfur")

        assert result["count"] > 0
        for reg in result["regulations"]:
            assert reg["type"] == "sulfur"

    def test_filter_by_carbon(self, mock_config):
        """Test filtering by carbon type."""
        tool = get_get_regulatory_updates_tool(mock_config)
        result = tool(regulation_type="carbon")

        assert result["count"] > 0
        for reg in result["regulations"]:
            assert reg["type"] == "carbon"

    def test_filter_by_region(self, mock_config):
        """Test filtering by region."""
        tool = get_get_regulatory_updates_tool(mock_config)
        result = tool(region="global")

        assert result["count"] > 0
        for reg in result["regulations"]:
            assert reg["region"] == "global"

    def test_filter_by_effective_date(self, mock_config):
        """Test filtering by effective date."""
        tool = get_get_regulatory_updates_tool(mock_config)
        result = tool(effective_after_date="2030-01-01")

        assert result["count"] > 0
        for reg in result["regulations"]:
            assert reg["effective_date"] >= "2030-01-01"

    def test_combined_filters(self, mock_config):
        """Test using multiple filters together."""
        tool = get_get_regulatory_updates_tool(mock_config)
        result = tool(regulation_type="carbon", region="global")

        for reg in result["regulations"]:
            assert reg["type"] == "carbon"
            assert reg["region"] == "global"

    def test_result_structure(self, mock_config):
        """Test that result has all required fields."""
        tool = get_get_regulatory_updates_tool(mock_config)
        result = tool()

        required_fields = [
            "regulations",
            "count",
            "filters_applied",
            "data_source",
            "note",
            "confidence",
        ]

        for field in required_fields:
            assert field in result

    def test_regulations_have_deadline_info(self, mock_config):
        """Test that returned regulations have deadline information."""
        tool = get_get_regulatory_updates_tool(mock_config)
        result = tool()

        assert len(result["regulations"]) > 0
        for reg in result["regulations"]:
            assert "days_until_effective" in reg
            assert "is_active" in reg
            assert "status" in reg


class TestCalculateComplianceCostsTool:
    """Test the calculate_compliance_costs MCP tool."""

    def test_tool_creation(self, mock_config):
        """Test that tool can be created."""
        tool = get_calculate_compliance_costs_tool(mock_config)
        assert callable(tool)

    def test_default_parameters(self, mock_config):
        """Test tool with default parameters."""
        tool = get_calculate_compliance_costs_tool(mock_config)
        result = tool()

        assert "regulation_type" in result
        assert "compliance_strategy" in result
        assert "annual_fuel_consumption_tons" in result
        assert "vessel_count" in result
        assert "one_time_capex" in result
        assert "annual_recurring_cost" in result
        assert "cost_per_ton_fuel" in result
        assert "total_annual_cost_per_vessel" in result
        assert "total_fleet_annual_cost" in result
        assert "cost_per_barrel_impact" in result
        assert "assumptions" in result
        assert "confidence" in result

    def test_sulfur_low_sulfur_fuel(self, mock_config):
        """Test sulfur compliance with low sulfur fuel strategy."""
        tool = get_calculate_compliance_costs_tool(mock_config)
        result = tool(
            regulation_type="sulfur",
            compliance_strategy="low_sulfur_fuel",
            annual_fuel_consumption_tons=10000,
            vessel_count=1,
        )

        assert result["regulation_type"] == "sulfur"
        assert result["compliance_strategy"] == "low_sulfur_fuel"
        assert result["one_time_capex"] == 0
        assert result["cost_per_ton_fuel"] > 0

    def test_sulfur_scrubbers(self, mock_config):
        """Test sulfur compliance with scrubbers strategy."""
        tool = get_calculate_compliance_costs_tool(mock_config)
        result = tool(
            regulation_type="sulfur",
            compliance_strategy="scrubbers",
            annual_fuel_consumption_tons=10000,
            vessel_count=2,
        )

        assert result["regulation_type"] == "sulfur"
        assert result["compliance_strategy"] == "scrubbers"
        assert result["one_time_capex"] > 0

    def test_carbon_offsets(self, mock_config):
        """Test carbon compliance with offsets strategy."""
        tool = get_calculate_compliance_costs_tool(mock_config)
        result = tool(
            regulation_type="carbon",
            compliance_strategy="carbon_offsets",
            annual_fuel_consumption_tons=10000,
            vessel_count=1,
        )

        assert result["regulation_type"] == "carbon"
        assert result["compliance_strategy"] == "carbon_offsets"
        assert result["one_time_capex"] == 0
        assert result["annual_recurring_cost"] > 0

    def test_carbon_alternative_fuels(self, mock_config):
        """Test carbon compliance with alternative fuels strategy."""
        tool = get_calculate_compliance_costs_tool(mock_config)
        result = tool(
            regulation_type="carbon",
            compliance_strategy="alternative_fuels",
            annual_fuel_consumption_tons=10000,
            vessel_count=1,
        )

        assert result["regulation_type"] == "carbon"
        assert result["compliance_strategy"] == "alternative_fuels"
        assert result["one_time_capex"] > 0
        assert result["cost_per_ton_fuel"] > 0

    def test_invalid_regulation_type(self, mock_config):
        """Test error handling for invalid regulation type."""
        tool = get_calculate_compliance_costs_tool(mock_config)
        result = tool(regulation_type="invalid_type")  # type: ignore

        assert "error" in result

    def test_invalid_strategy_for_sulfur(self, mock_config):
        """Test error handling for invalid strategy with sulfur."""
        tool = get_calculate_compliance_costs_tool(mock_config)
        result = tool(regulation_type="sulfur", compliance_strategy="carbon_offsets")

        assert "error" in result
        assert "valid_strategies" in result

    def test_invalid_strategy_for_carbon(self, mock_config):
        """Test error handling for invalid strategy with carbon."""
        tool = get_calculate_compliance_costs_tool(mock_config)
        result = tool(regulation_type="carbon", compliance_strategy="scrubbers")

        assert "error" in result
        assert "valid_strategies" in result

    def test_cost_per_barrel_impact(self, mock_config):
        """Test that cost per barrel impact is calculated."""
        tool = get_calculate_compliance_costs_tool(mock_config)
        result = tool()

        assert "cost_per_barrel_impact" in result
        # Cost per barrel should be cost per ton / ~7.33 barrels per ton
        expected = result["cost_per_ton_fuel"] / 7.33
        assert result["cost_per_barrel_impact"] == pytest.approx(expected, rel=0.01)

    def test_result_structure(self, mock_config):
        """Test that result has all required fields."""
        tool = get_calculate_compliance_costs_tool(mock_config)
        result = tool()

        required_fields = [
            "regulation_type",
            "compliance_strategy",
            "annual_fuel_consumption_tons",
            "vessel_count",
            "currency",
            "one_time_capex",
            "annual_recurring_cost",
            "cost_per_ton_fuel",
            "total_annual_cost_per_vessel",
            "total_fleet_annual_cost",
            "cost_per_barrel_impact",
            "assumptions",
            "confidence",
            "note",
        ]

        for field in required_fields:
            assert field in result
