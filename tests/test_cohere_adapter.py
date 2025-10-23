"""Unit tests for MCP to Cohere schema conversion."""

import pytest
from src.demand_planning_bot.client.utils.cohere_adapter import (
    mcp_tool_to_cohere_schema,
    mcp_tools_to_cohere_tools,
)


class TestMCPToolToCohereSchema:
    """Test individual MCP tool to Cohere schema conversion."""

    def test_basic_tool_conversion(self):
        """Test conversion of a simple tool with basic parameters."""
        mcp_tool = {
            "name": "test_tool",
            "description": "A test tool for unit testing",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "First parameter"
                    },
                    "param2": {
                        "type": "integer",
                        "description": "Second parameter"
                    }
                },
                "required": ["param1"]
            }
        }

        result = mcp_tool_to_cohere_schema(mcp_tool)

        assert result["type"] == "function"
        assert result["function"]["name"] == "test_tool"
        assert result["function"]["description"] == "A test tool for unit testing"
        assert result["function"]["parameters"]["type"] == "object"
        assert "param1" in result["function"]["parameters"]["properties"]
        assert "param2" in result["function"]["parameters"]["properties"]
        assert result["function"]["parameters"]["required"] == ["param1"]

    def test_tool_with_no_required_params(self):
        """Test conversion of a tool with no required parameters."""
        mcp_tool = {
            "name": "optional_tool",
            "description": "Tool with all optional params",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "optional_param": {
                        "type": "string",
                        "description": "An optional parameter"
                    }
                },
                "required": []
            }
        }

        result = mcp_tool_to_cohere_schema(mcp_tool)

        assert result["function"]["parameters"]["required"] == []

    def test_tool_with_complex_types(self):
        """Test conversion of a tool with complex parameter types."""
        mcp_tool = {
            "name": "complex_tool",
            "description": "Tool with complex types",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "string_array": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Array of strings"
                    },
                    "nested_object": {
                        "type": "object",
                        "properties": {
                            "nested_field": {"type": "number"}
                        },
                        "description": "Nested object"
                    },
                    "enum_field": {
                        "type": "string",
                        "enum": ["option1", "option2", "option3"],
                        "description": "Enum field"
                    }
                },
                "required": ["string_array"]
            }
        }

        result = mcp_tool_to_cohere_schema(mcp_tool)

        props = result["function"]["parameters"]["properties"]
        assert "string_array" in props
        assert props["string_array"]["type"] == "array"
        assert "nested_object" in props
        assert "nested_field" in props["nested_object"]["properties"]
        assert "enum_field" in props
        assert props["enum_field"]["enum"] == ["option1", "option2", "option3"]

    def test_tool_with_missing_input_schema(self):
        """Test conversion of a tool with missing inputSchema."""
        mcp_tool = {
            "name": "no_schema_tool",
            "description": "Tool without input schema",
            "inputSchema": {}
        }

        result = mcp_tool_to_cohere_schema(mcp_tool)

        assert result["type"] == "function"
        assert result["function"]["name"] == "no_schema_tool"
        assert result["function"]["parameters"]["properties"] == {}
        assert result["function"]["parameters"]["required"] == []

    def test_tool_with_missing_fields(self):
        """Test graceful handling of missing fields."""
        mcp_tool = {
            "name": "minimal_tool"
            # Missing description and inputSchema
        }

        result = mcp_tool_to_cohere_schema(mcp_tool)

        assert result["type"] == "function"
        assert result["function"]["name"] == "minimal_tool"
        assert result["function"]["description"] == ""
        assert result["function"]["parameters"]["properties"] == {}

    def test_real_world_ping_tool(self):
        """Test conversion of the actual ping tool from the server."""
        mcp_tool = {
            "name": "ping",
            "description": "Test tool to verify server is working.\n\nArgs:\n    message: A message to echo back.\n\nReturns:\n    A dictionary with the echoed message and server status.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to echo back"
                    }
                },
                "required": ["message"]
            }
        }

        result = mcp_tool_to_cohere_schema(mcp_tool)

        assert result["type"] == "function"
        assert result["function"]["name"] == "ping"
        assert "Test tool to verify server" in result["function"]["description"]
        assert "message" in result["function"]["parameters"]["properties"]
        assert result["function"]["parameters"]["required"] == ["message"]

    def test_real_world_market_prices_tool(self):
        """Test conversion of the get_market_prices tool."""
        mcp_tool = {
            "name": "get_market_prices",
            "description": "Get current or recent oil prices from EIA API.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "enum": ["brent", "wti"],
                        "description": "Oil product type"
                    },
                    "timeframe": {
                        "type": "string",
                        "enum": ["current", "recent"],
                        "description": "Time period"
                    }
                },
                "required": ["product"]
            }
        }

        result = mcp_tool_to_cohere_schema(mcp_tool)

        assert result["function"]["name"] == "get_market_prices"
        props = result["function"]["parameters"]["properties"]
        assert props["product"]["enum"] == ["brent", "wti"]
        assert props["timeframe"]["enum"] == ["current", "recent"]
        assert result["function"]["parameters"]["required"] == ["product"]


