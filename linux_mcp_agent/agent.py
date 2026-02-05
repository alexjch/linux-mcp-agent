import asyncio
import requests
from typing import Any
from linux_mcp_agent.config import config, SYSTEM_PROMPT
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec  # type: ignore[import-untyped]
from llama_index.core.agent.workflow import FunctionAgent
from rich.console import Console
from rich.prompt import Prompt
from llama_index.llms.ollama import Ollama  # type: ignore[import-untyped]

console = Console()


async def get_tool_list() -> Any:
    """Initialize MCP client and retrieve available tools from the MCP server."""
    mcp_client = BasicMCPClient(config.linux_mcp_server)
    mcp_tool_spec = McpToolSpec(client=mcp_client)
    tools = await mcp_tool_spec.to_tool_list_async()
    return tools


async def check_required_models() -> bool:
    """Check if the required LLM model is available in Ollama."""
    try:
        response = requests.get(f"{config.llm_base_url}/api/tags")
        response.raise_for_status()
        available_models = [model["name"] for model in response.json().get("models", [])]
        return config.llm_model in available_models

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to connect to Ollama API at {config.llm_base_url}: {e}")


async def pull_model() -> bool:
    """Pull model using the ollama API."""
    try:
        resp = requests.post(f"{config.llm_base_url}/api/pull", json={"name": config.llm_model})
        resp.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred while pulling model: {e}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Failed to pull model from Ollama: {e}")
        return False


async def provision_models() -> bool:
    if not await check_required_models():
        console.print(f"[red]Required model '{config.llm_model}' not found in Ollama[/red]")
        console.print(f"[yellow]Attempting to pull model '{config.llm_model}'...[/yellow]")
        return await pull_model()
    return True


async def start_chat() -> int:
    llm = Ollama(
        model=config.llm_model, base_url=config.llm_base_url, request_timeout=config.request_timeout
    )

    tools = await get_tool_list()

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

    if not await provision_models():
        console.print(f"[red]Model {config.llm_model} is not available")

    return await start_chat()


if __name__ == "__main__":
    asyncio.run(main())
