"""Tests for agent module."""

import pytest
import requests
from unittest.mock import MagicMock, patch
from linux_mcp_agent.agent import (
    check_required_models,
    pull_model,
    provision_models,
)


@pytest.mark.asyncio
async def test_check_required_models_success():
    """Test checking for available models when model exists."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "models": [
            {"name": "llama3.2:latest"},
            {"name": "gemma:2b"},
        ]
    }

    with patch("linux_mcp_agent.agent.requests.get", return_value=mock_response):
        result = await check_required_models()
        assert result is True


@pytest.mark.asyncio
async def test_check_required_models_not_found():
    """Test checking for available models when model doesn't exist."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "models": [
            {"name": "other-model:latest"},
        ]
    }

    with patch("linux_mcp_agent.agent.requests.get", return_value=mock_response):
        result = await check_required_models()
        assert result is False


@pytest.mark.asyncio
async def test_check_required_models_connection_error():
    """Test checking for models with connection error."""
    with patch(
        "linux_mcp_agent.agent.requests.get",
        side_effect=requests.exceptions.RequestException("Connection refused"),
    ):
        with pytest.raises(RuntimeError, match="Failed to connect to Ollama API"):
            await check_required_models()


@pytest.mark.asyncio
async def test_pull_model_success():
    """Test pulling a model successfully."""
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()

    with patch("linux_mcp_agent.agent.requests.post", return_value=mock_response):
        result = await pull_model()
        assert result is True


@pytest.mark.asyncio
async def test_pull_model_http_error():
    """Test pulling a model with HTTP error."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

    with patch("linux_mcp_agent.agent.requests.post", return_value=mock_response):
        result = await pull_model()
        assert result is False


@pytest.mark.asyncio
async def test_provision_models_already_available():
    """Test provisioning when model is already available."""
    with patch("linux_mcp_agent.agent.check_required_models", return_value=True):
        result = await provision_models()
        assert result is True


@pytest.mark.asyncio
async def test_provision_models_needs_pulling():
    """Test provisioning when model needs to be pulled."""
    with patch("linux_mcp_agent.agent.check_required_models", return_value=False):
        with patch("linux_mcp_agent.agent.pull_model", return_value=True):
            result = await provision_models()
            assert result is True


@pytest.mark.asyncio
async def test_provision_models_pull_fails():
    """Test provisioning when model pull fails."""
    with patch("linux_mcp_agent.agent.check_required_models", return_value=False):
        with patch("linux_mcp_agent.agent.pull_model", return_value=False):
            result = await provision_models()
            assert result is False
