.PHONY: help lint format test install clean all

help:
	@echo "Available targets:"
	@echo "  make install  - Install dependencies"
	@echo "  make format   - Format code with black"
	@echo "  make lint     - Run linters (flake8, mypy)"
	@echo "  make test     - Run tests with pytest"
	@echo "  make all      - Run format, lint, and test"
	@echo "  make clean    - Remove Python cache files"

install:
	pip install -r requirements.txt

format:
	black mcp_linux_agent/ tests/ examples/

lint:
	flake8 mcp_linux_agent/ tests/ examples/ --max-line-length=100
	mypy mcp_linux_agent/

test:
	pytest tests/ -v

all: format lint test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
