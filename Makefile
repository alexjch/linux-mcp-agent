.PHONY: help lint format test install clean all

help:
	@echo "Available targets:"
	@echo "  make install  - Install dependencies"
	@echo "  make dev      - Install development dependencies"
	@echo "  make format   - Format code with black"
	@echo "  make lint     - Run linters (flake8, mypy)"
	@echo "  make test     - Run tests with pytest"
	@echo "  make all      - Run format, lint, and test"
	@echo "  make clean    - Remove Python cache files"

# Install development dependencies
dev:
	pip install -e ".[dev]"

# Install production dependencies
install:
	pip install -r requirements.txt

format:
	black linux_mcp_agent/ tests/

lint:
	flake8 linux_mcp_agent/ tests/ --max-line-length=100 --extend-ignore=E501
	mypy linux_mcp_agent/ --ignore-missing-imports

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
