"""Unit tests for supply chain disruption simulation tools."""

import pytest

from src.demand_planning_bot.tools.supply_chain import (
    DISRUPTION_MODELS,
    REFINERY_DATA,
    calculate_disruption_impact,
    get_simulate_supply_disruption_tool,
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


class TestDisruptionModels:
    """Test disruption model data structures."""

    def test_all_disruption_types_exist(self):
        """Test that all expected disruption types are defined."""
        expected_types = [
            "strait_of_hormuz_closure",
            "pipeline_outage",
            "port_closure",
            "weather_event",
        ]
        for disruption_type in expected_types:
            assert disruption_type in DISRUPTION_MODELS
            assert "name" in DISRUPTION_MODELS[disruption_type]
            assert "description" in DISRUPTION_MODELS[disruption_type]
            assert "severity" in DISRUPTION_MODELS[disruption_type]
            assert "alternative_routes" in DISRUPTION_MODELS[disruption_type]

    def test_severity_levels(self):
        """Test that severity levels are appropriate."""
        assert DISRUPTION_MODELS["strait_of_hormuz_closure"]["severity"] == "high"
        assert DISRUPTION_MODELS["pipeline_outage"]["severity"] == "medium"
        assert DISRUPTION_MODELS["port_closure"]["severity"] == "medium"
        assert DISRUPTION_MODELS["weather_event"]["severity"] == "low"

    def test_alternative_routes_not_empty(self):
        """Test that all disruptions have alternative routes."""
        for disruption_type, data in DISRUPTION_MODELS.items():
            assert len(data["alternative_routes"]) > 0


class TestRefineryData:
    """Test refinery data structures."""

    def test_rotterdam_refinery_data(self):
        """Test Rotterdam refinery data."""
        rotterdam = REFINERY_DATA["rotterdam"]
        assert rotterdam["name"] == "Rotterdam Refinery"
        assert rotterdam["location"] == "Rotterdam, Netherlands"
        assert rotterdam["capacity_barrels_per_day"] == 400000
        assert len(rotterdam["primary_feedstock_sources"]) > 0
        assert rotterdam["typical_inventory_days"] == 30
        assert "Middle East (Strait of Hormuz)" in rotterdam["transit_time_days"]

    def test_singapore_refinery_data(self):
        """Test Singapore refinery data."""
        singapore = REFINERY_DATA["singapore"]
        assert singapore["name"] == "Singapore Refinery"
        assert singapore["location"] == "Singapore"
        assert singapore["capacity_barrels_per_day"] == 500000
        assert len(singapore["primary_feedstock_sources"]) > 0
        assert singapore["typical_inventory_days"] == 25
        assert "Middle East (Strait of Hormuz)" in singapore["transit_time_days"]


class TestCalculateDisruptionImpact:
    """Test disruption impact calculations."""

    def test_strait_of_hormuz_rotterdam_impact(self, mock_config):
        """Test Strait of Hormuz closure impact on Rotterdam."""
        impact = calculate_disruption_impact(
            disruption_type="strait_of_hormuz_closure",
            refinery="rotterdam",
            duration_days=14,
            config=mock_config,
        )

        assert "error" not in impact
        assert impact["refinery"] == "Rotterdam Refinery"
        assert impact["feedstock_shortage_percentage"] == 50.0
        assert impact["procurement_cost_increase_percentage"] == 25.0
        assert impact["days_until_impact"] == 30  # Rotterdam inventory days
        assert "barrels_affected" in impact
        assert "additional_procurement_cost_usd" in impact
        assert len(impact["mitigation_timeline"]) > 0
        assert len(impact["alternative_routes"]) > 0

    def test_strait_of_hormuz_singapore_impact(self, mock_config):
        """Test Strait of Hormuz closure impact on Singapore."""
        impact = calculate_disruption_impact(
            disruption_type="strait_of_hormuz_closure",
            refinery="singapore",
            duration_days=14,
            config=mock_config,
        )

        assert "error" not in impact
        assert impact["refinery"] == "Singapore Refinery"
        assert impact["feedstock_shortage_percentage"] == 70.0  # Higher than Rotterdam
        assert (
            impact["procurement_cost_increase_percentage"] == 35.0
        )  # Higher than Rotterdam
        assert impact["days_until_impact"] == 25  # Singapore inventory days

    def test_pipeline_outage_impact(self, mock_config):
        """Test pipeline outage impact."""
        impact = calculate_disruption_impact(
            disruption_type="pipeline_outage",
            refinery="rotterdam",
            duration_days=7,
            config=mock_config,
        )

        assert "error" not in impact
        assert impact["feedstock_shortage_percentage"] == 30.0
        assert impact["procurement_cost_increase_percentage"] == 15.0
        assert impact["days_until_impact"] == 7

    def test_port_closure_impact(self, mock_config):
        """Test port closure impact."""
        impact = calculate_disruption_impact(
            disruption_type="port_closure",
            refinery="singapore",
            duration_days=5,
            config=mock_config,
        )

        assert "error" not in impact
        assert impact["feedstock_shortage_percentage"] == 20.0
        assert impact["procurement_cost_increase_percentage"] == 10.0
        assert impact["days_until_impact"] == 5

    def test_weather_event_impact(self, mock_config):
        """Test weather event impact."""
        impact = calculate_disruption_impact(
            disruption_type="weather_event",
            refinery="rotterdam",
            duration_days=3,
            config=mock_config,
        )

        assert "error" not in impact
        assert impact["feedstock_shortage_percentage"] == 15.0
        assert impact["procurement_cost_increase_percentage"] == 5.0
        assert impact["days_until_impact"] == 3

    def test_cost_calculations(self, mock_config):
        """Test that cost calculations are reasonable."""
        impact = calculate_disruption_impact(
            disruption_type="strait_of_hormuz_closure",
            refinery="rotterdam",
            duration_days=14,
            config=mock_config,
        )

        # Calculate expected values
        daily_capacity = 400000  # Rotterdam capacity
        shortage_pct = 50.0
        cost_increase_pct = 25.0
        barrels = daily_capacity * (shortage_pct / 100) * 14
        expected_cost = barrels * 80 * (cost_increase_pct / 100)

        assert impact["barrels_affected"] == pytest.approx(barrels, rel=0.01)
        assert impact["additional_procurement_cost_usd"] == pytest.approx(
            expected_cost, rel=0.01
        )

    def test_mitigation_timeline_structure(self, mock_config):
        """Test that mitigation timeline is properly structured."""
        impact = calculate_disruption_impact(
            disruption_type="strait_of_hormuz_closure",
            refinery="rotterdam",
            duration_days=14,
            config=mock_config,
        )

        timeline = impact["mitigation_timeline"]
        assert len(timeline) == 4  # Start, impact, end, recovery
        assert timeline[0]["day"] == 0
        assert timeline[1]["day"] == 30  # Days until impact (Rotterdam inventory)
        assert timeline[2]["day"] == 14  # Duration
        assert timeline[3]["day"] == 28  # Duration + 14 recovery

        for event in timeline:
            assert "day" in event
            assert "date" in event
            assert "event" in event

    def test_invalid_disruption_type(self, mock_config):
        """Test handling of invalid disruption type."""
        impact = calculate_disruption_impact(
            disruption_type="invalid_type",
            refinery="rotterdam",
            duration_days=14,
            config=mock_config,
        )

        assert "error" in impact

    def test_invalid_refinery(self, mock_config):
        """Test handling of invalid refinery."""
        impact = calculate_disruption_impact(
            disruption_type="strait_of_hormuz_closure",
            refinery="invalid_refinery",
            duration_days=14,
            config=mock_config,
        )

        assert "error" in impact


class TestSimulateSupplyDisruptionTool:
    """Test the simulate_supply_disruption MCP tool."""

    def test_tool_creation(self, mock_config):
        """Test that tool can be created."""
        tool = get_simulate_supply_disruption_tool(mock_config)
        assert callable(tool)

    def test_default_parameters(self, mock_config):
        """Test tool with default parameters."""
        tool = get_simulate_supply_disruption_tool(mock_config)
        result = tool()

        assert "error" not in result
        assert result["disruption_type"] == "strait_of_hormuz_closure"
        assert result["disruption_name"] == "Strait of Hormuz Closure"
        assert "description" in result
        assert result["severity"] == "high"
        assert result["duration_days"] == 14
        assert len(result["affected_refineries"]) == 2  # Both refineries

    def test_single_refinery(self, mock_config):
        """Test tool with single refinery."""
        tool = get_simulate_supply_disruption_tool(mock_config)
        result = tool(
            disruption_type="pipeline_outage",
            affected_refineries=["rotterdam"],
            duration_days=7,
        )

        assert len(result["affected_refineries"]) == 1
        assert result["affected_refineries"][0]["refinery"] == "Rotterdam Refinery"
        assert result["duration_days"] == 7

    def test_all_disruption_types(self, mock_config):
        """Test tool with all disruption types."""
        tool = get_simulate_supply_disruption_tool(mock_config)
        disruption_types = [
            "strait_of_hormuz_closure",
            "pipeline_outage",
            "port_closure",
            "weather_event",
        ]

        for disruption_type in disruption_types:
            result = tool(disruption_type=disruption_type, duration_days=10)
            assert result["disruption_type"] == disruption_type
            assert result["duration_days"] == 10
            assert len(result["affected_refineries"]) > 0

    def test_refinery_specific_impacts_differ(self, mock_config):
        """Test that Rotterdam and Singapore have different impacts."""
        tool = get_simulate_supply_disruption_tool(mock_config)
        result = tool(disruption_type="strait_of_hormuz_closure")

        rotterdam = next(
            r
            for r in result["affected_refineries"]
            if r["refinery"] == "Rotterdam Refinery"
        )
        singapore = next(
            r
            for r in result["affected_refineries"]
            if r["refinery"] == "Singapore Refinery"
        )

        # Singapore should have higher shortage % for Strait of Hormuz
        assert (
            singapore["feedstock_shortage_percentage"]
            > rotterdam["feedstock_shortage_percentage"]
        )

    def test_result_structure(self, mock_config):
        """Test that result has all required fields."""
        tool = get_simulate_supply_disruption_tool(mock_config)
        result = tool()

        required_fields = [
            "disruption_type",
            "disruption_name",
            "description",
            "severity",
            "duration_days",
            "affected_refineries",
            "confidence",
            "assumptions",
        ]

        for field in required_fields:
            assert field in result

        # Check refinery impact structure
        for refinery_impact in result["affected_refineries"]:
            refinery_required_fields = [
                "refinery",
                "location",
                "daily_capacity_barrels",
                "feedstock_shortage_percentage",
                "procurement_cost_increase_percentage",
                "barrels_affected",
                "additional_procurement_cost_usd",
                "days_until_impact",
                "mitigation_timeline",
                "alternative_routes",
            ]
            for field in refinery_required_fields:
                assert field in refinery_impact

    def test_invalid_disruption_type_error(self, mock_config):
        """Test error handling for invalid disruption type."""
        tool = get_simulate_supply_disruption_tool(mock_config)
        result = tool(disruption_type="invalid_type")  # type: ignore

        assert "error" in result
        assert "valid_types" in result

    def test_assumptions_included(self, mock_config):
        """Test that assumptions are documented."""
        tool = get_simulate_supply_disruption_tool(mock_config)
        result = tool()

        assert "assumptions" in result
        assert isinstance(result["assumptions"], list)
        assert len(result["assumptions"]) > 0
