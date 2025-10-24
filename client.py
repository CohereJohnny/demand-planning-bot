#!/usr/bin/env python3
"""Interactive MCP Client with Cohere Command A integration.

This client connects to the Demand Planning MCP server and enables
interactive testing of tools using Cohere's Command A model.
"""

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.demand_planning_bot.client.cohere_client import CohereToolUseClient
from src.demand_planning_bot.client.utils.mcp_client import MCPClient

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Interactive MCP Client with Cohere Command A",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Connect via stdio transport (default)
  python client.py

  # Connect via HTTP transport to a remote server
  python client.py --transport streamable-http --host 170.9.241.171 --port 5222

  # Connect via HTTP transport to localhost
  python client.py --transport streamable-http --port 8000

  # Use a different Cohere model (if needed)
  python client.py --model command-a-reasoning-08-2025

  # Enable debug logging
  python client.py --debug
        """,
    )

    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport mode for MCP server connection (default: stdio)",
    )

    parser.add_argument(
        "--host",
        default="localhost",
        help="Host for HTTP transport (default: localhost)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for HTTP transport (default: 8000)",
    )

    parser.add_argument(
        "--model",
        default="command-a-reasoning-08-2025",
        help="Cohere model to use (default: command-a-reasoning-08-2025)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    parser.add_argument(
        "--server-script",
        default="server.py",
        help="Path to MCP server script (default: server.py)",
    )

    return parser.parse_args()


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 70)
    print("  Demand Planning MCP Client")
    print("  Powered by Cohere Command A")
    print("=" * 70)
    print("\nCommands:")
    print("  - Type your question to interact with the demand planning tools")
    print("  - 'reset' - Clear conversation history")
    print("  - 'stats' - Show conversation statistics")
    print("  - 'exit' or 'quit' - Exit the client")
    print("=" * 70 + "\n")


def print_tool_calls(tool_calls: list):
    """Pretty print tool calls."""
    print("\n🔧 Tool Calls:")
    for i, tc in enumerate(tool_calls, 1):
        args = tc.function.arguments if hasattr(tc, "function") else "{}"
        print(f"  {i}. {tc.function.name}({args})")


def print_response(result: dict):
    """Pretty print the response with citations."""
    print("\n💬 Response:")
    print(f"  {result['text']}")

    if result.get("citations"):
        print(f"\n📎 Citations ({len(result['citations'])}):")
        for i, citation in enumerate(result["citations"], 1):
            print(f"  {i}. \"{citation['text']}\" (sources: {len(citation['sources'])})")

    print(f"\n📊 Metadata:")
    print(f"  - Tool calls: {result.get('tool_calls_made', 0)}")
    print(f"  - Conversation turns: {result.get('conversation_turns', 0)}")


def print_stats(stats: dict):
    """Print conversation statistics."""
    print("\n📊 Conversation Statistics:")
    print(f"  - Total messages: {stats['total_messages']}")
    print(f"  - Turns: {stats['turn_count']}")
    print(f"  - User messages: {stats['user_messages']}")
    print(f"  - Assistant messages: {stats['assistant_messages']}")
    print(f"  - Tool messages: {stats['tool_messages']}")
    print(f"  - Total tool calls: {stats['total_tool_calls']}")


async def main():
    """Main entry point for the interactive client."""
    args = parse_args()

    # Configure logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    # Check for Cohere API key
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        logger.error("COHERE_API_KEY not found in environment variables")
        print("\n❌ Error: COHERE_API_KEY not set")
        print("Please set your Cohere API key:")
        print("  export COHERE_API_KEY=your_api_key_here")
        print("Or add it to your .env file")
        sys.exit(1)

    logger.info(f"Starting MCP client with transport={args.transport}, model={args.model}")

    # Initialize MCP client
    mcp_client = MCPClient(transport=args.transport, host=args.host, port=args.port)

    try:
        # Connect to MCP server based on transport mode
        if args.transport == "stdio":
            context = mcp_client.connect_stdio(server_script=args.server_script)
            logger.info("Connecting to MCP server via stdio")
        else:  # streamable-http
            context = mcp_client.connect_http()
            logger.info(f"Connecting to MCP server via HTTP at {args.host}:{args.port}")

        async with context:
            logger.info("Connected to MCP server successfully")

            # Initialize Cohere client
            cohere_client = CohereToolUseClient(
                api_key=cohere_api_key, mcp_client=mcp_client, model=args.model
            )

            # Discover and convert tools
            print("\n🔍 Discovering tools from MCP server...")
            tools = await cohere_client.initialize_tools()
            print(f"✅ Discovered {len(tools)} tools:")
            for tool in tools:
                tool_name = tool["function"]["name"]
                tool_desc = tool["function"]["description"]
                print(f"  - {tool_name}: {tool_desc[:60]}...")

            # Print banner
            print_banner()

            # Interactive loop
            while True:
                try:
                    # Get user input
                    user_input = input("\nYou: ").strip()

                    if not user_input:
                        continue

                    # Handle commands
                    if user_input.lower() in ["exit", "quit"]:
                        print("\n👋 Goodbye!")
                        break

                    elif user_input.lower() == "reset":
                        cohere_client.reset_conversation()
                        print("\n🔄 Conversation reset")
                        continue

                    elif user_input.lower() == "stats":
                        stats = cohere_client.get_conversation_summary()
                        print_stats(stats)
                        continue

                    elif user_input.lower() == "debug":
                        cohere_client.display_conversation()
                        continue

                    # Process message with Cohere
                    print("\n⏳ Processing...")
                    result = await cohere_client.process_message(user_input)

                    # Display response
                    print_response(result)

                except KeyboardInterrupt:
                    print("\n\n👋 Interrupted. Type 'exit' to quit.")
                    continue

                except Exception as e:
                    logger.error(f"Error processing message: {e}", exc_info=True)
                    print(f"\n❌ Error: {e}")
                    print("Please try again or type 'exit' to quit.")

    except FileNotFoundError:
        logger.error(f"Server script not found: {args.server_script}")
        print(f"\n❌ Error: Could not find MCP server at '{args.server_script}'")
        print("Please ensure the server.py file exists in the current directory.")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Failed to start client: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)

