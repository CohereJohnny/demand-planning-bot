"""Unit tests for market data tools."""

from unittest.mock import Mock, patch

import pytest

from src.demand_planning_bot.tools.market_data import (
    EIAAPIClient,
    get_fallback_market_data,
    get_market_prices_tool,
)
from src.demand_planning_bot.utils.api_client import APIError
from src.demand_planning_bot.utils.config import Config


@pytest.fixture
def mock_config():
    """Create a mock configuration object."""
    config = Mock(spec=Config)
    config.has_eia_api_key = True
    config.eia_api_key = "test_api_key"
    config.debug = False
    return config


@pytest.fixture
def mock_config_no_api_key():
    """Create a mock configuration without API key."""
    config = Mock(spec=Config)
    config.has_eia_api_key = False
    config.eia_api_key = None
    config.debug = False
    return config


class TestEIAAPIClient:
    """Tests for EIA API client."""

    def test_init(self, mock_config):
        """Test client initialization."""
        client = EIAAPIClient("test_key", mock_config)
        assert client.api_key == "test_key"
        assert client.config == mock_config

    def test_get_spot_price_no_api_key(self, mock_config):
        """Test that missing API key raises error."""
        from src.demand_planning_bot.utils.api_client import APIError as ActualAPIError

        client = EIAAPIClient(None, mock_config)
        with pytest.raises(ActualAPIError, match="EIA API key not configured"):
            client.get_spot_price("brent")

    def test_get_spot_price_invalid_product(self, mock_config):
        """Test that invalid product raises error."""
        client = EIAAPIClient("test_key", mock_config)
        with pytest.raises(ValueError, match="Unknown product"):
            client.get_spot_price("invalid")

    @patch("src.demand_planning_bot.tools.market_data.APIClient")
    def test_get_spot_price_success(self, mock_api_client_class, mock_config):
        """Test successful API call."""
        # Mock API response
        mock_response = {
            "response": {
                "data": [
                    {
                        "period": "2025-10-23",
                        "value": 85.50,
                        "series": "PET.RBRTE.D",
                    }
                ]
            }
        }

        # Setup mock
        mock_api_instance = Mock()
        mock_api_instance.get.return_value = mock_response
        mock_api_client_class.return_value = mock_api_instance

        client = EIAAPIClient("test_key", mock_config)
        result = client.get_spot_price("brent", limit=1)

        assert "data" in result
        assert len(result["data"]) == 1
        assert result["data"][0]["value"] == 85.50

    @patch("src.demand_planning_bot.tools.market_data.APIClient")
    def test_get_spot_price_api_error(self, mock_api_client_class, mock_config):
        """Test API error handling."""
        mock_api_instance = Mock()
        mock_api_instance.get.side_effect = APIError("API call failed")
        mock_api_client_class.return_value = mock_api_instance

        client = EIAAPIClient("test_key", mock_config)
        with pytest.raises(APIError, match="API call failed"):
            client.get_spot_price("brent")


class TestFallbackMarketData:
    """Tests for fallback market data."""

    def test_fallback_brent(self):
        """Test fallback data for Brent crude."""
        result = get_fallback_market_data("brent")
        assert result["product"] == "BRENT"
        assert result["price"] == 85.50
        assert result["currency"] == "USD"
        assert result["data_source"] == "fallback"
        assert "date" in result

    def test_fallback_wti(self):
        """Test fallback data for WTI."""
        result = get_fallback_market_data("wti")
        assert result["product"] == "WTI"
        assert result["price"] == 81.25
        assert result["currency"] == "USD"
        assert result["data_source"] == "fallback"


class TestGetMarketPricesTool:
    """Tests for get_market_prices MCP tool."""

    def test_tool_with_fallback_no_api_key(self, mock_config_no_api_key):
        """Test tool returns fallback when no API key configured."""
        tool = get_market_prices_tool(mock_config_no_api_key)
        result = tool(product="brent", timeframe="current")

        assert result["product"] == "BRENT"
        assert result["data_source"] == "fallback"
        assert "price" in result
        assert result["currency"] == "USD"

    @patch("src.demand_planning_bot.tools.market_data.EIAAPIClient")
    def test_tool_with_api_success(self, mock_eia_client_class, mock_config):
        """Test tool with successful API call."""
        # Mock API response
        mock_api_data = {
            "data": [
                {
                    "period": "2025-10-23",
                    "value": 87.25,
                    "series": "PET.RBRTE.D",
                }
            ]
        }

        mock_client_instance = Mock()
        mock_client_instance.get_spot_price.return_value = mock_api_data
        mock_eia_client_class.return_value = mock_client_instance

        tool = get_market_prices_tool(mock_config)
        result = tool(product="brent", timeframe="current")

        assert result["price"] == 87.25
        assert result["product"] == "BRENT"
        assert result["date"] == "2025-10-23"
        assert result["data_source"] == "eia_api"
        assert result["confidence"] == "high"

    @patch("src.demand_planning_bot.tools.market_data.EIAAPIClient")
    def test_tool_api_failure_fallback(self, mock_eia_client_class, mock_config):
        """Test tool falls back when API fails."""
        from src.demand_planning_bot.utils.api_client import APIError as ActualAPIError

        mock_client_instance = Mock()
        mock_client_instance.get_spot_price.side_effect = ActualAPIError("API failed")
        mock_eia_client_class.return_value = mock_client_instance

        tool = get_market_prices_tool(mock_config)
        result = tool(product="wti", timeframe="current")

        # Should fall back to simulated data
        assert result["product"] == "WTI"
        assert result["data_source"] == "fallback"
        assert "price" in result

    def test_tool_recent_timeframe(self, mock_config_no_api_key):
        """Test tool with recent timeframe."""
        tool = get_market_prices_tool(mock_config_no_api_key)
        result = tool(product="brent", timeframe="recent")

        assert result["product"] == "BRENT"
        assert "price" in result
        # Falls back since no API key
        assert result["data_source"] == "fallback"
