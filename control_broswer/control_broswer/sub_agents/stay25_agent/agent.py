from google.adk.agents import LlmAgent
from control_broswer.sub_agents.stay25_agent import prompt
from control_broswer.tools.mcp_stay25 import get_stay25_tools_async

async def create_stay25_agent():
  """Gets tools from MCP Server."""
  tools, exit_stack = await get_stay25_tools_async()

  agent = LlmAgent(
      model='gemini-2.0-flash-001', # Adjust model name if needed based on availability
      name='stay25_agent',
      instruction=prompt.AGENT_INSTR,
      tools=tools, # Provide the MCP tools to the ADK agent
  )
  return agent, exit_stack