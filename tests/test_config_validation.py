"""Additional tests for configuration edge cases."""

from linux_mcp_agent.config import Config


def test_config_invalid_timeout_non_numeric(monkeypatch, capsys):
    """Test that invalid non-numeric timeout falls back to default."""
    monkeypatch.setenv("REQUEST_TIMEOUT", "not-a-number")

    config = Config()

    # Should fall back to default
    assert config.request_timeout == 90

    # Should print error message
    captured = capsys.readouterr()
    assert "Invalid REQUEST_TIMEOUT value" in captured.err


def test_config_invalid_timeout_negative(monkeypatch, capsys):
    """Test that negative timeout falls back to default."""
    monkeypatch.setenv("REQUEST_TIMEOUT", "-10")

    config = Config()

    # Should fall back to default
    assert config.request_timeout == 90

    # Should print error message
    captured = capsys.readouterr()
    assert "REQUEST_TIMEOUT must be positive" in captured.err


def test_config_invalid_timeout_zero(monkeypatch, capsys):
    """Test that zero timeout falls back to default."""
    monkeypatch.setenv("REQUEST_TIMEOUT", "0")

    config = Config()

    # Should fall back to default
    assert config.request_timeout == 90

    # Should print error message
    captured = capsys.readouterr()
    assert "REQUEST_TIMEOUT must be positive" in captured.err


def test_config_valid_timeout_string(monkeypatch):
    """Test that valid timeout string is correctly parsed."""
    monkeypatch.setenv("REQUEST_TIMEOUT", "150")

    config = Config()

    assert config.request_timeout == 150
    assert isinstance(config.request_timeout, int)


def test_config_invalid_llm_provider(monkeypatch, capsys):
    """Test that invalid provider falls back to the default provider."""
    monkeypatch.setenv("LLM_PROVIDER", "unknown-provider")

    config = Config()

    assert config.llm_provider == "ollama"

    captured = capsys.readouterr()
    assert "Invalid LLM_PROVIDER value" in captured.err
