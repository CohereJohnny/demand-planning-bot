"""Financial analysis tools for the Demand Planning Bot.

This module provides tools to calculate revenue impacts from stockouts,
ROI for inventory investments, and other financial metrics.
"""

import logging
from typing import Dict, Literal

from src.demand_planning_bot.utils.config import Config

logger = logging.getLogger(__name__)


def calculate_stockout_revenue_loss(
    stockout_days: int,
    daily_demand_barrels: float,
    price_per_barrel: float,
    customer_impact_factor: float = 1.0,
) -> Dict:
    """Calculate revenue loss from stockouts.

    Args:
        stockout_days: Number of days with stockouts.
        daily_demand_barrels: Average daily demand in barrels.
        price_per_barrel: Price per barrel (USD).
        customer_impact_factor: Multiplier for customer impact (1.0-1.5).
                                1.0 = no additional impact
                                1.2 = 20% additional loss from customer dissatisfaction
                                1.5 = 50% additional loss from customer churn

    Returns:
        Dictionary with revenue loss breakdown.
    """
    # Direct revenue loss from unsold barrels
    barrels_not_sold = stockout_days * daily_demand_barrels
    direct_revenue_loss = barrels_not_sold * price_per_barrel

    # Penalty costs (assume 10% of direct loss for contract violations)
    penalty_percentage = 0.10
    penalty_costs = direct_revenue_loss * penalty_percentage

    # Customer impact (additional loss from dissatisfaction/churn)
    customer_impact_multiplier = customer_impact_factor - 1.0  # 0.0 to 0.5
    customer_impact_loss = direct_revenue_loss * customer_impact_multiplier

    # Total revenue impact
    total_impact = direct_revenue_loss + penalty_costs + customer_impact_loss

    return {
        "barrels_not_sold": round(barrels_not_sold, 0),
        "direct_revenue_loss": round(direct_revenue_loss, 2),
        "penalty_costs": round(penalty_costs, 2),
        "customer_impact_loss": round(customer_impact_loss, 2),
        "total_revenue_impact": round(total_impact, 2),
    }


def calculate_roi_metrics(
    investment_cost: float,
    expected_annual_benefit: float,
    time_period_months: int,
    discount_rate: float = 0.05,
) -> Dict:
    """Calculate ROI and related financial metrics.

    Args:
        investment_cost: Initial investment (USD).
        expected_annual_benefit: Expected annual benefit/savings (USD).
        time_period_months: Investment time horizon (months).
        discount_rate: Annual discount rate (default 5%).

    Returns:
        Dictionary with ROI metrics.
    """
    # Calculate period benefit (prorated for timeframe)
    time_period_years = time_period_months / 12
    period_benefit = expected_annual_benefit * time_period_years

    # Standard ROI: (Benefit - Cost) / Cost * 100
    if investment_cost > 0:
        roi_percentage = ((period_benefit - investment_cost) / investment_cost) * 100
    else:
        roi_percentage = 0.0

    # Net benefit
    net_benefit = period_benefit - investment_cost

    # Payback period in months
    if expected_annual_benefit > 0:
        payback_period_months = (investment_cost / expected_annual_benefit) * 12
    else:
        payback_period_months = float("inf")

    # Simple NPV (using annual discount rate)
    # NPV = -Investment + Sum(Benefit / (1 + r)^t) for each year
    npv = -investment_cost
    for year in range(1, int(time_period_years) + 1):
        discounted_benefit = expected_annual_benefit / ((1 + discount_rate) ** year)
        npv += discounted_benefit

    # Recommendation based on ROI
    if roi_percentage >= 30:
        recommendation = "excellent"
    elif roi_percentage >= 15:
        recommendation = "good"
    elif roi_percentage >= 5:
        recommendation = "marginal"
    else:
        recommendation = "poor"

    return {
        "roi_percentage": round(roi_percentage, 2),
        "net_benefit": round(net_benefit, 2),
        "payback_period_months": (
            round(payback_period_months, 1)
            if payback_period_months != float("inf")
            else None
        ),
        "npv": round(npv, 2),
        "recommendation": recommendation,
    }


