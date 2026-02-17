import asyncio
from linux_mcp_agent.config import config, SYSTEM_PROMPT
from linux_mcp_agent.model import init_llm, provision_models
from llama_index.tools.mcp import McpToolSpec  # type: ignore[import-untyped]
from llama_index.core.agent.workflow import FunctionAgent
from rich.console import Console
from rich.prompt import Prompt
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

console = Console()


async def start_chat() -> int:
    """
    Start an interactive chat session with the agent.

    Initializes the LLM and agent, then enters a loop accepting user input
    and displaying agent responses until the user exits or interrupts.
    The MCP client connection is maintained throughout the session for efficiency.

    Returns:
        int: Exit code (0 for successful completion).
    """
    llm = init_llm()

    server_params = StdioServerParameters(
        command=config.linux_mcp_server,
        args=[],
    )

    # Keep MCP client alive for the entire session
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as client:
            # Initialize the connection
            await client.initialize()
            mcp_tool_spec = McpToolSpec(client=client)
            tools = await mcp_tool_spec.to_tool_list_async()

            agent = FunctionAgent(
                tools=tools,
                llm=llm,
                system_prompt=SYSTEM_PROMPT,
            )

            while True:
                try:
                    user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
                    if user_input.lower() in ("exit", "quit"):
                        console.print("[yellow]Goodbye![/yellow]")
                        break

                    response = await agent.run(user_input)  # type: ignore
                    console.print(f"[bold green]Agent[/bold green]: {response}")
                except KeyboardInterrupt:
                    console.print("\n[yellow]Interrupted[/yellow]")
                    break
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")
    return 0


async def main() -> int:
    """
    Main entry point for the Linux MCP agent application.

    Provisions required models and starts the interactive chat session.

    Returns:
        int: Exit code (0 for success, non-zero for failure).
    """
    if config.llm_provider == "ollama":
        if not await provision_models():
            console.print(f"[red]Model {config.llm_model} is not available[/red]")
            # Return a non-zero exit code to indicate provisioning failure and avoid starting chat.
            return 1

    return await start_chat()


if __name__ == "__main__":
    asyncio.run(main())
