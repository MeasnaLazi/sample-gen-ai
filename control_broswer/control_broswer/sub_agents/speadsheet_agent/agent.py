from google.adk.agents import LlmAgent
from control_broswer.sub_agents.speadsheet_agent import prompt
from control_broswer.tools.mcp_speadsheet import get_speadsheet_tools_async

async def create_speadsheet_agent():
  """Gets tools from MCP Server."""
  tools, exit_stack = await get_speadsheet_tools_async()

  agent = LlmAgent(
      model='gemini-2.0-flash', # Adjust model name if needed based on availability
      name='speadsheet_agent',
      instruction=prompt.SYSTEM_EXCEL_INSTR,
      tools=tools, # Provide the MCP tools to the ADK agent
      description="Handles spreadsheet operations, including Google Sheets tasks like creating, reading, and updating spreadsheets."
  )
  return agent, exit_stack