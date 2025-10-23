"""Conversation state management for multi-turn interactions with Cohere.

This module manages the conversation history and tool call state required for
Cohere's tool use workflow.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ConversationManager:
    """Manages conversation state for Cohere tool use workflow.

    Tracks:
    - Message history (user, assistant, tool messages)
    - Tool call IDs for matching results
    - Conversation turns
    """

    def __init__(self):
        """Initialize the conversation manager."""
        self.messages: list[dict[str, Any]] = []
        self.turn_count = 0

        logger.debug("ConversationManager initialized")

    def add_user_message(self, content: str):
        """Add a user message to the conversation.

        Args:
            content: User's message text
        """
        self.messages.append({"role": "user", "content": content})
        self.turn_count += 1

        logger.info(f"Added user message (turn {self.turn_count})")
        logger.debug(f"User: {content[:100]}...")

    def add_assistant_message(self, response: Any):
        """Add an assistant message with optional tool calls to the conversation.

        Args:
            response: Cohere response object containing message content, tool_plan, and tool_calls
        """
        message: dict[str, Any] = {"role": "assistant"}

        # Add text content if present
        if hasattr(response, "message") and hasattr(response.message, "content"):
            if response.message.content and len(response.message.content) > 0:
                content_item = response.message.content[0]
                if hasattr(content_item, "text"):
                    message["content"] = content_item.text

        # Add tool_plan if present
        if hasattr(response, "message") and hasattr(response.message, "tool_plan"):
            if response.message.tool_plan:
                message["tool_plan"] = response.message.tool_plan
                logger.debug(f"Tool plan: {response.message.tool_plan}")

        # Add tool_calls if present
        if hasattr(response, "message") and hasattr(response.message, "tool_calls"):
            if response.message.tool_calls:
                message["tool_calls"] = response.message.tool_calls
                logger.debug(f"Tool calls: {len(response.message.tool_calls)}")

        self.messages.append(message)
        logger.info(f"Added assistant message with {len(message.get('tool_calls', []))} tool calls")

    def add_tool_results(self, tool_call_id: str, content: list[dict[str, Any]]):
        """Add tool results to the conversation.

        Args:
            tool_call_id: ID of the tool call being responded to
            content: List of document objects with tool results
        """
        self.messages.append({"role": "tool", "tool_call_id": tool_call_id, "content": content})

        logger.info(f"Added tool results for call ID: {tool_call_id}")
        logger.debug(f"Tool result content: {content}")

    def get_messages(self) -> list[dict[str, Any]]:
        """Get the current conversation messages.

        Returns:
            List of message dictionaries
        """
        return self.messages

    def reset(self):
        """Reset the conversation state."""
        self.messages = []
        self.turn_count = 0

        logger.info("Conversation reset")

    def get_conversation_summary(self) -> dict[str, Any]:
        """Get a summary of the conversation state.

        Returns:
            Dictionary with conversation statistics
        """
        user_messages = sum(1 for m in self.messages if m["role"] == "user")
        assistant_messages = sum(1 for m in self.messages if m["role"] == "assistant")
        tool_messages = sum(1 for m in self.messages if m["role"] == "tool")
        total_tool_calls = sum(
            len(m.get("tool_calls", [])) for m in self.messages if m["role"] == "assistant"
        )

        return {
            "total_messages": len(self.messages),
            "turns": self.turn_count,
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "tool_messages": tool_messages,
            "total_tool_calls": total_tool_calls,
        }

    def display_conversation(self):
        """Display the conversation history (for debugging)."""
        print("\n" + "=" * 60)
        print("CONVERSATION HISTORY")
        print("=" * 60)

        for i, message in enumerate(self.messages, 1):
            role = message["role"].upper()
            print(f"\n[{i}] {role}:")

            if role == "USER":
                print(f"  {message['content']}")

            elif role == "ASSISTANT":
                if "tool_plan" in message:
                    print(f"  Tool Plan: {message['tool_plan']}")
                if "tool_calls" in message:
                    print(f"  Tool Calls: {len(message['tool_calls'])}")
                    for tc in message['tool_calls']:
                        print(f"    - {tc.function.name}({tc.function.arguments})")
                if "content" in message:
                    print(f"  Response: {message['content'][:100]}...")

            elif role == "TOOL":
                print(f"  Tool Call ID: {message['tool_call_id']}")
                print(f"  Results: {len(message['content'])} documents")

        print("\n" + "=" * 60)
        summary = self.get_conversation_summary()
        print(f"Summary: {summary}")
        print("=" * 60 + "\n")

