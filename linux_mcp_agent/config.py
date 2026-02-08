import os
import sys

"""Configuration settings for the application."""

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
    DEFAULT_LLM_MODEL = "llama3.2:latest"
    DEFAULT_LLM_BASE_URL = "http://localhost:11434"
    DEFAULT_REQUEST_TIMEOUT = "90"

    def __init__(self) -> None:
        """Initialize configuration from environment variables with validation."""
        self.linux_mcp_server: str = os.getenv("LINUX_MCP_SERVER", self.DEFAULT_LINUX_MCP_SERVER)
        self.llm_model: str = os.getenv("LLM_MODEL", self.DEFAULT_LLM_MODEL)
        self.llm_base_url: str = os.getenv("LLM_BASE_URL", self.DEFAULT_LLM_BASE_URL)

        # Validate and parse request timeout
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
