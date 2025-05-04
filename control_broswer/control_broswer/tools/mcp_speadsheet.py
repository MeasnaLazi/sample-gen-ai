# from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
# from contextlib import AsyncExitStack

# # async def get_speadsheet_tools_async():
# #     """Creates SpeadSheet agent with mcp-google-sheets tools."""
# #     # Configure MCPToolset for mcp-google-sheets server
# #     mcp_params = StdioServerParameters(
# #         command="uvx",
# #         args=["mcp-google-sheets"],
# #         env={
# #             "SERVICE_ACCOUNT_PATH": "/Users/measna/Documents/Personal\ Project/Generative\ AI/GenAi/samples/control_broswer/resources/google_service_account_cred.json",
# #             "DRIVE_FOLDER_ID": "1tnniL6IkvHjss523hACyYFlMmLWqo-YL"
# #         }
# #     )
# #     exit_stack = AsyncExitStack()
# #     mcp_toolset = await exit_stack.enter_async_context(
# #         MCPToolset(connection_params=mcp_params)
# #     )
# #     tools = await mcp_toolset.get_tools()

# #     return tools, exit_stack


# async def get_speadsheet_tools_async():
#   """Gets tools from the File System MCP Server."""
#   print("Attempting to connect to MCP Filesystem server...")
#   tools, exit_stack = await MCPToolset.from_server(
#       # Use StdioServerParameters for local process communication
#       connection_params=StdioServerParameters(
#           command='uvx', # Command to run the server
#           args=["mcp-google-sheets"],
#           env={
#             "SERVICE_ACCOUNT_PATH": "/Users/measna/Documents/google_service_account_cred.json",
#             "DRIVE_FOLDER_ID": "1tnniL6IkvHjss523hACyYFlMmLWqo-YL"
#         }
#       )
#       # For remote servers, you would use SseServerParams instead:
#       # connection_params=SseServerParams(url="http://remote-server:port/path", headers={...})
#   )
#   tools = [tool for tool in tools if tool.name != "get_sheet_data"]

#   print("MCP Toolset of speadsheet created successfully.")
#   #MCP requires maintaining a connection to the local MCP Server.
#   #exit_stack manages the cleanup of this connection.
#   return tools, exit_stack