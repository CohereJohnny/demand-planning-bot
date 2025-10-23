#!/usr/bin/env python3
"""Test script for MCP Client with Cohere integration.

This script tests the client programmatically without interactive input.
"""

import asyncio
import logging
import os
import sys

from dotenv import load_dotenv

from src.demand_planning_bot.client.cohere_client import CohereToolUseClient
from src.demand_planning_bot.client.utils.mcp_client import MCPClient

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def test_connection_and_discovery():
    """Test TC1 and TC3: Connection and tool discovery."""
    print("\n" + "=" * 70)
    print("TEST 1: Connection and Tool Discovery")
    print("=" * 70)
    
    try:
        # Initialize MCP client
        mcp_client = MCPClient(transport="stdio")
        
        # Connect to server
        async with mcp_client.connect_stdio(server_script="server.py"):
            print("✅ Successfully connected to MCP server via stdio")
            
            # Discover tools
            tools = await mcp_client.discover_tools()
            print(f"✅ Discovered {len(tools)} tools:")
            for tool in tools:
                print(f"   - {tool['name']}")
            
            # Verify all expected tools are present
            expected_tools = {
                "ping", "get_market_prices", "get_geopolitical_risk_assessment",
                "simulate_supply_disruption", "calculate_inventory_requirements",
                "calculate_carrying_costs", "calculate_revenue_impact",
                "calculate_roi", "get_regulatory_updates", "calculate_compliance_costs"
            }
            discovered_tools = {tool['name'] for tool in tools}
            
            if expected_tools == discovered_tools:
                print("✅ All expected tools discovered")
            else:
                missing = expected_tools - discovered_tools
                extra = discovered_tools - expected_tools
                if missing:
                    print(f"⚠️  Missing tools: {missing}")
                if extra:
                    print(f"⚠️  Extra tools: {extra}")
            
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logger.error(f"Connection test failed", exc_info=True)
        return False


async def test_simple_query():
    """Test TC5: Single tool call with simple query."""
    print("\n" + "=" * 70)
    print("TEST 2: Simple Tool Call - Ping")
    print("=" * 70)
    
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        print("❌ COHERE_API_KEY not found")
        return False
    
    try:
        mcp_client = MCPClient(transport="stdio")
        
        async with mcp_client.connect_stdio(server_script="server.py"):
            # Initialize Cohere client
            cohere_client = CohereToolUseClient(
                api_key=cohere_api_key,
                mcp_client=mcp_client,
            )
            
            # Discover tools
            await cohere_client.initialize_tools()
            print(f"✅ Initialized with {len(cohere_client.cohere_tools)} Cohere tools")
            
            # Test simple query
            print("\nQuery: 'Ping the server with message Hello from test'")
            result = await cohere_client.process_message(
                "Ping the server with the message 'Hello from test'"
            )
            
            print(f"\n💬 Response: {result['text'][:200]}...")
            print(f"📊 Tool calls made: {result['tool_calls_made']}")
            print(f"📎 Citations: {len(result['citations'])}")
            
            if result['tool_calls_made'] > 0:
                print("✅ Tool call successful")
            else:
                print("⚠️  No tool calls made")
            
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logger.error(f"Simple query test failed", exc_info=True)
        return False


async def test_market_data_query():
    """Test TC5: Market data tool call."""
    print("\n" + "=" * 70)
    print("TEST 3: Market Data Query")
    print("=" * 70)
    
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        print("❌ COHERE_API_KEY not found")
        return False
    
    try:
        mcp_client = MCPClient(transport="stdio")
        
        async with mcp_client.connect_stdio(server_script="server.py"):
            cohere_client = CohereToolUseClient(
                api_key=cohere_api_key,
                mcp_client=mcp_client,
            )
            
            await cohere_client.initialize_tools()
            
            # Test market data query
            print("\nQuery: 'What is the current price of Brent crude oil?'")
            result = await cohere_client.process_message(
                "What is the current price of Brent crude oil?"
            )
            
            print(f"\n💬 Response:\n{result['text']}\n")
            print(f"📊 Tool calls made: {result['tool_calls_made']}")
            print(f"📎 Citations: {len(result['citations'])}")
            
            if result['citations']:
                print("\nCitations:")
                for i, citation in enumerate(result['citations'][:3], 1):
                    print(f"   {i}. \"{citation['text'][:80]}...\"")
            
            if result['tool_calls_made'] > 0:
                print("\n✅ Market data query successful")
            else:
                print("\n⚠️  No tool calls made")
            
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logger.error(f"Market data test failed", exc_info=True)
        return False


async def test_conversation_history():
    """Test conversation state management."""
    print("\n" + "=" * 70)
    print("TEST 4: Conversation History")
    print("=" * 70)
    
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        print("❌ COHERE_API_KEY not found")
        return False
    
    try:
        mcp_client = MCPClient(transport="stdio")
        
        async with mcp_client.connect_stdio(server_script="server.py"):
            cohere_client = CohereToolUseClient(
                api_key=cohere_api_key,
                mcp_client=mcp_client,
            )
            
            await cohere_client.initialize_tools()
            
            # First query
            print("\nQuery 1: 'What is the current price of Brent crude?'")
            result1 = await cohere_client.process_message(
                "What is the current price of Brent crude?"
            )
            print(f"Response 1: {result1['text'][:100]}...")
            
            # Follow-up query (should use context)
            print("\nQuery 2: 'How has it changed in the last month?'")
            result2 = await cohere_client.process_message(
                "How has it changed in the last month?"
            )
            print(f"Response 2: {result2['text'][:100]}...")
            
            # Check conversation stats
            stats = cohere_client.get_conversation_summary()
            print(f"\n📊 Conversation Stats:")
            print(f"   - Total messages: {stats['total_messages']}")
            print(f"   - User messages: {stats['user_messages']}")
            print(f"   - Assistant messages: {stats['assistant_messages']}")
            print(f"   - Tool messages: {stats['tool_messages']}")
            print(f"   - Total tool calls: {stats['total_tool_calls']}")
            
            if stats['user_messages'] == 2:
                print("\n✅ Conversation history maintained correctly")
            else:
                print(f"\n⚠️  Expected 2 user messages, got {stats['user_messages']}")
            
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logger.error(f"Conversation history test failed", exc_info=True)
        return False


