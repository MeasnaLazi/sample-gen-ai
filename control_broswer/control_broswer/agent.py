from google.adk.agents import LlmAgent
from control_broswer import prompt
from control_broswer.sub_agents.airbnb_agent.agent import create_airbnb_agent
from control_broswer.sub_agents.read_system_file_agent.agent import create_file_system_agent
from control_broswer.sub_agents.playwright_agent.agent import create_playwright_agent
from contextlib import AsyncExitStack


async def create_root_agent():
    """Creates the root agent with subagents, including filesystem_assistant."""
    root_exit_stack = AsyncExitStack()
    try:
        
        # Create filesystem agent
        filesystem_agent, fs_exit_stack = await create_file_system_agent()
        await root_exit_stack.enter_async_context(fs_exit_stack)
        
        #Create Airbnb agent
        airbnb_agent, airbnb_exit_stack = await create_airbnb_agent()       
        await root_exit_stack.enter_async_context(airbnb_exit_stack)

        #Create Airbnb agent
        playwright_agent, playwright_exit_stack = await create_playwright_agent()       
        await root_exit_stack.enter_async_context(playwright_exit_stack)

        root_agent = LlmAgent(
            model="gemini-2.0-flash-001",
            name="root_agent",
            description="A Manager using the services of multiple sub-agents",
            instruction=prompt.ROOT_AGENT_INSTR,
            sub_agents=[
                filesystem_agent,
                airbnb_agent,
                playwright_agent
            ],
        )

        return root_agent, root_exit_stack
    
    except Exception as e:
        # Ensure cleanup on error
        await root_exit_stack.aclose()
        raise

root_agent = create_root_agent()