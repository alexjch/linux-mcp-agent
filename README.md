# mcp-linux-agent

A lightweight CLI client for the [Linux MCP server](https://github.com/rhel-lightspeed/linux-mcp-server). Unlike graphical alternatives, this tool runs on headless servers without requiring X11 or other display libraries, enabling interactive Linux system diagnostics directly from the terminal.

## Features

- 🤖 Interactive chat interface with AI-powered troubleshooting
- 🔍 Read-only system diagnostics via [Linux MCP server](https://github.com/rhel-lightspeed/linux-mcp-server)
- 🎨 Rich console UI with color-coded output
- ⚙️ Environment-based configuration
- 🐳 Dev container support for easy setup

## Prerequisites

- Python 3.9+
- [Ollama](https://ollama.ai) running locally (default: http://localhost:11434)
- [linux-mcp-server](https://github.com/modelcontextprotocol/servers) installed

## Installation

### Quick Start with Dev Container

1. Open project in VS Code
2. Reopen in container when prompted
3. Wait for automatic setup to complete

### Manual Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install linux-mcp-server
pip install linux-mcp-server
```

## Configuration

Configure via environment variables or use defaults:

| Variable | Default | Description |
|----------|---------|-------------|
| `LINUX_MCP_SERVER` | `.bin/linux-mcp-server` | Path to MCP server executable |
| `LLM_MODEL` | `llama3.2:latest` | Ollama model to use |
| `LLM_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `REQUEST_TIMEOUT` | `90` | Request timeout in seconds |

## Usage

### Run the Agent

```bash
# As a module
python -m linux_mcp_agent

# Or directly
python linux_mcp_agent
```

### Example Session

```
You: What is the free disk space?
Agent: [Analyzes system and provides disk usage information]

You: Check if nginx is running
Agent: [Queries service status and reports findings]

You: exit
Goodbye!
```

## Development

### Available Make Targets

```bash
make install   # Install dependencies
make format    # Format code with black
make lint      # Run flake8 and mypy
make test      # Run pytest
make all       # Run format, lint, and test
make clean     # Remove cache files
```

### Project Structure

```
linux_mcp_agent/
├── __init__.py      # Package initialization
├── __main__.py      # Entry point
├── agent.py         # Main agent logic
└── config.py        # Configuration management
tests/
├── __init__.py
└── test_config.py   # Configuration tests
```

## Architecture

The agent uses:
- **LlamaIndex**: Framework for LLM-powered applications
- **MCP (Model Context Protocol)**: Standard protocol for tool access
- **Ollama**: Local LLM inference
- **Rich**: Terminal UI formatting

The agent operates in read-only mode, gathering system diagnostics without making modifications.

## License

See [LICENSE](LICENSE) file for details.
