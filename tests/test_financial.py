"""Unit tests for financial analysis tools."""

import pytest

from src.demand_planning_bot.tools.financial import (
    calculate_roi_metrics,
    calculate_stockout_revenue_loss,
    get_calculate_revenue_impact_tool,
    get_calculate_roi_tool,
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


class TestCalculateStockoutRevenueLoss:
    """Test stockout revenue loss calculations."""

    def test_basic_revenue_loss(self):
        """Test basic revenue loss calculation."""
        result = calculate_stockout_revenue_loss(
            stockout_days=3,
            daily_demand_barrels=50000,
            price_per_barrel=85.0,
            customer_impact_factor=1.0,
        )

        # Direct loss: 3 days * 50,000 barrels * $85 = $12,750,000
        expected_direct_loss = 3 * 50000 * 85.0
        assert result["direct_revenue_loss"] == pytest.approx(
            expected_direct_loss, rel=0.01
        )

        # Barrels not sold
        assert result["barrels_not_sold"] == 150000

        # Penalty costs: 10% of direct loss
        expected_penalty = expected_direct_loss * 0.10
        assert result["penalty_costs"] == pytest.approx(expected_penalty, rel=0.01)

        # No customer impact with factor 1.0
        assert result["customer_impact_loss"] == 0.0

    def test_customer_impact_20_percent(self):
        """Test customer impact factor of 1.2 (20% additional loss)."""
        result = calculate_stockout_revenue_loss(
            stockout_days=3,
            daily_demand_barrels=50000,
            price_per_barrel=85.0,
            customer_impact_factor=1.2,
        )

        direct_loss = 3 * 50000 * 85.0
        # Customer impact: 20% additional loss (factor - 1.0)
        expected_customer_loss = direct_loss * 0.2
        assert result["customer_impact_loss"] == pytest.approx(
            expected_customer_loss, rel=0.01
        )

    def test_customer_impact_50_percent(self):
        """Test customer impact factor of 1.5 (50% additional loss)."""
        result = calculate_stockout_revenue_loss(
            stockout_days=5,
            daily_demand_barrels=40000,
            price_per_barrel=90.0,
            customer_impact_factor=1.5,
        )

        direct_loss = 5 * 40000 * 90.0
        # Customer impact: 50% additional loss
        expected_customer_loss = direct_loss * 0.5
        assert result["customer_impact_loss"] == pytest.approx(
            expected_customer_loss, rel=0.01
        )

    def test_total_impact_calculation(self):
        """Test that total impact is sum of all components."""
        result = calculate_stockout_revenue_loss(
            stockout_days=2,
            daily_demand_barrels=30000,
            price_per_barrel=80.0,
            customer_impact_factor=1.3,
        )

        total = (
            result["direct_revenue_loss"]
            + result["penalty_costs"]
            + result["customer_impact_loss"]
        )
        assert result["total_revenue_impact"] == pytest.approx(total, rel=0.01)

    def test_scales_with_stockout_days(self):
        """Test that loss scales proportionally with stockout days."""
        result_1_day = calculate_stockout_revenue_loss(
            stockout_days=1,
            daily_demand_barrels=50000,
            price_per_barrel=85.0,
            customer_impact_factor=1.0,
        )
        result_3_days = calculate_stockout_revenue_loss(
            stockout_days=3,
            daily_demand_barrels=50000,
            price_per_barrel=85.0,
            customer_impact_factor=1.0,
        )

        assert result_3_days["direct_revenue_loss"] == pytest.approx(
            result_1_day["direct_revenue_loss"] * 3, rel=0.01
        )


class TestCalculateROIMetrics:
    """Test ROI metric calculations."""

    def test_basic_roi_calculation(self):
        """Test basic ROI calculation."""
        # Investment: $500k, Annual benefit: $200k, Time: 24 months (2 years)
        # Period benefit: $200k * 2 = $400k
        # ROI: (400k - 500k) / 500k * 100 = -20%
        result = calculate_roi_metrics(
            investment_cost=500000,
            expected_annual_benefit=200000,
            time_period_months=24,
            discount_rate=0.05,
        )

        assert result["roi_percentage"] == pytest.approx(-20.0, rel=0.01)
        assert result["net_benefit"] == pytest.approx(-100000, rel=0.01)

    def test_positive_roi(self):
        """Test positive ROI scenario."""
        # Investment: $500k, Annual benefit: $300k, Time: 24 months
        # Period benefit: $300k * 2 = $600k
        # ROI: (600k - 500k) / 500k * 100 = 20%
        result = calculate_roi_metrics(
            investment_cost=500000,
            expected_annual_benefit=300000,
            time_period_months=24,
            discount_rate=0.05,
        )

        assert result["roi_percentage"] == pytest.approx(20.0, rel=0.01)
        assert result["net_benefit"] == pytest.approx(100000, rel=0.01)

    def test_payback_period_calculation(self):
        """Test payback period calculation."""
        # Investment: $600k, Annual benefit: $200k
        # Payback: 600k / 200k * 12 = 36 months
        result = calculate_roi_metrics(
            investment_cost=600000,
            expected_annual_benefit=200000,
            time_period_months=60,
            discount_rate=0.05,
        )

        assert result["payback_period_months"] == pytest.approx(36.0, rel=0.01)

    def test_recommendation_excellent(self):
        """Test recommendation for excellent ROI (≥30%)."""
        result = calculate_roi_metrics(
            investment_cost=100000,
            expected_annual_benefit=150000,
            time_period_months=12,
            discount_rate=0.05,
        )

        # ROI: (150k - 100k) / 100k * 100 = 50%
        assert result["roi_percentage"] >= 30
        assert result["recommendation"] == "excellent"

    def test_recommendation_good(self):
        """Test recommendation for good ROI (15-30%)."""
        result = calculate_roi_metrics(
            investment_cost=100000,
            expected_annual_benefit=120000,
            time_period_months=12,
            discount_rate=0.05,
        )

        # ROI: (120k - 100k) / 100k * 100 = 20%
        assert 15 <= result["roi_percentage"] < 30
        assert result["recommendation"] == "good"

    def test_recommendation_marginal(self):
        """Test recommendation for marginal ROI (5-15%)."""
        result = calculate_roi_metrics(
            investment_cost=100000,
            expected_annual_benefit=110000,
            time_period_months=12,
            discount_rate=0.05,
        )

        # ROI: (110k - 100k) / 100k * 100 = 10%
        assert 5 <= result["roi_percentage"] < 15
        assert result["recommendation"] == "marginal"

    def test_recommendation_poor(self):
        """Test recommendation for poor ROI (<5%)."""
        result = calculate_roi_metrics(
            investment_cost=100000,
            expected_annual_benefit=103000,
            time_period_months=12,
            discount_rate=0.05,
        )

        # ROI: (103k - 100k) / 100k * 100 = 3%
        assert result["roi_percentage"] < 5
        assert result["recommendation"] == "poor"

    def test_npv_calculation(self):
        """Test NPV calculation with discount rate."""
        result = calculate_roi_metrics(
            investment_cost=100000,
            expected_annual_benefit=60000,
            time_period_months=24,
            discount_rate=0.10,
        )

        # NPV should be positive but less than simple net benefit
        # due to time value of money
        assert result["npv"] > 0
        assert result["npv"] < result["net_benefit"]

    def test_zero_investment_cost(self):
        """Test handling of zero investment cost."""
        result = calculate_roi_metrics(
            investment_cost=0,
            expected_annual_benefit=50000,
            time_period_months=12,
            discount_rate=0.05,
        )

        # ROI should be 0 to avoid division by zero
        assert result["roi_percentage"] == 0.0

    def test_zero_annual_benefit(self):
        """Test handling of zero annual benefit."""
        result = calculate_roi_metrics(
            investment_cost=100000,
            expected_annual_benefit=0,
            time_period_months=12,
            discount_rate=0.05,
        )

        # Payback period should be None (infinity)
        assert result["payback_period_months"] is None


class TestCalculateRevenueImpactTool:
    """Test the calculate_revenue_impact MCP tool."""

    def test_tool_creation(self, mock_config):
        """Test that tool can be created."""
        tool = get_calculate_revenue_impact_tool(mock_config)
        assert callable(tool)

    def test_default_parameters(self, mock_config):
        """Test tool with default parameters."""
        tool = get_calculate_revenue_impact_tool(mock_config)
        result = tool()

        assert "stockout_days" in result
        assert "daily_demand_barrels" in result
        assert "price_per_barrel" in result
        assert "direct_revenue_loss" in result
        assert "penalty_costs" in result
        assert "customer_impact_loss" in result
        assert "total_revenue_impact" in result
        assert "assumptions" in result
        assert "confidence" in result

    def test_custom_parameters(self, mock_config):
        """Test tool with custom parameters."""
        tool = get_calculate_revenue_impact_tool(mock_config)
        result = tool(
            stockout_days=5,
            daily_demand_barrels=60000,
            price_per_barrel=90.0,
            customer_impact_factor=1.3,
        )

        assert result["stockout_days"] == 5
        assert result["daily_demand_barrels"] == 60000
        assert result["price_per_barrel"] == 90.0
        assert result["customer_impact_factor"] == 1.3

    def test_validation_stockout_days_too_low(self, mock_config):
        """Test validation for stockout_days < 1."""
        tool = get_calculate_revenue_impact_tool(mock_config)
        result = tool(stockout_days=0)

        assert "error" in result
        assert "stockout_days must be between 1 and 30" in result["error"]

    def test_validation_stockout_days_too_high(self, mock_config):
        """Test validation for stockout_days > 30."""
        tool = get_calculate_revenue_impact_tool(mock_config)
        result = tool(stockout_days=31)

        assert "error" in result

    def test_validation_customer_impact_factor_too_low(self, mock_config):
        """Test validation for customer_impact_factor < 1.0."""
        tool = get_calculate_revenue_impact_tool(mock_config)
        result = tool(customer_impact_factor=0.9)

        assert "error" in result
        assert "customer_impact_factor must be between 1.0 and 1.5" in result["error"]

    def test_validation_customer_impact_factor_too_high(self, mock_config):
        """Test validation for customer_impact_factor > 1.5."""
        tool = get_calculate_revenue_impact_tool(mock_config)
        result = tool(customer_impact_factor=1.6)

        assert "error" in result

    def test_result_structure(self, mock_config):
        """Test that result has all required fields."""
        tool = get_calculate_revenue_impact_tool(mock_config)
        result = tool()

        required_fields = [
            "stockout_days",
            "daily_demand_barrels",
            "price_per_barrel",
            "currency",
            "barrels_not_sold",
            "direct_revenue_loss",
            "penalty_costs",
            "customer_impact_loss",
            "total_revenue_impact",
            "customer_impact_factor",
            "assumptions",
            "confidence",
        ]

        for field in required_fields:
            assert field in result


class TestCalculateROITool:
    """Test the calculate_roi MCP tool."""

    def test_tool_creation(self, mock_config):
        """Test that tool can be created."""
        tool = get_calculate_roi_tool(mock_config)
        assert callable(tool)

    def test_default_parameters(self, mock_config):
        """Test tool with default parameters."""
        tool = get_calculate_roi_tool(mock_config)
        result = tool()

        assert "investment_cost" in result
        assert "expected_annual_benefit" in result
        assert "roi_percentage" in result
        assert "net_benefit" in result
        assert "payback_period_months" in result
        assert "npv" in result
        assert "recommendation" in result
        assert "interpretation" in result
        assert "assumptions" in result
        assert "confidence" in result

    def test_custom_parameters(self, mock_config):
        """Test tool with custom parameters."""
        tool = get_calculate_roi_tool(mock_config)
        result = tool(
            investment_cost=1000000,
            expected_annual_benefit=400000,
            time_period_months=36,
            discount_rate=0.08,
        )

        assert result["investment_cost"] == 1000000
        assert result["expected_annual_benefit"] == 400000
        assert result["time_period_months"] == 36
        assert result["discount_rate"] == 0.08

    def test_validation_time_period_too_low(self, mock_config):
        """Test validation for time_period_months < 1."""
        tool = get_calculate_roi_tool(mock_config)
        result = tool(time_period_months=0)

        assert "error" in result
        assert "time_period_months must be between 1 and 60" in result["error"]

    def test_validation_time_period_too_high(self, mock_config):
        """Test validation for time_period_months > 60."""
        tool = get_calculate_roi_tool(mock_config)
        result = tool(time_period_months=61)

        assert "error" in result

    def test_validation_discount_rate_too_low(self, mock_config):
        """Test validation for discount_rate < 0.01."""
        tool = get_calculate_roi_tool(mock_config)
        result = tool(discount_rate=0.005)

        assert "error" in result
        assert "discount_rate must be between 0.01 and 0.20" in result["error"]

    def test_validation_discount_rate_too_high(self, mock_config):
        """Test validation for discount_rate > 0.20."""
        tool = get_calculate_roi_tool(mock_config)
        result = tool(discount_rate=0.25)

        assert "error" in result

    def test_interpretation_section(self, mock_config):
        """Test that interpretation section is included."""
        tool = get_calculate_roi_tool(mock_config)
        result = tool()

        assert "interpretation" in result
        assert "roi_rating" in result["interpretation"]
        assert "payback_assessment" in result["interpretation"]
        assert "npv_verdict" in result["interpretation"]

    def test_result_structure(self, mock_config):
        """Test that result has all required fields."""
        tool = get_calculate_roi_tool(mock_config)
        result = tool()

        required_fields = [
            "investment_cost",
            "expected_annual_benefit",
            "time_period_months",
            "time_period_years",
            "discount_rate",
            "currency",
            "roi_percentage",
            "net_benefit",
            "payback_period_months",
            "npv",
            "recommendation",
            "interpretation",
            "assumptions",
            "confidence",
        ]

        for field in required_fields:
            assert field in result
