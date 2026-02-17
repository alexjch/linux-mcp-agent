import requests
from typing import Any
from llama_index.core.llms import LLM
from rich.console import Console
from linux_mcp_agent.config import config

console = Console()


async def pull_model() -> bool:
    """
    Pull a model from the Ollama API.

    Makes an HTTP POST request to the Ollama API endpoint to pull/download a model
    specified in the configuration.

    Returns:
        bool: True if the model was successfully pulled, False if an HTTP error
              or request exception occurred during the pull operation.

    Notes:
        Network and HTTP request exceptions are handled internally and reported to the console.
    """
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
    try:
        response = requests.get(f"{config.llm_base_url}/api/tags")
        response.raise_for_status()
        available_models = [model["name"] for model in response.json().get("models", [])]
        return config.llm_model in available_models

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to connect to Ollama API at {config.llm_base_url}: {e}")


async def provision_models() -> bool:
    """
    Asynchronously provision required models for the agent.

    Checks if the required LLM model is available in Ollama. If not found,
    attempts to pull the model from a remote repository.

    Returns:
        bool: True if provisioning is not required, the model is already available,
        or model pull succeeds; False if model pull fails.

    Raises:
        RuntimeError: Propagated when the model availability check cannot reach the Ollama API.
    """
    # Only Ollama requires local model provisioning.
    if config.llm_provider != "ollama":
        return True

    if not await check_required_models():
        console.print(f"[red]Required model '{config.llm_model}' not found in Ollama[/red]")
        console.print(f"[yellow]Attempting to pull model '{config.llm_model}'...[/yellow]")
        return await pull_model()
    return True


def init_llm() -> LLM | Any:
    """Initialize and return the configured LLM implementation."""
    # Keep imports local so optional provider dependencies are only required when selected.
    if config.llm_provider == "ollama":
        from llama_index.llms.ollama import Ollama  # type: ignore[import-untyped]

        return Ollama(
            model=config.llm_model,
            base_url=config.llm_base_url,
            request_timeout=config.request_timeout,
        )

    if config.llm_provider == "googlegenai":
        from llama_index.llms.google_genai import GoogleGenAI  # type: ignore[import-untyped]

        return GoogleGenAI(model=config.llm_model)

    # Config validation should prevent this path, but keep a defensive error for safety.
    raise ValueError(f"Unsupported LLM provider: {config.llm_provider}")
