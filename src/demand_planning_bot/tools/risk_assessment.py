"""Geopolitical risk assessment tools using NewsAPI.

Provides MCP tools for assessing geopolitical risks affecting oil & gas
supply chains by analyzing recent news and calculating risk probabilities.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Literal, Optional

from demand_planning_bot.utils.api_client import APIClient, APIError, RateLimitError
from demand_planning_bot.utils.config import Config

logger = logging.getLogger(__name__)

# NewsAPI base URL
NEWS_API_BASE = "https://newsapi.org/v2"

# Risk-related keywords for sentiment analysis
THREAT_KEYWORDS = {
    "high": ["war", "conflict", "attack", "closure", "sanctions", "blockade", "crisis"],
    "medium": ["tension", "dispute", "threat", "concern", "warning", "risk"],
    "low": ["negotiation", "talks", "agreement", "cooperation", "stability"],
}

# Regional query mappings
REGION_QUERIES = {
    "strait of hormuz": "Strait of Hormuz OR Persian Gulf OR Iran oil",
    "middle east": "Middle East oil OR OPEC OR Saudi Arabia",
    "russia ukraine": "Russia Ukraine oil OR gas OR energy",
    "venezuela": "Venezuela oil OR PDVSA",
    "libya": "Libya oil OR NOC",
}


class NewsAPIClient:
    """Client for NewsAPI geopolitical news retrieval."""

    def __init__(self, api_key: Optional[str], config: Config):
        """Initialize the NewsAPI client.

        Args:
            api_key: NewsAPI key (optional, will use fallback if None).
            config: Configuration object.
        """
        self.api_key = api_key
        self.config = config
        self.client = APIClient(timeout=30.0, max_retries=3)

    def get_news(
        self,
        query: str,
        days_back: int = 7,
        language: str = "en",
        max_results: int = 10,
    ) -> Dict:
        """Get news articles from NewsAPI.

        Args:
            query: Search query string.
            days_back: Number of days to look back.
            language: Language code (default: "en").
            max_results: Maximum number of articles to return.

        Returns:
            Dictionary with news articles.

        Raises:
            APIError: If API call fails.
        """
        if not self.api_key:
            raise APIError("NewsAPI key not configured")

        # Calculate date range
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days_back)

        # Build API URL
        url = f"{NEWS_API_BASE}/everything"

        params = {
            "apiKey": self.api_key,
            "q": query,
            "from": from_date.strftime("%Y-%m-%d"),
            "to": to_date.strftime("%Y-%m-%d"),
            "language": language,
            "sortBy": "relevancy",
            "pageSize": max_results,
        }

        try:
            logger.debug(f"Fetching news for query: {query}")
            response = self.client.get(url, params=params)

            if "status" not in response or response["status"] != "ok":
                error_msg = response.get("message", "Unknown error")
                raise APIError(f"NewsAPI error: {error_msg}")

            return response

        except RateLimitError as e:
            logger.error(f"NewsAPI rate limit exceeded: {e}")
            raise
        except APIError as e:
            logger.error(f"NewsAPI error: {e}")
            raise


def calculate_risk_score(articles: List[Dict]) -> tuple[float, str, List[str]]:
    """Calculate risk score from news articles.

    Args:
        articles: List of news article dictionaries.

    Returns:
        Tuple of (risk_probability, risk_level, keywords_found).
    """
    if not articles:
        return 0.0, "low", []

    # Count threat keywords in titles and descriptions
    high_count = 0
    medium_count = 0
    low_count = 0
    keywords_found = set()

    for article in articles:
        text = f"{article.get('title', '')} {article.get('description', '')}".lower()

        for keyword in THREAT_KEYWORDS["high"]:
            if keyword in text:
                high_count += 1
                keywords_found.add(keyword)

        for keyword in THREAT_KEYWORDS["medium"]:
            if keyword in text:
                medium_count += 1
                keywords_found.add(keyword)

        for keyword in THREAT_KEYWORDS["low"]:
            if keyword in text:
                low_count += 1
                keywords_found.add(keyword)

    # Calculate risk probability (0-100%)
    # High threat keywords contribute more to the score
    total_articles = len(articles)
    risk_score = 0.0

    if total_articles > 0:
        high_ratio = high_count / total_articles
        medium_ratio = medium_count / total_articles

        # Weighted calculation
        risk_score = min(100, (high_ratio * 60 + medium_ratio * 30))

    # Determine risk level
    if risk_score >= 40:
        risk_level = "high"
    elif risk_score >= 20:
        risk_level = "medium"
    else:
        risk_level = "low"

    return risk_score, risk_level, list(keywords_found)


def get_fallback_risk_data(region: str) -> Dict:
    """Get fallback risk assessment when API is unavailable.

    Args:
        region: Geographic region or risk area.

    Returns:
        Dictionary with simulated risk assessment.
    """
    # Pre-defined risk scenarios based on common concerns
    fallback_scenarios = {
        "strait of hormuz": {
            "probability": 25.0,
            "impact": "25% probability of temporary closure due to escalating regional conflicts. "
            "Historical data suggests such an event would cause a 12-15% spike in Brent crude prices within 30 days.",
            "risk_level": "medium",
            "affected_routes": [
                "Persian Gulf shipping lanes",
                "Strait of Hormuz passage",
            ],
            "potential_impact": "12-15% price increase within 30 days",
        },
        "middle east": {
            "probability": 30.0,
            "impact": "Ongoing geopolitical tensions in the Middle East create moderate supply chain risks. "
            "OPEC production decisions and regional conflicts remain key factors.",
            "risk_level": "medium",
            "affected_routes": ["Multiple Middle East export terminals"],
            "potential_impact": "5-10% price volatility",
        },
        "default": {
            "probability": 15.0,
            "impact": "Standard geopolitical risk level for global oil markets. "
            "Normal fluctuations expected based on OPEC decisions and seasonal demand.",
            "risk_level": "low",
            "affected_routes": ["Global shipping routes"],
            "potential_impact": "3-5% price volatility",
        },
    }

    region_lower = region.lower()
    scenario = fallback_scenarios.get(region_lower, fallback_scenarios["default"])

    return {
        "region": region,
        "risk_probability": scenario["probability"],
        "risk_level": scenario["risk_level"],
        "impact_description": scenario["impact"],
        "affected_routes": scenario["affected_routes"],
        "potential_impact": scenario["potential_impact"],
        "assessment_date": datetime.now().strftime("%Y-%m-%d"),
        "data_source": "fallback",
        "confidence": "medium",
        "note": "Using pre-defined risk scenario - NewsAPI unavailable or not configured",
        "news_headlines": [
            f"Simulated news: {region} geopolitical assessment",
            "Historical risk patterns suggest moderate supply chain concerns",
        ],
    }


def get_geopolitical_risk_assessment_tool(
    config: Config,
) -> callable:
    """Create the get_geopolitical_risk_assessment MCP tool.

    Args:
        config: Configuration object with API keys.

    Returns:
        MCP tool function.
    """

    def get_geopolitical_risk_assessment(
        region: str = "Strait of Hormuz",
        timeframe_days: int = 7,
    ) -> Dict:
        """Assess geopolitical risks affecting oil supply chains.

        Analyzes recent news to identify and quantify geopolitical risks that could
        impact oil supply routes and pricing. Uses NewsAPI for real-time news analysis
        with keyword-based risk scoring. Falls back to pre-defined scenarios if API
        is unavailable.

        Args:
            region: Geographic region or chokepoint to assess (e.g., "Strait of Hormuz",
                   "Middle East", "Russia Ukraine"). Default: "Strait of Hormuz".
            timeframe_days: Number of days of recent news to analyze (default: 7).

        Returns:
            Dictionary with risk assessment including:
            - region: Region assessed
            - risk_probability: Probability score (0-100%)
            - risk_level: "low", "medium", or "high"
            - impact_description: Detailed impact analysis
            - news_headlines: Supporting news article titles
            - confidence: Data confidence level
            - data_source: "newsapi" or "fallback"
        """
        logger.info(
            f"get_geopolitical_risk_assessment called: region={region}, timeframe={timeframe_days}"
        )

        # Try to use NewsAPI if configured
        if config.has_news_api_key:
            try:
                client = NewsAPIClient(config.news_api_key, config)

                # Get appropriate query for region
                region_lower = region.lower()
                query = REGION_QUERIES.get(region_lower, f"{region} oil OR energy")

                # Fetch news
                response = client.get_news(
                    query=query, days_back=timeframe_days, max_results=20
                )

                articles = response.get("articles", [])

                if not articles:
                    logger.warning(f"No articles found for region: {region}")
                    # Fall through to fallback data
                else:
                    # Calculate risk score from articles
                    risk_score, risk_level, keywords = calculate_risk_score(articles)

                    # Extract headlines
                    headlines = [
                        article.get("title", "No title") for article in articles[:5]
                    ]

                    result = {
                        "region": region,
                        "risk_probability": risk_score,
                        "risk_level": risk_level,
                        "impact_description": f"Based on analysis of {len(articles)} recent news articles, "
                        f"the risk level is assessed as {risk_level}. "
                        f"Key threat indicators: {', '.join(keywords[:5]) if keywords else 'none detected'}.",
                        "news_headlines": headlines,
                        "articles_analyzed": len(articles),
                        "threat_keywords": keywords[:10],
                        "assessment_date": datetime.now().strftime("%Y-%m-%d"),
                        "timeframe_days": timeframe_days,
                        "data_source": "newsapi",
                        "confidence": "high",
                        "api_note": "Risk assessment based on NewsAPI real-time news analysis",
                    }

                    logger.info(
                        f"Risk assessment complete: {risk_level} risk ({risk_score:.1f}%)"
                    )
                    return result

            except (APIError, RateLimitError) as e:
                logger.warning(
                    f"Failed to fetch from NewsAPI, using fallback data: {e}"
                )
                # Fall through to fallback data

        # Use fallback data
        logger.info(f"Using fallback risk assessment for {region}")
        return get_fallback_risk_data(region)

    return get_geopolitical_risk_assessment
