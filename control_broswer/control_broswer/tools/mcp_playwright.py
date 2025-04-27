from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

async def get_playwright_tools_async():
  """Gets tools from the PlayWright MCP Server."""
  print("Attempting to connect to MCP Ui test server...")
  tools, exit_stack = await MCPToolset.from_server(
      # Use StdioServerParameters for local process communication
      connection_params=StdioServerParameters(
          command='npx', # Command to run the server
          args=["-y",    # Arguments for the command
                "@playwright/mcp@latest"],
      )
  )
  print("MCP PlayWright Toolset created successfully.")
  #MCP requires maintaining a connection to the local MCP Server.
  #exit_stack manages the cleanup of this connection.
  return tools, exit_stack