class TestMCPToolsToCohereTools:
    """Test batch conversion of multiple MCP tools."""

    def test_empty_list(self):
        """Test conversion of an empty tool list."""
        result = mcp_tools_to_cohere_tools([])
        assert result == []

    def test_single_tool(self):
        """Test conversion of a single tool."""
        mcp_tools = [{
            "name": "single_tool",
            "description": "A single tool",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }]

        result = mcp_tools_to_cohere_tools(mcp_tools)

        assert len(result) == 1
        assert result[0]["function"]["name"] == "single_tool"

    def test_multiple_tools(self):
        """Test conversion of multiple tools."""
        mcp_tools = [
            {
                "name": "tool1",
                "description": "First tool",
                "inputSchema": {
                    "type": "object",
                    "properties": {"param1": {"type": "string"}},
                    "required": []
                }
            },
            {
                "name": "tool2",
                "description": "Second tool",
                "inputSchema": {
                    "type": "object",
                    "properties": {"param2": {"type": "integer"}},
                    "required": ["param2"]
                }
            },
            {
                "name": "tool3",
                "description": "Third tool",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]

        result = mcp_tools_to_cohere_tools(mcp_tools)

        assert len(result) == 3
        assert result[0]["function"]["name"] == "tool1"
        assert result[1]["function"]["name"] == "tool2"
        assert result[2]["function"]["name"] == "tool3"
        assert result[1]["function"]["parameters"]["required"] == ["param2"]

    def test_tool_with_missing_name(self):
        """Test that tools with missing names get empty string name."""
        mcp_tools = [
            {
                "name": "valid_tool",
                "description": "Valid tool",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                # Missing name - gets empty string
                "description": "Tool without name",
                "inputSchema": {}
            },
            {
                "name": "another_valid_tool",
                "description": "Another valid tool",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]

        result = mcp_tools_to_cohere_tools(mcp_tools)

        # All tools are converted, missing name becomes empty string
        assert len(result) == 3
        assert result[0]["function"]["name"] == "valid_tool"
        assert result[1]["function"]["name"] == ""  # Missing name becomes empty string
        assert result[2]["function"]["name"] == "another_valid_tool"

    def test_all_ten_server_tools(self):
        """Test conversion of all 10 tools from the actual MCP server."""
        tool_names = [
            "ping",
            "get_market_prices",
            "get_geopolitical_risk_assessment",
            "simulate_supply_disruption",
            "calculate_inventory_requirements",
            "calculate_carrying_costs",
            "calculate_revenue_impact",
            "calculate_roi",
            "get_regulatory_updates",
            "calculate_compliance_costs"
        ]

        # Simplified tool definitions for testing
        mcp_tools = [
            {
                "name": name,
                "description": f"Test description for {name}",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "test_param": {"type": "string"}
                    },
                    "required": []
                }
            }
            for name in tool_names
        ]

        result = mcp_tools_to_cohere_tools(mcp_tools)

        assert len(result) == 10
        result_names = [tool["function"]["name"] for tool in result]
        assert result_names == tool_names


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

