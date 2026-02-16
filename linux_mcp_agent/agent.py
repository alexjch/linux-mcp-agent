import asyncio
import requests
from linux_mcp_agent.config import config, SYSTEM_PROMPT
from linux_mcp_agent.model import init_llm
from llama_index.tools.mcp import McpToolSpec  # type: ignore[import-untyped]
from llama_index.core.agent.workflow import FunctionAgent
from rich.console import Console
from rich.prompt import Prompt
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

console = Console()


async def check_required_models() -> bool:
    """
    Check if the required LLM model is available in Ollama.

    This function connects to the Ollama API and retrieves a list of available models,
    then verifies whether the configured LLM model is present in that list.

    Returns:
        bool: True if the required model is available in Ollama, False otherwise.

    Raises:
        RuntimeError: If the connection to the Ollama API fails or times out.
    """
    """Check if the required LLM model is available in Ollama."""
    try:
        response = requests.get(f"{config.llm_base_url}/api/tags")
        response.raise_for_status()
        available_models = [model["name"] for model in response.json().get("models", [])]
        return config.llm_model in available_models

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to connect to Ollama API at {config.llm_base_url}: {e}")


async def pull_model() -> bool:
    """
    Pull a model from the Ollama API.

    Makes an HTTP POST request to the Ollama API endpoint to pull/download a model
    specified in the configuration.

    Returns:
        bool: True if the model was successfully pulled, False if an HTTP error
              or request exception occurred during the pull operation.

    Raises:
        None: Exceptions are caught and logged internally; no exceptions are raised.
    """
    """Pull model using the ollama API."""
    try:
        resp = requests.post(f"{config.llm_base_url}/api/pull", json={"name": config.llm_model})
        resp.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        console.print(f"[red]HTTP error occurred while pulling model: {e}[/red]")
        return False
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Failed to pull model from Ollama: {e}[/red]")
        return False


async def provision_models() -> bool:
    """
    Asynchronously provision required models for the agent.

    Checks if the required LLM model is available in Ollama. If not found,
    attempts to pull the model from a remote repository.

    Returns:
        bool: True if the required model is available or successfully pulled,
                False if the model check fails and the pull operation unsuccessful.

    Raises:
        None explicitly, but may raise exceptions from check_required_models()
        or pull_model() if they are not properly handled internally.
    """
    # Only Ollama requires local model provisioning.
    if config.llm_provider != "ollama":
        return True

    if not await check_required_models():
        console.print(f"[red]Required model '{config.llm_model}' not found in Ollama[/red]")
        console.print(f"[yellow]Attempting to pull model '{config.llm_model}'...[/yellow]")
        return await pull_model()
    return True


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
    if not await provision_models():
        console.print(f"[red]Model {config.llm_model} is not available[/red]")
        # Return a non-zero exit code to indicate provisioning failure and avoid starting chat.
        return 1

    return await start_chat()


if __name__ == "__main__":
    asyncio.run(main())
