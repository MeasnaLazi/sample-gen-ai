from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

async def get_stay25_tools_async():
  """Gets tools from the Stay25 MCP Server."""
  print("Attempting to connect to Stay25 server...")
  tools, exit_stack = await MCPToolset.from_server(
      # Use StdioServerParameters for local process communication
      connection_params=StdioServerParameters(
          command='node', # Command to run the server
          args=["/Users/measna/Documents/Personal Project/Generative AI/sample-gen-ai/stay_25_mcp/build/index.js"],
      )
  )
  print("MCP Stay25 Toolset created successfully.")
  #MCP requires maintaining a connection to the local MCP Server.
  #exit_stack manages the cleanup of this connection.
  return tools, exit_stack