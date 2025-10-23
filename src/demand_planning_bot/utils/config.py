"""Configuration management for the Demand Planning MCP Server.

Handles loading environment variables, validation, and providing
configuration to the rest of the application.
"""

import logging
import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Configuration for the Demand Planning MCP Server."""

    # API Keys
    eia_api_key: Optional[str]
    news_api_key: Optional[str]

    # Server Configuration
    server_secret: Optional[str]
    port: int
    debug: bool

    @property
    def has_eia_api_key(self) -> bool:
        """Check if EIA API key is configured."""
        return self.eia_api_key is not None and len(self.eia_api_key) > 0

    @property
    def has_news_api_key(self) -> bool:
        """Check if News API key is configured."""
        return self.news_api_key is not None and len(self.news_api_key) > 0

    @property
    def has_server_secret(self) -> bool:
        """Check if server secret is configured."""
        return self.server_secret is not None and len(self.server_secret) > 0


def load_config() -> Config:
    """Load configuration from environment variables.

    Attempts to load from .env file first, then falls back to system
    environment variables.

    Returns:
        Config: Configuration object with all settings.
    """
    # Load from .env file if it exists
    load_dotenv()

    # Configure logging level
    debug = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Load configuration
    config = Config(
        eia_api_key=os.getenv("EIA_API_KEY"),
        news_api_key=os.getenv("NEWS_API_KEY"),
        server_secret=os.getenv("SERVER_SECRET"),
        port=int(os.getenv("PORT", "5222")),
        debug=debug,
    )

    # Validate and warn about missing API keys
    _validate_config(config)

    return config


def _validate_config(config: Config) -> None:
    """Validate configuration and log warnings for missing values.

    Args:
        config: Configuration object to validate.
    """
    if not config.has_eia_api_key:
        logger.warning(
            "EIA_API_KEY not configured. Market data tools will use fallback data. "
            "Get a free API key at: https://www.eia.gov/opendata/register.php"
        )

    if not config.has_news_api_key:
        logger.warning(
            "NEWS_API_KEY not configured. Risk assessment tools will use fallback data. "
            "Get a free API key at: https://newsapi.org/register"
        )

    if not config.has_server_secret:
        logger.info(
            "SERVER_SECRET not configured. Server will run without authentication. "
            "This is fine for local testing with stdio transport."
        )

    if config.debug:
        logger.debug("Debug mode enabled - verbose logging active")
        logger.debug(f"Configuration loaded: port={config.port}")
        logger.debug(
            f"API keys: EIA={config.has_eia_api_key}, News={config.has_news_api_key}"
        )

