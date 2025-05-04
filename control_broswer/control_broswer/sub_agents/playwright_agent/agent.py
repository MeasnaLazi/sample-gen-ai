from google.adk.agents import LlmAgent
from control_broswer.sub_agents.playwright_agent import prompt
from control_broswer.tools.mcp_playwright import get_playwright_tools_async

async def create_playwright_agent():
  """Gets tools from MCP Server."""
  tools, exit_stack = await get_playwright_tools_async()

  agent = LlmAgent(
      model='gemini-2.0-flash-001', # Adjust model name if needed based on availability
      name='web_broswer_agent',
      instruction=prompt.AGENT_INSTR,
      tools=tools, # Provide the MCP tools to the ADK agent
  )
  return agent, exit_stack