def get_calculate_revenue_impact_tool(config: Config):
    """Provides an MCP tool to calculate revenue impact from stockouts.

    Args:
        config: The application configuration.

    Returns:
        A callable MCP tool function.
    """

    def calculate_revenue_impact(
        stockout_days: int = 3,
        daily_demand_barrels: float = 50000,
        price_per_barrel: float = 85.0,
        customer_impact_factor: float = 1.2,
    ) -> Dict:
        """Calculate potential revenue loss from stockout scenarios.

        Estimates the financial impact of stockouts including direct revenue loss,
        contract penalties, and customer satisfaction effects. Helps quantify the
        cost of inventory shortfalls and justifies inventory investments.

        Args:
            stockout_days: Number of days with stockouts (1-30).
            daily_demand_barrels: Average daily demand in barrels.
            price_per_barrel: Current price per barrel (USD).
            customer_impact_factor: Customer satisfaction multiplier (1.0-1.5).
                                    1.0 = no additional impact
                                    1.2 = 20% additional loss from dissatisfaction
                                    1.5 = 50% additional loss from customer churn

        Returns:
            Dictionary with revenue impact analysis including:
            - barrels_not_sold: Quantity lost
            - direct_revenue_loss: Base revenue loss
            - penalty_costs: Contract violation penalties
            - customer_impact_loss: Additional loss from customer dissatisfaction
            - total_revenue_impact: Total financial impact
            - assumptions: Calculation assumptions
        """
        logger.info(
            f"calculate_revenue_impact called: stockout_days={stockout_days}, "
            f"demand={daily_demand_barrels}, price={price_per_barrel}, "
            f"customer_factor={customer_impact_factor}"
        )

        # Validate inputs
        if stockout_days < 1 or stockout_days > 30:
            return {
                "error": "stockout_days must be between 1 and 30",
                "provided": stockout_days,
            }

        if customer_impact_factor < 1.0 or customer_impact_factor > 1.5:
            return {
                "error": "customer_impact_factor must be between 1.0 and 1.5",
                "provided": customer_impact_factor,
            }

        # Calculate revenue loss
        loss_data = calculate_stockout_revenue_loss(
            stockout_days=stockout_days,
            daily_demand_barrels=daily_demand_barrels,
            price_per_barrel=price_per_barrel,
            customer_impact_factor=customer_impact_factor,
        )

        result = {
            "stockout_days": stockout_days,
            "daily_demand_barrels": round(daily_demand_barrels, 0),
            "price_per_barrel": price_per_barrel,
            "currency": "USD",
            **loss_data,
            "customer_impact_factor": customer_impact_factor,
            "assumptions": [
                f"Penalty costs: 10% of direct revenue loss for contract violations",
                f"Customer impact: {(customer_impact_factor - 1.0) * 100:.0f}% additional loss from dissatisfaction",
                f"Demand remains constant at {daily_demand_barrels:.0f} barrels/day",
                f"Price per barrel: ${price_per_barrel}",
                "No alternative supply sources available during stockout",
            ],
            "confidence": "high",
        }

        logger.info(
            f"Revenue impact calculated: ${loss_data['total_revenue_impact']:,.2f} total loss"
        )
        return result

    return calculate_revenue_impact


def get_calculate_roi_tool(config: Config):
    """Provides an MCP tool to calculate ROI for investments.

    Args:
        config: The application configuration.

    Returns:
        A callable MCP tool function.
    """

    def calculate_roi(
        investment_cost: float = 500000,
        expected_annual_benefit: float = 200000,
        time_period_months: int = 24,
        discount_rate: float = 0.05,
    ) -> Dict:
        """Calculate ROI and financial metrics for inventory or operational investments.

        Calculates return on investment, payback period, and net present value to help
        evaluate whether inventory increases, process improvements, or other investments
        are financially justified.

        Args:
            investment_cost: Initial investment amount (USD).
            expected_annual_benefit: Expected annual benefit or savings (USD).
            time_period_months: Investment evaluation horizon (1-60 months).
            discount_rate: Annual discount rate for NPV (0.01-0.20, default 0.05 = 5%).

        Returns:
            Dictionary with ROI analysis including:
            - roi_percentage: Return on investment (%)
            - net_benefit: Total benefit minus cost
            - payback_period_months: Months to recover investment
            - npv: Net present value
            - recommendation: Investment quality rating
            - assumptions: Calculation assumptions
        """
        logger.info(
            f"calculate_roi called: cost={investment_cost}, "
            f"annual_benefit={expected_annual_benefit}, "
            f"period={time_period_months}mo, discount={discount_rate}"
        )

        # Validate inputs
        if time_period_months < 1 or time_period_months > 60:
            return {
                "error": "time_period_months must be between 1 and 60",
                "provided": time_period_months,
            }

        if discount_rate < 0.01 or discount_rate > 0.20:
            return {
                "error": "discount_rate must be between 0.01 and 0.20",
                "provided": discount_rate,
            }

        # Calculate ROI metrics
        metrics = calculate_roi_metrics(
            investment_cost=investment_cost,
            expected_annual_benefit=expected_annual_benefit,
            time_period_months=time_period_months,
            discount_rate=discount_rate,
        )

        result = {
            "investment_cost": round(investment_cost, 2),
            "expected_annual_benefit": round(expected_annual_benefit, 2),
            "time_period_months": time_period_months,
            "time_period_years": round(time_period_months / 12, 2),
            "discount_rate": discount_rate,
            "currency": "USD",
            **metrics,
            "interpretation": {
                "roi_rating": (
                    "Excellent (≥30%)"
                    if metrics["roi_percentage"] >= 30
                    else "Good (15-30%)"
                    if metrics["roi_percentage"] >= 15
                    else "Marginal (5-15%)"
                    if metrics["roi_percentage"] >= 5
                    else "Poor (<5%)"
                ),
                "payback_assessment": (
                    "Quick payback (<12 months)"
                    if metrics["payback_period_months"]
                    and metrics["payback_period_months"] < 12
                    else "Moderate payback (12-24 months)"
                    if metrics["payback_period_months"]
                    and metrics["payback_period_months"] < 24
                    else "Slow payback (>24 months)"
                    if metrics["payback_period_months"]
                    else "Payback not achievable"
                ),
                "npv_verdict": (
                    "Positive NPV - value creating"
                    if metrics["npv"] > 0
                    else "Negative NPV - value destroying"
                ),
            },
            "assumptions": [
                f"Annual benefit remains constant at ${expected_annual_benefit:,.0f}",
                f"Discount rate: {discount_rate * 100}% per year",
                f"Evaluation period: {time_period_months} months",
                "Benefits begin accruing immediately after investment",
                "No additional costs or benefits beyond those specified",
            ],
            "confidence": "high",
        }

        logger.info(
            f"ROI calculated: {metrics['roi_percentage']:.2f}% over {time_period_months} months"
        )
        return result

    return calculate_roi
