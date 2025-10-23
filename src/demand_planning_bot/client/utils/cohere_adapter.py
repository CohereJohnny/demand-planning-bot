"""Adapter to convert MCP tool schemas to Cohere tool format.

This module provides utilities to convert MCP (Model Context Protocol) tool
schemas to Cohere's JSON Schema format for tool use (function calling).
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def mcp_tool_to_cohere_schema(mcp_tool: dict[str, Any]) -> dict[str, Any]:
    """Convert a single MCP tool schema to Cohere tool schema format.

    Args:
        mcp_tool: MCP tool definition with name, description, and inputSchema.

    Returns:
        Cohere-compatible tool schema with type="function".

    Example:
        >>> mcp_tool = {
        ...     "name": "get_weather",
        ...     "description": "Get weather for a location",
        ...     "inputSchema": {
        ...         "type": "object",
        ...         "properties": {
        ...             "location": {"type": "string", "description": "City name"}
        ...         },
        ...         "required": ["location"]
        ...     }
        ... }
        >>> cohere_tool = mcp_tool_to_cohere_schema(mcp_tool)
        >>> cohere_tool["type"]
        'function'
    """
    try:
        # Extract MCP tool properties
        name = mcp_tool.get("name", "")
        description = mcp_tool.get("description", "")
        input_schema = mcp_tool.get("inputSchema", {})

        # Convert to Cohere format
        cohere_schema = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": input_schema.get("properties", {}),
                    "required": input_schema.get("required", []),
                },
            },
        }

        logger.debug(f"Converted MCP tool '{name}' to Cohere schema")
        return cohere_schema

    except Exception as e:
        logger.error(f"Failed to convert MCP tool schema: {e}")
        raise ValueError(f"Invalid MCP tool schema: {e}") from e


def mcp_tools_to_cohere_tools(mcp_tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert a list of MCP tool schemas to Cohere tool schemas.

    Args:
        mcp_tools: List of MCP tool definitions.

    Returns:
        List of Cohere-compatible tool schemas.

    Example:
        >>> mcp_tools = [
        ...     {"name": "tool1", "description": "First tool", "inputSchema": {...}},
        ...     {"name": "tool2", "description": "Second tool", "inputSchema": {...}}
        ... ]
        >>> cohere_tools = mcp_tools_to_cohere_tools(mcp_tools)
        >>> len(cohere_tools)
        2
    """
    cohere_tools = []

    for mcp_tool in mcp_tools:
        try:
            cohere_tool = mcp_tool_to_cohere_schema(mcp_tool)
            cohere_tools.append(cohere_tool)
        except ValueError as e:
            logger.warning(f"Skipping invalid MCP tool: {e}")
            continue

    logger.info(
        f"Converted {len(cohere_tools)} MCP tools to Cohere format "
        f"({len(mcp_tools) - len(cohere_tools)} skipped)"
    )

    return cohere_tools

