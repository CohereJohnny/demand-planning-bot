"""Market data tools for oil prices using EIA API.

Provides MCP tools for retrieving current and historical oil prices
(Brent crude, WTI) from the U.S. Energy Information Administration API.
"""

import logging
from datetime import datetime
from typing import Dict, Literal, Optional

from src.demand_planning_bot.utils.api_client import APIClient, APIError, RateLimitError
from src.demand_planning_bot.utils.config import Config

logger = logging.getLogger(__name__)

# EIA API base URL
EIA_API_BASE = "https://api.eia.gov/v2"

# EIA Series IDs for petroleum spot prices
# These are the official EIA series identifiers
EIA_SERIES_IDS = {
    "brent": "PET.RBRTE.D",  # Brent crude spot price ($/barrel)
    "wti": "PET.RWTC.D",  # WTI crude spot price ($/barrel)
}


class EIAAPIClient:
    """Client for the EIA (Energy Information Administration) API."""

    def __init__(self, api_key: Optional[str], config: Config):
        """Initialize the EIA API client.

        Args:
            api_key: EIA API key (optional, will use fallback if None).
            config: Configuration object.
        """
        self.api_key = api_key
        self.config = config
        self.client = APIClient(timeout=30.0, max_retries=3)

    def get_spot_price(self, product: Literal["brent", "wti"], limit: int = 1) -> Dict:
        """Get spot price for oil product from EIA API.

        Args:
            product: Oil product type ("brent" or "wti").
            limit: Number of data points to return (default: 1 for current).

        Returns:
            Dictionary with price data.

        Raises:
            APIError: If API call fails.
        """
        if not self.api_key:
            raise APIError("EIA API key not configured")

        series_id = EIA_SERIES_IDS.get(product)
        if not series_id:
            raise ValueError(f"Unknown product: {product}")

        # Build API URL
        url = f"{EIA_API_BASE}/seriesid/{series_id}"

        params = {"api_key": self.api_key, "length": limit}

        try:
            logger.debug(f"Fetching EIA data for {product} (series: {series_id})")
            response = self.client.get(url, params=params)

            # Parse EIA response format
            if "response" not in response:
                raise APIError("Invalid EIA API response format")

            data = response["response"]

            if "data" not in data or not data["data"]:
                raise APIError("No data available from EIA API")

            return data

        except RateLimitError as e:
            logger.error(f"EIA API rate limit exceeded: {e}")
            raise
        except APIError as e:
            logger.error(f"EIA API error: {e}")
            raise


def get_fallback_market_data(product: Literal["brent", "wti"]) -> Dict:
    """Get fallback market data when API is unavailable.

    Args:
        product: Oil product type ("brent" or "wti").

    Returns:
        Dictionary with simulated market data.
    """
    # Realistic price ranges based on historical data
    fallback_prices = {
        "brent": {
            "price": 85.50,
            "product_name": "Brent Crude Oil Spot Price",
            "unit": "USD per barrel",
            "typical_range": "75-95 USD/barrel",
        },
        "wti": {
            "price": 81.25,
            "product_name": "WTI Crude Oil Spot Price",
            "unit": "USD per barrel",
            "typical_range": "70-90 USD/barrel",
        },
    }

    price_info = fallback_prices.get(product, fallback_prices["brent"])

    return {
        "price": price_info["price"],
        "product": product.upper(),
        "product_name": price_info["product_name"],
        "currency": "USD",
        "unit": price_info["unit"],
        "date": datetime.now().strftime("%Y-%m-%d"),
        "typical_range": price_info["typical_range"],
        "data_source": "fallback",
        "note": "Using simulated data - API unavailable or not configured",
        "confidence": "medium",
    }


def get_market_prices_tool(
    config: Config,
) -> callable:
    """Create the get_market_prices MCP tool.

    Args:
        config: Configuration object with API keys.

    Returns:
        MCP tool function.
    """

    def get_market_prices(
        product: Literal["brent", "wti"] = "brent",
        timeframe: Literal["current", "recent"] = "current",
    ) -> Dict:
        """Get current or recent oil prices from EIA API.

        Retrieves spot prices for Brent crude or WTI (West Texas Intermediate)
        from the U.S. Energy Information Administration. Falls back to simulated
        data if API is unavailable.

        Args:
            product: Oil product type - "brent" for Brent crude or "wti" for WTI.
            timeframe: "current" for latest price, "recent" for last few days.

        Returns:
            Dictionary with price information including:
            - price: Current spot price
            - product: Product identifier
            - currency: Currency (USD)
            - unit: Unit of measure (USD per barrel)
            - date: Price date
            - data_source: "eia_api" or "fallback"
            - confidence: Data confidence level
        """
        logger.info(
            f"get_market_prices called: product={product}, timeframe={timeframe}"
        )

        # Determine how many data points to fetch
        limit = 1 if timeframe == "current" else 5

        # Try to use EIA API if configured
        if config.has_eia_api_key:
            try:
                client = EIAAPIClient(config.eia_api_key, config)
                api_data = client.get_spot_price(product, limit=limit)

                # Parse the most recent price from EIA data
                latest = api_data["data"][0]

                result = {
                    "price": float(latest["value"]),
                    "product": product.upper(),
                    "product_name": f"{product.upper()} Crude Oil Spot Price",
                    "currency": "USD",
                    "unit": "USD per barrel",
                    "date": latest["period"],
                    "data_source": "eia_api",
                    "confidence": "high",
                    "api_note": "Data from U.S. Energy Information Administration",
                }

                logger.info(
                    f"Successfully retrieved price from EIA: {result['price']} {result['unit']}"
                )
                return result

            except (APIError, RateLimitError) as e:
                logger.warning(
                    f"Failed to fetch from EIA API, using fallback data: {e}"
                )
                # Fall through to fallback data

        # Use fallback data
        logger.info("Using fallback market data")
        return get_fallback_market_data(product)

    return get_market_prices
