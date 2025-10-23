# MCP Client Testing Specification

## ADDED Requirements

### Requirement: MCP Client Foundation
The system SHALL provide an MCP client that connects to the demand planning MCP server and enables AI-assisted interactions using Cohere's Command A model.

#### Scenario: Connect via stdio transport
- **WHEN** the client is started with `--transport stdio` flag
- **THEN** the client SHALL establish a connection to the MCP server via stdio
- **AND** the client SHALL discover available tools from the server
- **AND** the client SHALL display an interactive prompt for user queries

#### Scenario: Connect via HTTP transport
- **WHEN** the client is started with `--transport streamable-http --port 8000` flag
- **THEN** the client SHALL establish an HTTP connection to the MCP server
- **AND** the client SHALL discover available tools from the server
- **AND** the client SHALL display an interactive prompt for user queries

#### Scenario: Handle MCP connection failure
- **WHEN** the client attempts to connect to the MCP server and the server is unavailable
- **THEN** the client SHALL display a clear error message
- **AND** the client SHALL exit gracefully with a non-zero status code

### Requirement: Tool Schema Conversion
The system SHALL convert MCP tool schemas to Cohere's JSON Schema format to enable tool use.

#### Scenario: Convert single MCP tool schema
- **WHEN** an MCP tool with JSON Schema is fetched from the server
- **THEN** the system SHALL convert it to Cohere's tool schema format
- **AND** the converted schema SHALL include type="function"
- **AND** the function SHALL include name, description, and parameters
- **AND** the parameters SHALL include type, properties, and required fields

#### Scenario: Convert multiple MCP tool schemas
- **WHEN** multiple MCP tools are discovered from the server
- **THEN** the system SHALL convert all tool schemas to Cohere format
- **AND** the system SHALL return a list of Cohere-compatible tool definitions

#### Scenario: Handle missing optional fields
- **WHEN** an MCP tool schema has missing optional fields (e.g., no required parameters)
- **THEN** the system SHALL convert the schema with appropriate defaults
- **AND** the converted schema SHALL remain valid for Cohere's API

### Requirement: Cohere Tool Use Workflow
The system SHALL implement Cohere's 4-step tool use workflow for AI-assisted conversations.

#### Scenario: Single tool call workflow
- **WHEN** a user asks "What's the current price of Brent crude?"
- **THEN** the system SHALL append the user message to the conversation
- **AND** the system SHALL call Cohere's chat API with the user message and available tools
- **AND** the system SHALL receive tool_plan and tool_calls from Cohere
- **AND** the system SHALL execute the tool call via the MCP server
- **AND** the system SHALL append tool results to the conversation
- **AND** the system SHALL call Cohere's chat API again to generate the final response
- **AND** the system SHALL display the response with citations to the user

#### Scenario: Parallel tool calls
- **WHEN** Cohere determines multiple tools should be called in parallel
- **THEN** the system SHALL execute all tool calls via the MCP server
- **AND** the system SHALL append all tool results to the conversation
- **AND** the system SHALL call Cohere's chat API to generate the final response

#### Scenario: Multi-step tool use (agent behavior)
- **WHEN** Cohere determines additional tool calls are needed after receiving tool results
- **THEN** the system SHALL repeat the tool execution loop
- **AND** the system SHALL continue until Cohere generates a final response without tool calls

#### Scenario: Direct response without tools
- **WHEN** Cohere determines no tools are needed to answer the user query
- **THEN** the system SHALL display the direct response from Cohere
- **AND** the system SHALL not execute any tool calls

### Requirement: Conversation State Management
The system SHALL maintain conversation state across multiple turns to support multi-turn interactions.

#### Scenario: Maintain conversation history
- **WHEN** a user asks a follow-up question
- **THEN** the system SHALL include all previous messages in the conversation
- **AND** the system SHALL pass the full conversation history to Cohere
- **AND** Cohere SHALL have context from previous interactions

#### Scenario: Reset conversation
- **WHEN** a user types "reset" command
- **THEN** the system SHALL clear the conversation history
- **AND** the system SHALL display a confirmation message
- **AND** subsequent queries SHALL start a new conversation

#### Scenario: Track tool call IDs
- **WHEN** Cohere generates tool calls with unique IDs
- **THEN** the system SHALL preserve the tool call IDs
- **AND** the system SHALL match tool results to their corresponding tool call IDs
- **AND** tool results SHALL be appended with the correct tool_call_id

