"""Unit tests for inventory optimization tools."""

import math

import pytest

from src.demand_planning_bot.tools.inventory import (
    calculate_carrying_cost_components,
    calculate_safety_stock,
    get_calculate_carrying_costs_tool,
    get_calculate_inventory_requirements_tool,
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


class TestCalculateSafetyStock:
    """Test safety stock calculation formulas."""

    def test_basic_calculation(self):
        """Test basic safety stock calculation."""
        # Formula: z × σ × √L
        # For 95% service level: z = 1.65
        # σ = 5000 barrels/day
        # L = 21 days
        # Expected: 1.65 × 5000 × √21 = 37,839 barrels
        demand_std_dev = 5000
        lead_time_days = 21
        service_level = 0.95

        safety_stock = calculate_safety_stock(
            demand_std_dev, lead_time_days, service_level
        )

        expected = 1.65 * 5000 * math.sqrt(21)
        assert safety_stock == pytest.approx(expected, rel=0.01)
        assert safety_stock == pytest.approx(37839, rel=0.01)

    def test_different_service_levels(self):
        """Test safety stock with different service levels."""
        demand_std_dev = 5000
        lead_time_days = 21

        # Test known z-scores
        service_levels = {
            0.90: 1.28,
            0.95: 1.65,
            0.975: 1.96,
            0.99: 2.33,
        }

        for service_level, z_score in service_levels.items():
            safety_stock = calculate_safety_stock(
                demand_std_dev, lead_time_days, service_level
            )
            expected = z_score * demand_std_dev * math.sqrt(lead_time_days)
            assert safety_stock == pytest.approx(expected, rel=0.01)

    def test_higher_std_dev_increases_safety_stock(self):
        """Test that higher demand variability increases safety stock."""
        lead_time_days = 21
        service_level = 0.95

        low_std_dev_stock = calculate_safety_stock(3000, lead_time_days, service_level)
        high_std_dev_stock = calculate_safety_stock(7000, lead_time_days, service_level)

        assert high_std_dev_stock > low_std_dev_stock
        # Should be proportional to std dev
        assert high_std_dev_stock / low_std_dev_stock == pytest.approx(
            7000 / 3000, rel=0.01
        )

    def test_longer_lead_time_increases_safety_stock(self):
        """Test that longer lead time increases safety stock."""
        demand_std_dev = 5000
        service_level = 0.95

        short_lead_stock = calculate_safety_stock(demand_std_dev, 10, service_level)
        long_lead_stock = calculate_safety_stock(demand_std_dev, 30, service_level)

        assert long_lead_stock > short_lead_stock
        # Should be proportional to √lead_time
        assert long_lead_stock / short_lead_stock == pytest.approx(
            math.sqrt(30) / math.sqrt(10), rel=0.01
        )

    def test_zero_std_dev(self):
        """Test with zero standard deviation (no variability)."""
        safety_stock = calculate_safety_stock(
            demand_std_dev=0, lead_time_days=21, service_level=0.95
        )
        assert safety_stock == 0

    def test_zero_lead_time(self):
        """Test with zero lead time."""
        safety_stock = calculate_safety_stock(
            demand_std_dev=5000, lead_time_days=0, service_level=0.95
        )
        assert safety_stock == 0


class TestCalculateCarryingCostComponents:
    """Test carrying cost component calculations."""

    def test_basic_cost_calculation(self):
        """Test basic carrying cost calculation."""
        inventory_barrels = 100000
        duration_months = 3
        cost_per_barrel_month = 1.5

        costs = calculate_carrying_cost_components(
            inventory_barrels, duration_months, cost_per_barrel_month
        )

        # Expected breakdown:
        # Storage: 40% of $1.50 = $0.60/barrel/month × 100,000 × 3 = $180,000
        # Insurance: 20% of $1.50 = $0.30/barrel/month × 100,000 × 3 = $90,000
        # Opportunity: 40% of $1.50 = $0.60/barrel/month × 100,000 × 3 = $180,000
        # Total: $450,000

        assert costs["storage_cost"] == pytest.approx(180000, rel=0.01)
        assert costs["insurance_cost"] == pytest.approx(90000, rel=0.01)
        assert costs["opportunity_cost"] == pytest.approx(180000, rel=0.01)
        assert costs["total_carrying_cost"] == pytest.approx(450000, rel=0.01)

    def test_cost_proportional_to_inventory(self):
        """Test that costs scale proportionally with inventory."""
        duration_months = 3
        cost_per_barrel_month = 1.5

        costs_small = calculate_carrying_cost_components(
            50000, duration_months, cost_per_barrel_month
        )
        costs_large = calculate_carrying_cost_components(
            100000, duration_months, cost_per_barrel_month
        )

        assert costs_large["total_carrying_cost"] == pytest.approx(
            costs_small["total_carrying_cost"] * 2, rel=0.01
        )

    def test_cost_proportional_to_duration(self):
        """Test that costs scale proportionally with duration."""
        inventory_barrels = 100000
        cost_per_barrel_month = 1.5

        costs_short = calculate_carrying_cost_components(
            inventory_barrels, 3, cost_per_barrel_month
        )
        costs_long = calculate_carrying_cost_components(
            inventory_barrels, 6, cost_per_barrel_month
        )

        assert costs_long["total_carrying_cost"] == pytest.approx(
            costs_short["total_carrying_cost"] * 2, rel=0.01
        )

    def test_cost_breakdown_percentages(self):
        """Test that cost breakdown follows expected percentages."""
        costs = calculate_carrying_cost_components(
            inventory_barrels=100000, duration_months=3, cost_per_barrel_month=1.5
        )

        total = costs["total_carrying_cost"]
        storage_pct = costs["storage_cost"] / total * 100
        insurance_pct = costs["insurance_cost"] / total * 100
        opportunity_pct = costs["opportunity_cost"] / total * 100

        assert storage_pct == pytest.approx(40, rel=0.01)
        assert insurance_pct == pytest.approx(20, rel=0.01)
        assert opportunity_pct == pytest.approx(40, rel=0.01)

    def test_zero_inventory(self):
        """Test with zero inventory."""
        costs = calculate_carrying_cost_components(
            inventory_barrels=0, duration_months=3, cost_per_barrel_month=1.5
        )

        assert costs["storage_cost"] == 0
        assert costs["insurance_cost"] == 0
        assert costs["opportunity_cost"] == 0
        assert costs["total_carrying_cost"] == 0


class TestCalculateInventoryRequirementsTool:
    """Test the calculate_inventory_requirements MCP tool."""

    def test_tool_creation(self, mock_config):
        """Test that tool can be created."""
        tool = get_calculate_inventory_requirements_tool(mock_config)
        assert callable(tool)

    def test_default_parameters(self, mock_config):
        """Test tool with default parameters."""
        tool = get_calculate_inventory_requirements_tool(mock_config)
        result = tool()

        assert "current_inventory_barrels" in result
        assert "recommended_safety_stock_barrels" in result
        assert "additional_storage_needed_barrels" in result
        assert "safety_stock_increase_percentage" in result
        assert "service_level_percentage" in result
        assert "rationale" in result
        assert "formula_used" in result
        assert "assumptions" in result
        assert "confidence" in result

        # Default risk level is medium → 97.5% service level
        assert result["service_level_percentage"] == 97.5
        assert result["risk_level"] == "medium"

    def test_low_risk_level(self, mock_config):
        """Test tool with low risk level."""
        tool = get_calculate_inventory_requirements_tool(mock_config)
        result = tool(risk_level="low")

        assert result["risk_level"] == "low"
        assert result["service_level_percentage"] == 95.0  # Lower service level

    def test_high_risk_level(self, mock_config):
        """Test tool with high risk level."""
        tool = get_calculate_inventory_requirements_tool(mock_config)
        result = tool(risk_level="high")

        assert result["risk_level"] == "high"
        assert result["service_level_percentage"] == 99.0  # Higher service level

    def test_higher_risk_increases_safety_stock(self, mock_config):
        """Test that higher risk levels increase recommended safety stock."""
        tool = get_calculate_inventory_requirements_tool(mock_config)

        result_low = tool(risk_level="low")
        result_medium = tool(risk_level="medium")
        result_high = tool(risk_level="high")

        # Higher risk should recommend more safety stock
        assert (
            result_high["recommended_safety_stock_barrels"]
            > result_medium["recommended_safety_stock_barrels"]
        )
        assert (
            result_medium["recommended_safety_stock_barrels"]
            > result_low["recommended_safety_stock_barrels"]
        )

    def test_days_of_supply_calculation(self, mock_config):
        """Test days of supply calculation."""
        tool = get_calculate_inventory_requirements_tool(mock_config)

        result = tool(current_inventory_barrels=500000, daily_demand_barrels=50000)

        expected_days = 500000 / 50000  # 10 days
        assert result["current_days_of_supply"] == pytest.approx(
            expected_days, rel=0.01
        )

    def test_sufficient_inventory_no_increase(self, mock_config):
        """Test that sufficient inventory results in no increase recommendation."""
        tool = get_calculate_inventory_requirements_tool(mock_config)

        # Very large inventory relative to demand
        result = tool(
            current_inventory_barrels=5000000,
            daily_demand_barrels=50000,
            demand_std_dev_barrels=5000,
            lead_time_days=21,
            risk_level="low",
        )

        # Should not need additional storage
        assert result["additional_storage_needed_barrels"] == 0
        assert result["safety_stock_increase_percentage"] == 0

    def test_insufficient_inventory_increase(self, mock_config):
        """Test that insufficient inventory results in increase recommendation."""
        tool = get_calculate_inventory_requirements_tool(mock_config)

        # Low inventory relative to demand and lead time
        result = tool(
            current_inventory_barrels=100000,
            daily_demand_barrels=50000,
            demand_std_dev_barrels=5000,
            lead_time_days=21,
            risk_level="high",
        )

        # Should need significant additional storage
        assert result["additional_storage_needed_barrels"] > 0
        assert result["safety_stock_increase_percentage"] > 0

    def test_result_structure(self, mock_config):
        """Test that result has all required fields with correct types."""
        tool = get_calculate_inventory_requirements_tool(mock_config)
        result = tool()

        # Check numeric fields
        assert isinstance(result["current_inventory_barrels"], (int, float))
        assert isinstance(result["recommended_safety_stock_barrels"], (int, float))
        assert isinstance(result["additional_storage_needed_barrels"], (int, float))
        assert isinstance(result["safety_stock_increase_percentage"], (int, float))
        assert isinstance(result["service_level_percentage"], (int, float))

        # Check string fields
        assert isinstance(result["rationale"], str)
        assert isinstance(result["formula_used"], str)
        assert isinstance(result["confidence"], str)

        # Check list fields
        assert isinstance(result["assumptions"], list)
        assert len(result["assumptions"]) > 0

    def test_formula_documented(self, mock_config):
        """Test that the formula is documented in results."""
        tool = get_calculate_inventory_requirements_tool(mock_config)
        result = tool()

        assert "z-score" in result["formula_used"].lower()


class TestCalculateCarryingCostsTool:
    """Test the calculate_carrying_costs MCP tool."""

    def test_tool_creation(self, mock_config):
        """Test that tool can be created."""
        tool = get_calculate_carrying_costs_tool(mock_config)
        assert callable(tool)

    def test_default_parameters(self, mock_config):
        """Test tool with default parameters."""
        tool = get_calculate_carrying_costs_tool(mock_config)
        result = tool()

        assert "inventory_increase_barrels" in result
        assert "duration_months" in result
        assert "cost_per_barrel_month" in result
        assert "storage_cost_usd" in result
        assert "insurance_cost_usd" in result
        assert "opportunity_cost_usd" in result
        assert "total_carrying_cost_usd" in result
        assert "monthly_carrying_cost_usd" in result
        assert "cost_breakdown" in result
        assert "assumptions" in result

    def test_cost_calculation_accuracy(self, mock_config):
        """Test accuracy of cost calculations."""
        tool = get_calculate_carrying_costs_tool(mock_config)

        result = tool(
            inventory_increase_barrels=100000,
            duration_months=3,
            cost_per_barrel_month=1.5,
        )

        # Expected:
        # Total = 100,000 × 3 × $1.50 = $450,000
        assert result["total_carrying_cost_usd"] == pytest.approx(450000, rel=0.01)

        # Monthly = $450,000 / 3 = $150,000
        assert result["monthly_carrying_cost_usd"] == pytest.approx(150000, rel=0.01)

    def test_cost_scales_with_inventory(self, mock_config):
        """Test that costs scale proportionally with inventory."""
        tool = get_calculate_carrying_costs_tool(mock_config)

        result_small = tool(inventory_increase_barrels=50000, duration_months=3)
        result_large = tool(inventory_increase_barrels=100000, duration_months=3)

        assert result_large["total_carrying_cost_usd"] == pytest.approx(
            result_small["total_carrying_cost_usd"] * 2, rel=0.01
        )

    def test_cost_scales_with_duration(self, mock_config):
        """Test that costs scale proportionally with duration."""
        tool = get_calculate_carrying_costs_tool(mock_config)

        result_short = tool(inventory_increase_barrels=100000, duration_months=3)
        result_long = tool(inventory_increase_barrels=100000, duration_months=6)

        assert result_long["total_carrying_cost_usd"] == pytest.approx(
            result_short["total_carrying_cost_usd"] * 2, rel=0.01
        )

    def test_cost_breakdown_structure(self, mock_config):
        """Test cost breakdown structure."""
        tool = get_calculate_carrying_costs_tool(mock_config)
        result = tool()

        breakdown = result["cost_breakdown"]
        assert "storage_percentage" in breakdown
        assert "insurance_percentage" in breakdown
        assert "opportunity_cost_percentage" in breakdown

        # Should sum to 100%
        total_percentage = (
            breakdown["storage_percentage"]
            + breakdown["insurance_percentage"]
            + breakdown["opportunity_cost_percentage"]
        )
        assert total_percentage == 100

    def test_component_costs_sum_to_total(self, mock_config):
        """Test that component costs sum to total."""
        tool = get_calculate_carrying_costs_tool(mock_config)
        result = tool()

        components_sum = (
            result["storage_cost_usd"]
            + result["insurance_cost_usd"]
            + result["opportunity_cost_usd"]
        )

        assert components_sum == pytest.approx(
            result["total_carrying_cost_usd"], rel=0.01
        )

    def test_monthly_cost_calculation(self, mock_config):
        """Test monthly cost calculation."""
        tool = get_calculate_carrying_costs_tool(mock_config)
        result = tool(duration_months=6)

        expected_monthly = result["total_carrying_cost_usd"] / 6
        assert result["monthly_carrying_cost_usd"] == pytest.approx(
            expected_monthly, rel=0.01
        )

    def test_zero_inventory(self, mock_config):
        """Test with zero inventory increase."""
        tool = get_calculate_carrying_costs_tool(mock_config)
        result = tool(inventory_increase_barrels=0)

        assert result["total_carrying_cost_usd"] == 0
        assert result["storage_cost_usd"] == 0
        assert result["insurance_cost_usd"] == 0
        assert result["opportunity_cost_usd"] == 0

    def test_result_structure(self, mock_config):
        """Test that result has all required fields with correct types."""
        tool = get_calculate_carrying_costs_tool(mock_config)
        result = tool()

        # Check numeric fields
        assert isinstance(result["inventory_increase_barrels"], (int, float))
        assert isinstance(result["duration_months"], int)
        assert isinstance(result["cost_per_barrel_month"], (int, float))
        assert isinstance(result["storage_cost_usd"], (int, float))
        assert isinstance(result["insurance_cost_usd"], (int, float))
        assert isinstance(result["opportunity_cost_usd"], (int, float))
        assert isinstance(result["total_carrying_cost_usd"], (int, float))
        assert isinstance(result["monthly_carrying_cost_usd"], (int, float))

        # Check nested objects
        assert isinstance(result["cost_breakdown"], dict)
        assert isinstance(result["assumptions"], list)

    def test_assumptions_documented(self, mock_config):
        """Test that assumptions are documented."""
        tool = get_calculate_carrying_costs_tool(mock_config)
        result = tool()

        assert isinstance(result["assumptions"], list)
        assert len(result["assumptions"]) > 0
        # Should mention percentages
        assumptions_text = " ".join(result["assumptions"])
        assert "40%" in assumptions_text or "20%" in assumptions_text
