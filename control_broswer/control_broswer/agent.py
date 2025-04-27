from google.adk.agents import LlmAgent
from control_broswer import prompt
from control_broswer.sub_agents.speadsheet_agent.agent import create_speadsheet_agent
from control_broswer.sub_agents.read_system_file_agent.agent import create_file_system_agent
from contextlib import AsyncExitStack


async def create_root_agent():
    """Creates the root agent with subagents, including filesystem_assistant."""
    root_exit_stack = AsyncExitStack()
    try:
        
        # Create filesystem agent
        filesystem_agent, fs_exit_stack = await create_file_system_agent()
        # Create Excel agent
        excel_agent, excel_exit_stack = await create_speadsheet_agent()

        # Push exit stack to root exit stack
        await root_exit_stack.enter_async_context(fs_exit_stack)
        await root_exit_stack.enter_async_context(excel_exit_stack)

        root_agent = LlmAgent(
            model="gemini-2.0-flash-001",
            name="root_agent",
            description="A Quality Assurance using the services of multiple sub-agents",
            instruction=prompt.ROOT_AGENT_INSTR,
            sub_agents=[
                filesystem_agent,
                excel_agent
            ],
        )

        return root_agent, root_exit_stack
    
    except Exception as e:
        # Ensure cleanup on error
        await root_exit_stack.aclose()
        raise

root_agent = create_root_agent()