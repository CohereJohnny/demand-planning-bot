"""Cohere client implementation for MCP tool use workflow.

This module implements Cohere's 4-step tool use pattern:
1. User message → append to conversation
2. Generate tool calls → Cohere decides which tools to call
3. Execute tools → call MCP server and collect results
4. Generate response → Cohere synthesizes final answer with citations
"""

import json
import logging
from typing import Any

import cohere

from .conversation import ConversationManager
from .utils.cohere_adapter import mcp_tools_to_cohere_tools
from .utils.mcp_client import MCPClient

logger = logging.getLogger(__name__)


class CohereToolUseClient:
    """Client for Cohere Command A model with MCP tool use integration."""

    def __init__(
        self,
        api_key: str,
        mcp_client: MCPClient,
        model: str = "command-a-03-2025",
        max_iterations: int = 5,
    ):
        """Initialize the Cohere tool use client.

        Args:
            api_key: Cohere API key
            mcp_client: Connected MCP client instance
            model: Cohere model to use (default: command-a-03-2025)
            max_iterations: Maximum tool use iterations (default: 5)
        """
        self.cohere = cohere.ClientV2(api_key=api_key)
        self.mcp_client = mcp_client
        self.model = model
        self.max_iterations = max_iterations
        self.conversation = ConversationManager()
        self.cohere_tools: list[dict[str, Any]] = []

        logger.info(f"CohereToolUseClient initialized with model={model}")

    async def initialize_tools(self):
        """Discover tools from MCP server and convert to Cohere format."""
        try:
            # Discover MCP tools
            mcp_tools = await self.mcp_client.discover_tools()
            logger.info(f"Discovered {len(mcp_tools)} MCP tools")

            # Convert to Cohere format
            self.cohere_tools = mcp_tools_to_cohere_tools(mcp_tools)
            logger.info(f"Converted {len(self.cohere_tools)} tools to Cohere format")

            return self.cohere_tools

        except Exception as e:
            logger.error(f"Failed to initialize tools: {e}")
            raise

    async def process_message(self, user_message: str) -> dict[str, Any]:
        """Process a user message with the 4-step tool use workflow.

        This implements Cohere's tool use pattern:
        1. Add user message to conversation
        2. Call Cohere to get tool calls (may repeat multiple times)
        3. Execute tools via MCP
        4. Call Cohere to generate final response

        Args:
            user_message: User's input message

        Returns:
            Dictionary with response text, citations, and metadata
        """
        # Step 1: Add user message to conversation
        self.conversation.add_user_message(user_message)
        logger.info(f"Processing user message: {user_message[:100]}...")

        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            logger.info(f"Tool use iteration {iteration}/{self.max_iterations}")

            try:
                # Step 2: Generate tool calls with Cohere
                response = self.cohere.chat(
                    model=self.model,
                    messages=self.conversation.get_messages(),
                    tools=self.cohere_tools,
                )

                logger.debug(f"Cohere response: {response}")

                # Check if Cohere wants to call tools
                if hasattr(response, "message") and hasattr(response.message, "tool_calls"):
                    if response.message.tool_calls and len(response.message.tool_calls) > 0:
                        # Add assistant message with tool calls
                        self.conversation.add_assistant_message(response)

                        # Step 3: Execute tools via MCP
                        await self._execute_tool_calls(response.message.tool_calls)

                        # Continue loop to get next response
                        continue

                # No tool calls - generate final response (Step 4)
                self.conversation.add_assistant_message(response)

                # Extract response details
                result = self._extract_response(response)
                logger.info("Generated final response")

                return result

            except Exception as e:
                logger.error(f"Error in iteration {iteration}: {e}")
                raise

        # Max iterations reached
        logger.warning(f"Max iterations ({self.max_iterations}) reached")
        return {
            "text": "I apologize, but I've reached the maximum number of tool calls. Please try rephrasing your question.",
            "citations": [],
            "iterations": iteration,
        }

    async def _execute_tool_calls(self, tool_calls: list) -> None:
        """Execute tool calls via MCP server.

        Args:
            tool_calls: List of tool call objects from Cohere
        """
        logger.info(f"Executing {len(tool_calls)} tool calls")

        for tool_call in tool_calls:
            try:
                # Extract tool call details
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                tool_call_id = tool_call.id

                logger.info(f"Calling tool: {tool_name} with args: {arguments}")

                # Execute tool via MCP
                result = await self.mcp_client.call_tool(tool_name, arguments)

                # Format result for Cohere
                formatted_result = self.mcp_client.format_tool_result(result)

                # Add tool results to conversation
                self.conversation.add_tool_results(tool_call_id, formatted_result)

                logger.debug(f"Tool {tool_name} executed successfully")

            except Exception as e:
                logger.error(f"Tool call failed: {e}")
                # Add error as tool result
                error_result = [
                    {
                        "type": "document",
                        "document": {"data": json.dumps({"error": str(e)})},
                    }
                ]
                self.conversation.add_tool_results(tool_call.id, error_result)

    def _extract_response(self, response: Any) -> dict[str, Any]:
        """Extract response text and citations from Cohere response.

        Args:
            response: Cohere chat response object

        Returns:
            Dictionary with text, citations, and metadata
        """
        result = {
            "text": "",
            "citations": [],
            "tool_calls_made": 0,
            "conversation_turns": self.conversation.turn_count,
        }

        # Extract text content
        if hasattr(response, "message") and hasattr(response.message, "content"):
            if response.message.content and len(response.message.content) > 0:
                content_item = response.message.content[0]
                if hasattr(content_item, "text"):
                    result["text"] = content_item.text

        # Extract citations
        if hasattr(response, "message") and hasattr(response.message, "citations"):
            if response.message.citations:
                result["citations"] = [
                    {
                        "text": citation.text if hasattr(citation, "text") else "",
                        "start": citation.start if hasattr(citation, "start") else 0,
                        "end": citation.end if hasattr(citation, "end") else 0,
                        "sources": (
                            [
                                {
                                    "type": source.type if hasattr(source, "type") else "unknown",
                                    "id": source.id if hasattr(source, "id") else "",
                                }
                                for source in citation.sources
                            ]
                            if hasattr(citation, "sources")
                            else []
                        ),
                    }
                    for citation in response.message.citations
                ]

        # Count tool calls made
        summary = self.conversation.get_conversation_summary()
        result["tool_calls_made"] = summary["total_tool_calls"]

        return result

    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation.reset()
        logger.info("Conversation reset")

    def get_conversation_summary(self) -> dict[str, Any]:
        """Get conversation statistics.

        Returns:
            Dictionary with conversation metrics
        """
        return self.conversation.get_conversation_summary()

    def display_conversation(self):
        """Display the full conversation history (for debugging)."""
        self.conversation.display_conversation()

