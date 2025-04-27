from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

async def get_file_system_tools_async():
  """Gets tools from the File System MCP Server."""
  print("Attempting to connect to MCP Filesystem server...")
  tools, exit_stack = await MCPToolset.from_server(
      # Use StdioServerParameters for local process communication
      connection_params=StdioServerParameters(
          command='npx', # Command to run the server
          args=["-y",    # Arguments for the command
                "@modelcontextprotocol/server-filesystem",
                # TODO: IMPORTANT! Change the path below to an ABSOLUTE path on your system.
                "/Users/measna/Documents/Personal Project/Generative AI/GenAi/samples/control_broswer/data/"],
      )
      # For remote servers, you would use SseServerParams instead:
      # connection_params=SseServerParams(url="http://remote-server:port/path", headers={...})
  )
  print("MCP Toolset created successfully.")
  #MCP requires maintaining a connection to the local MCP Server.
  #exit_stack manages the cleanup of this connection.
  return tools, exit_stack