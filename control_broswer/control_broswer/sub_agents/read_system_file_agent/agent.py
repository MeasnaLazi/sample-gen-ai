from google.adk.agents import LlmAgent
from control_broswer.sub_agents.read_system_file_agent import prompt
from control_broswer.tools.mcp_filesystem import get_file_system_tools_async

async def create_file_system_agent():
  """Gets tools from MCP Server."""
  tools, exit_stack = await get_file_system_tools_async()

  agent = LlmAgent(
      model='gemini-2.0-flash-001', # Adjust model name if needed based on availability
      name='filesystem_agent',
      instruction=prompt.SYSTEM_FILE_AGENT_INSTR,
      tools=tools, # Provide the MCP tools to the ADK agent
  )
  return agent, exit_stack