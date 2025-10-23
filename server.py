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

from src.demand_planning_bot.utils.config import load_config

logger = logging.getLogger(__name__)


def create_server(config) -> NorthMCPServer:
    """Create and configure the MCP server.

    Args:
        config: Configuration object with server settings.

    Returns:
        Configured NorthMCPServer instance.
    """
    # Initialize server with configuration
    server_kwargs = {
        "name": "Demand Planning Server",
        "port": config.port,
    }

    # Add server secret if configured (for authenticated mode)
    if config.has_server_secret:
        server_kwargs["server_secret"] = config.server_secret
        logger.info("Server authentication enabled with server_secret")
    else:
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
            "tools_available": "Basic foundation ready for Sprint 1",
        }

    logger.info("MCP server configured successfully")
    logger.info("Test tool 'ping' registered")

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
    logger.info(f"Port: {config.port}")
    logger.info(f"Debug mode: {config.debug}")

    try:
        # Create server
        mcp = create_server(config)

        # Start server with appropriate transport
        if args.transport == "stdio":
            logger.info("Starting server with stdio transport...")
            logger.info("Connect using MCP Inspector with stdio configuration")
            mcp.run(transport="stdio")
        else:
            logger.info(
                f"Starting server with Streamable HTTP transport on port {config.port}..."
            )
            logger.info(
                f"Server will be available at: http://localhost:{config.port}/mcp"
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