### Requirement: Interactive CLI Interface
The system SHALL provide an interactive command-line interface for testing MCP server functionality.

#### Scenario: Display startup information
- **WHEN** the client starts successfully
- **THEN** the system SHALL display the client name and Cohere model being used
- **AND** the system SHALL display available commands (exit, reset)
- **AND** the system SHALL display a prompt for user input

#### Scenario: Display tool calls and results
- **WHEN** Cohere generates tool calls
- **THEN** the system SHALL display each tool call with function name and arguments
- **AND** the system SHALL display tool results after execution
- **AND** the display SHALL be formatted for readability

#### Scenario: Display final responses with citations
- **WHEN** Cohere generates a final response
- **THEN** the system SHALL display the response text
- **AND** the system SHALL display citations if present
- **AND** citations SHALL reference the tool results used

#### Scenario: Exit gracefully
- **WHEN** a user types "exit" or "quit" command
- **THEN** the system SHALL close the MCP connection
- **AND** the system SHALL exit with a zero status code

### Requirement: Error Handling and Resilience
The system SHALL handle errors gracefully and provide clear feedback when issues occur.

#### Scenario: Invalid Cohere API key
- **WHEN** the Cohere API key is invalid or missing
- **THEN** the system SHALL display a clear error message
- **AND** the system SHALL indicate that COHERE_API_KEY needs to be configured
- **AND** the system SHALL exit with a non-zero status code

#### Scenario: MCP tool execution failure
- **WHEN** an MCP tool execution fails
- **THEN** the system SHALL log the error details
- **AND** the system SHALL return an error message to Cohere as the tool result
- **AND** Cohere SHALL generate a response acknowledging the tool failure

#### Scenario: Cohere API rate limit
- **WHEN** Cohere API rate limit is exceeded
- **THEN** the system SHALL display a rate limit error message
- **AND** the system SHALL suggest retrying after a delay
- **AND** the conversation state SHALL be preserved

#### Scenario: Network connectivity issues
- **WHEN** network connectivity is lost during an interaction
- **THEN** the system SHALL display a network error message
- **AND** the system SHALL allow the user to retry or exit
- **AND** the conversation state SHALL be preserved

### Requirement: Configuration Management
The system SHALL support configuration via environment variables and command-line arguments.

#### Scenario: Load Cohere API key from environment
- **WHEN** COHERE_API_KEY environment variable is set
- **THEN** the system SHALL use the API key to initialize Cohere client
- **AND** the system SHALL not expose the API key in logs or output

#### Scenario: Override configuration with command-line args
- **WHEN** command-line arguments are provided (--transport, --port, --model)
- **THEN** the system SHALL use these values instead of defaults
- **AND** the system SHALL log the configuration being used

#### Scenario: Use default configuration
- **WHEN** no command-line arguments are provided
- **THEN** the system SHALL use default values (stdio transport, command-a-03-2025 model)
- **AND** the system SHALL function correctly with defaults

### Requirement: Tool Use Testing Scenarios
The system SHALL support testing the MCP server with realistic demand planning scenarios.

#### Scenario: Market data query
- **WHEN** a user asks "What's the current price of Brent crude?"
- **THEN** the system SHALL call get_market_prices tool via MCP
- **AND** the system SHALL display the market price result
- **AND** the system SHALL generate a natural language response with the price

#### Scenario: Risk assessment query
- **WHEN** a user asks "What's the risk of Strait of Hormuz closure?"
- **THEN** the system SHALL call get_geopolitical_risk_assessment tool via MCP
- **AND** the system SHALL display the risk assessment result
- **AND** the system SHALL generate a response with risk probability and impact

#### Scenario: Multi-tool supply chain analysis
- **WHEN** a user asks a complex question requiring multiple tools
- **THEN** the system SHALL call multiple MCP tools as determined by Cohere
- **AND** the system SHALL synthesize results from all tools
- **AND** the system SHALL generate a comprehensive response with citations

#### Scenario: ROI calculation workflow
- **WHEN** a user provides inventory scenario details
- **THEN** the system SHALL call relevant calculation tools (calculate_carrying_costs, calculate_revenue_impact, calculate_roi)
- **AND** the system SHALL display intermediate calculations
- **AND** the system SHALL provide a final recommendation with supporting rationale

