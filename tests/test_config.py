"""Tests for configuration module."""

from linux_mcp_agent.config import Config, SYSTEM_PROMPT


def test_config_defaults():
    """Test that config loads default values correctly."""
    config = Config()
    assert config.linux_mcp_server == ".venv/bin/linux-mcp-server"
    assert config.llm_provider == "ollama"
    assert config.llm_model == "llama3.2:latest"
    assert config.llm_base_url == "http://localhost:11434"
    assert config.request_timeout == 90


def test_config_from_environment(monkeypatch):
    """Test that config loads from environment variables."""
    monkeypatch.setenv("LINUX_MCP_SERVER", "/custom/path/server")
    monkeypatch.setenv("LLM_PROVIDER", "googlegenai")
    monkeypatch.setenv("LLM_MODEL", "llama3:7b")
    monkeypatch.setenv("LLM_BASE_URL", "http://custom:8080")
    monkeypatch.setenv("REQUEST_TIMEOUT", "120")

    config = Config()
    assert config.linux_mcp_server == "/custom/path/server"
    assert config.llm_provider == "googlegenai"
    assert config.llm_model == "llama3:7b"
    assert config.llm_base_url == "http://custom:8080"
    assert config.request_timeout == 120


def test_system_prompt_exists():
    """Test that system prompt is defined."""
    assert SYSTEM_PROMPT is not None
    assert len(SYSTEM_PROMPT) > 0
    assert "read-only" in SYSTEM_PROMPT.lower()
