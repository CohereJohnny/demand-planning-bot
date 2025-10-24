#!/usr/bin/env python3
"""Demand Planning MCP Server.

An MCP server for AI-assisted demand planning in the Oil & Gas supply chain.
Provides tools for market data, risk assessment, supply chain simulation,
inventory optimization, and financial calculations.
"""

import argparse
import logging
import sys

from north_mcp_python_sdk import NorthMCPServer

from src.demand_planning_bot.tools.financial import (
    get_calculate_revenue_impact_tool,
    get_calculate_roi_tool,
)
from src.demand_planning_bot.tools.inventory import (
    get_calculate_carrying_costs_tool,
    get_calculate_inventory_requirements_tool,
)
from src.demand_planning_bot.tools.market_data import get_market_prices_tool
from src.demand_planning_bot.tools.regulatory import (
    get_calculate_compliance_costs_tool,
    get_get_regulatory_updates_tool,
)
from src.demand_planning_bot.tools.risk_assessment import (
    get_geopolitical_risk_assessment_tool,
)
from src.demand_planning_bot.tools.supply_chain import (
    get_simulate_supply_disruption_tool,
)
from src.demand_planning_bot.utils.config import load_config

logger = logging.getLogger(__name__)


def create_server(config, host: str = "0.0.0.0") -> NorthMCPServer:
    """Create and configure the MCP server.

    Args:
        config: Configuration object with server settings.
        host: Host address to bind to (default: 0.0.0.0 for all interfaces).

    Returns:
        Configured NorthMCPServer instance.
    """
    # Initialize server with configuration
    server_kwargs = {
        "name": "Demand Planning Server",
        "host": host,
        "port": config.port,
    }

    # Add server secret ONLY if configured (for authenticated mode)
    # Do not include server_secret key at all when not configured to disable authentication
    if config.has_server_secret:
        server_kwargs["server_secret"] = config.server_secret
        logger.info("Server authentication enabled with server_secret")
    else:
        # Do NOT add server_secret key - omit it entirely to disable auth
        logger.info("Server running without authentication (local testing mode)")

    # Add debug mode if enabled
    if config.debug:
        server_kwargs["debug"] = True
        logger.debug("Server debug mode enabled")

    mcp = NorthMCPServer(**server_kwargs)

    # Register test tool
    @mcp.tool()
    def ping(message: str = "Hello") -> dict:
        """Test tool to verify server is working.

        Args:
            message: A message to echo back.

        Returns:
            A dictionary with the echoed message and server status.
        """
        logger.info(f"Ping tool called with message: {message}")
        return {
            "echo": message,
            "status": "Server is running",
            "tools_available": "Sprint 4: Market, risk, supply chain, inventory, financial, and regulatory tools available",
        }

    # Register market data tool
    get_market_prices = get_market_prices_tool(config)
    mcp.tool()(get_market_prices)

    # Register geopolitical risk assessment tool
    get_geopolitical_risk_assessment = get_geopolitical_risk_assessment_tool(config)
    mcp.tool()(get_geopolitical_risk_assessment)

    # Register supply chain simulation tool
    simulate_supply_disruption = get_simulate_supply_disruption_tool(config)
    mcp.tool()(simulate_supply_disruption)

    # Register inventory optimization tools
    calculate_inventory_requirements = get_calculate_inventory_requirements_tool(config)
    mcp.tool()(calculate_inventory_requirements)

    calculate_carrying_costs = get_calculate_carrying_costs_tool(config)
    mcp.tool()(calculate_carrying_costs)

    # Register financial analysis tools
    calculate_revenue_impact = get_calculate_revenue_impact_tool(config)
    mcp.tool()(calculate_revenue_impact)

    calculate_roi = get_calculate_roi_tool(config)
    mcp.tool()(calculate_roi)

    # Register regulatory compliance tools
    get_regulatory_updates = get_get_regulatory_updates_tool(config)
    mcp.tool()(get_regulatory_updates)

    calculate_compliance_costs = get_calculate_compliance_costs_tool(config)
    mcp.tool()(calculate_compliance_costs)

    logger.info("MCP server configured successfully")
    logger.info("Registered tools:")
    logger.info("  - ping (test tool)")
    logger.info("  - get_market_prices (EIA API - oil prices)")
    logger.info("  - get_geopolitical_risk_assessment (NewsAPI - risk analysis)")
    logger.info("  - simulate_supply_disruption (supply chain disruption modeling)")
    logger.info("  - calculate_inventory_requirements (safety stock calculations)")
    logger.info("  - calculate_carrying_costs (inventory cost analysis)")
    logger.info("  - calculate_revenue_impact (stockout revenue loss)")
    logger.info("  - calculate_roi (investment return on investment)")
    logger.info("  - get_regulatory_updates (IMO/regulatory compliance)")
    logger.info("  - calculate_compliance_costs (regulatory cost estimates)")

    return mcp


def parse_args():
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Demand Planning MCP Server for Oil & Gas Supply Chain"
    )

    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="streamable-http",
        help="Transport mode: stdio for local testing, streamable-http for North platform",
    )

    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host address to bind to (default: 0.0.0.0 for all interfaces)",
    )

    parser.add_argument(
        "--port",
        type=int,
        help="Port for HTTP transport (overrides PORT env var)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging (overrides DEBUG env var)",
    )

    return parser.parse_args()


def main():
    """Main entry point for the MCP server."""
    # Parse command-line arguments
    args = parse_args()

    # Load configuration
    config = load_config()

    # Override config with command-line arguments if provided
    if args.port:
        config.port = args.port
    if args.debug:
        config.debug = True
        logging.getLogger().setLevel(logging.DEBUG)

    # Log startup information
    logger.info("=" * 60)
    logger.info("Demand Planning MCP Server")
    logger.info("AI-Assisted Demand Planning for Oil & Gas Supply Chain")
    logger.info("=" * 60)
    logger.info(f"Transport mode: {args.transport}")
    logger.info(f"Host: {args.host}")
    logger.info(f"Port: {config.port}")
    logger.info(f"Debug mode: {config.debug}")

    try:
        # Create server
        mcp = create_server(config, host=args.host)

        # Start server with appropriate transport
        if args.transport == "stdio":
            logger.info("Starting server with stdio transport...")
            logger.info("Connect using MCP Inspector with stdio configuration")
            mcp.run(transport="stdio")
        else:
            logger.info(
                f"Starting server with Streamable HTTP transport on {args.host}:{config.port}..."
            )
            logger.info(
                f"Server will be available at: http://{args.host}:{config.port}/mcp"
            )
            logger.info("Connect using MCP Inspector with HTTP configuration")
            mcp.run(transport="streamable-http")

    except KeyboardInterrupt:
        logger.info("\nServer shutdown requested")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
