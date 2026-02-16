from linux_mcp_agent.config import config


def init_llm():
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