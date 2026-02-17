"""Configuration settings for the application."""

import os
import sys

SYSTEM_PROMPT = """
You are an autonomous troubleshooting agent with read-only access to target Linux hosts via a Model Context Protocol (MCP) diagnostics server. Use the server’s provided tools to gather facts, diagnose problems, and produce safe, actionable guidance. Never attempt to modify files, run write operations, or instruct the server to perform destructive actions. Follow these rules for every session:
Capabilities & constraints
You may only use the MCP tools exposed by the linux-mcp-server instance; all operations are read-only.
You may query system information, logs, services, processes, network state, disk usage, package lists, and other diagnostics the server provides.
You must not attempt to run commands that change state, request credentials, escalate privileges, or instruct human operators to run destructive commands (e.g., rm -rf, systemctl disable without review).
When in doubt, prefer additional read-only queries over speculative recommendations.
"""


class Config:
    """Application configuration loaded from environment variables."""

    DEFAULT_LINUX_MCP_SERVER = ".venv/bin/linux-mcp-server"
    DEFAULT_LLM_PROVIDER = "ollama"
    DEFAULT_LLM_MODEL = "llama3.2:latest"
    DEFAULT_LLM_BASE_URL = "http://localhost:11434"
    DEFAULT_REQUEST_TIMEOUT = "90"

    def __init__(self) -> None:
        """Initialize configuration from environment variables with validation."""
        self.linux_mcp_server: str = os.getenv("LINUX_MCP_SERVER", self.DEFAULT_LINUX_MCP_SERVER)
        self.llm_provider: str = (
            os.getenv("LLM_PROVIDER", self.DEFAULT_LLM_PROVIDER).strip().lower()
        )
        self.llm_model: str = os.getenv("LLM_MODEL", self.DEFAULT_LLM_MODEL)
        self.llm_base_url: str = os.getenv("LLM_BASE_URL", self.DEFAULT_LLM_BASE_URL)

        # Validate provider and fall back to default when an invalid value is provided.
        valid_providers = {"ollama", "googlegenai"}
        if self.llm_provider not in valid_providers:
            print(
                (
                    f"Error: Invalid LLM_PROVIDER value '{self.llm_provider}'. "
                    f"Using default provider: {self.DEFAULT_LLM_PROVIDER}"
                ),
                file=sys.stderr,
            )
            self.llm_provider = self.DEFAULT_LLM_PROVIDER

        # Validate and parse request timeout with a safe fallback.
        timeout_str = os.getenv("REQUEST_TIMEOUT", self.DEFAULT_REQUEST_TIMEOUT)
        try:
            self.request_timeout: int = int(timeout_str)
            if self.request_timeout <= 0:
                raise ValueError("REQUEST_TIMEOUT must be positive")
        except ValueError as e:
            print(f"Error: Invalid REQUEST_TIMEOUT value '{timeout_str}': {e}", file=sys.stderr)
            print(f"Using default timeout: {self.DEFAULT_REQUEST_TIMEOUT} seconds", file=sys.stderr)
            self.request_timeout = int(self.DEFAULT_REQUEST_TIMEOUT)


config = Config()