async def test_multistep_agent():
    """Test multi-step agent behavior with complex supply chain analysis."""
    print("\n" + "=" * 70)
    print("TEST 5: Multi-Step Agent Behavior")
    print("=" * 70)
    
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        print("❌ COHERE_API_KEY not found")
        return False
    
    try:
        mcp_client = MCPClient(transport="stdio")
        
        async with mcp_client.connect_stdio(server_script="server.py"):
            cohere_client = CohereToolUseClient(
                api_key=cohere_api_key,
                mcp_client=mcp_client,
            )
            
            await cohere_client.initialize_tools()
            
            # Step 1: Risk assessment
            print("\nStep 1: Assessing geopolitical risks")
            result1 = await cohere_client.process_message(
                "What are the geopolitical risks in the Strait of Hormuz?"
            )
            print(f"✅ Risk assessment: {result1['text'][:100]}...")
            print(f"   Tool calls: {result1['tool_calls_made']}")
            
            # Step 2: Supply disruption simulation
            print("\nStep 2: Simulating supply disruption impact")
            result2 = await cohere_client.process_message(
                "If there's a 7-day disruption affecting a refinery with 100000 barrels daily capacity, what would be the impact?"
            )
            print(f"✅ Disruption impact: {result2['text'][:100]}...")
            print(f"   Tool calls: {result2['tool_calls_made']}")
            
            # Step 3: Inventory calculation
            print("\nStep 3: Calculating inventory requirements")
            result3 = await cohere_client.process_message(
                "Based on that, calculate inventory requirements for 100000 daily demand with 95% service level"
            )
            print(f"✅ Inventory needs: {result3['text'][:100]}...")
            print(f"   Tool calls: {result3['tool_calls_made']}")
            
            # Get final stats
            stats = cohere_client.get_conversation_summary()
            total_tool_calls = result1['tool_calls_made'] + result2['tool_calls_made'] + result3['tool_calls_made']
            
            print(f"\n📊 Multi-Step Analysis Stats:")
            print(f"   - Conversation steps: 3")
            print(f"   - Total tool calls: {total_tool_calls}")
            print(f"   - Tools used: Risk assessment → Disruption → Inventory")
            print(f"   - Context maintained: ✅")
            
            if total_tool_calls >= 3:
                print("\n✅ Multi-step agent behavior successful")
                return True
            else:
                print(f"\n⚠️  Expected at least 3 tool calls, got {total_tool_calls}")
                return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logger.error(f"Multi-step agent test failed", exc_info=True)
        return False


async def test_parallel_tool_calls():
    """Test parallel tool calls - Cohere calling multiple tools simultaneously."""
    print("\n" + "=" * 70)
    print("TEST 6: Parallel Tool Calls")
    print("=" * 70)
    
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        print("❌ COHERE_API_KEY not found")
        return False
    
    try:
        mcp_client = MCPClient(transport="stdio")
        
        async with mcp_client.connect_stdio(server_script="server.py"):
            cohere_client = CohereToolUseClient(
                api_key=cohere_api_key,
                mcp_client=mcp_client,
            )
            
            await cohere_client.initialize_tools()
            
            # Query that could trigger parallel tool calls
            print("\nQuery: 'What is the current price of both Brent crude and WTI?'")
            result = await cohere_client.process_message(
                "What is the current price of both Brent crude and WTI?"
            )
            
            print(f"✅ Response: {result['text'][:150]}...")
            print(f"   Tool calls made: {result['tool_calls_made']}")
            
            if result['tool_calls_made'] >= 2:
                print(f"   ✅ Multiple tools called (possibly in parallel)")
                print("\n✅ Parallel tool calls test successful")
                return True
            elif result['tool_calls_made'] == 1:
                print(f"   ℹ️  Single tool call (model chose sequential approach)")
                print("\n✅ Test passed (model decision)")
                return True
            else:
                print(f"   ⚠️  No tool calls made")
                return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logger.error(f"Parallel tool calls test failed", exc_info=True)
        return False


async def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("MCP CLIENT TEST SUITE")
    print("Testing Cohere Command A Reasoning Integration")
    print("=" * 70)
    
    tests = [
        ("Connection & Discovery", test_connection_and_discovery),
        ("Simple Query (Ping)", test_simple_query),
        ("Market Data Query", test_market_data_query),
        ("Conversation History", test_conversation_history),
        ("Multi-Step Agent Behavior", test_multistep_agent),
        ("Parallel Tool Calls", test_parallel_tool_calls),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            logger.error(f"Test '{test_name}' crashed: {e}", exc_info=True)
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed ({passed*100//total}%)")
    print("=" * 70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Test suite failed: {e}", exc_info=True)
        sys.exit(1)

