"""MCP client wrapper for connecting to and executing tools on the MCP server.

This module provides utilities to:
- Connect to MCP servers via stdio or HTTP transports
- Discover available tools from the server
- Execute tool calls with parameters
- Handle connection errors gracefully
"""

import asyncio
import json
import logging
from contextlib import asynccontextmanager
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

logger = logging.getLogger(__name__)


class MCPClient:
    """Client for connecting to and interacting with an MCP server."""

    def __init__(self, transport: str = "stdio", host: str = "localhost", port: int = 8000):
        """Initialize the MCP client.

        Args:
            transport: Transport mode - "stdio" or "http"
            host: Host for HTTP transport (default: "localhost")
            port: Port for HTTP transport (default: 8000)
        """
        self.transport = transport
        self.host = host
        self.port = port
        self.session: ClientSession | None = None
        self.tools: list[dict[str, Any]] = []

        logger.info(f"MCP Client initialized with transport={transport}")

    @asynccontextmanager
    async def connect_stdio(self, server_script: str = "server.py"):
        """Connect to MCP server via stdio transport.

        Args:
            server_script: Path to the server script to run

        Yields:
            ClientSession for interacting with the server
        """
        server_params = StdioServerParameters(
            command="python",
            args=[server_script, "--transport", "stdio"],
            env=None,
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                logger.info("Connected to MCP server via stdio")

                self.session = session
                yield session

    @asynccontextmanager
    async def connect_http(self, server_secret: str | None = None):
        """Connect to MCP server via HTTP transport.

        Args:
            server_secret: Optional authentication secret for the server

        Yields:
            ClientSession for interacting with the server
        """
        url = f"http://{self.host}:{self.port}/mcp"
        headers = {}
        
        # Add authentication header if server secret is provided
        # Try both Authorization Bearer and X-Server-Secret formats
        if server_secret:
            headers["Authorization"] = f"Bearer {server_secret}"
            headers["X-Server-Secret"] = server_secret
            logger.info(f"Connecting to MCP server at {url} with authentication")
        else:
            logger.info(f"Connecting to MCP server at {url} without authentication")

        async with sse_client(url, headers=headers) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                logger.info(f"Connected to MCP server via HTTP at {url}")

                self.session = session
                yield session

    async def discover_tools(self) -> list[dict[str, Any]]:
        """Discover available tools from the MCP server.

        Returns:
            List of tool definitions with name, description, and inputSchema

        Raises:
            RuntimeError: If not connected to a server
        """
        if not self.session:
            raise RuntimeError("Not connected to MCP server. Call connect() first.")

        try:
            # List available tools
            tools_result = await self.session.list_tools()
            self.tools = [
                {
                    "name": tool.name,
                    "description": tool.description or "",
                    "inputSchema": tool.inputSchema if hasattr(tool, "inputSchema") else {},
                }
                for tool in tools_result.tools
            ]

            logger.info(f"Discovered {len(self.tools)} tools from MCP server")
            for tool in self.tools:
                logger.debug(f"  - {tool['name']}: {tool['description']}")

            return self.tools

        except Exception as e:
            logger.error(f"Failed to discover tools: {e}")
            raise

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Execute a tool call on the MCP server.

        Args:
            tool_name: Name of the tool to call
            arguments: Dictionary of arguments to pass to the tool

        Returns:
            Tool result from the server

        Raises:
            RuntimeError: If not connected to a server
            ValueError: If tool not found or execution fails
        """
        if not self.session:
            raise RuntimeError("Not connected to MCP server. Call connect() first.")

        try:
            logger.info(f"Calling tool '{tool_name}' with arguments: {arguments}")

            # Call the tool
            result = await self.session.call_tool(tool_name, arguments=arguments)

            logger.debug(f"Tool '{tool_name}' returned: {result}")
            return result

        except Exception as e:
            logger.error(f"Tool call '{tool_name}' failed: {e}")
            raise ValueError(f"Tool call failed: {e}") from e

    def format_tool_result(self, result: Any) -> list[dict[str, Any]]:
        """Format MCP tool result for Cohere's expected format.

        Cohere expects tool results as a list of document objects with:
        - type: "document"
        - document: {data: <json_string>, id: <optional_id>}

        Args:
            result: Raw MCP tool result

        Returns:
            List of formatted document objects
        """
        try:
            # Convert result to JSON string
            if hasattr(result, "content"):
                # MCP result has content field
                content_list = []
                for item in result.content:
                    if hasattr(item, "text"):
                        # Text content - parse as JSON if possible
                        try:
                            data = json.loads(item.text)
                        except json.JSONDecodeError:
                            data = {"text": item.text}
                    else:
                        data = {"raw": str(item)}

                    content_list.append({"type": "document", "document": {"data": json.dumps(data)}})

                return content_list
            else:
                # Fallback: wrap entire result
                data = json.dumps(result) if not isinstance(result, str) else result
                return [{"type": "document", "document": {"data": data}}]

        except Exception as e:
            logger.warning(f"Failed to format tool result: {e}, returning as-is")
            return [{"type": "document", "document": {"data": json.dumps({"error": str(result)})}}]

    async def close(self):
        """Close the connection to the MCP server."""
        if self.session:
            logger.info("Closing MCP client connection")
            self.session = None


async def test_connection():
    """Test function to verify MCP client connection."""
    client = MCPClient(transport="stdio")

    try:
        async with client.connect_stdio():
            # Discover tools
            tools = await client.discover_tools()
            print(f"\nDiscovered {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")

            # Test ping tool
            if any(t["name"] == "ping" for t in tools):
                result = await client.call_tool("ping", {"message": "Hello from MCP client!"})
                print(f"\nPing result: {result}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Run test
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_connection())

