"""Configuration settings for the application."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
STORAGE_DIR = PROJECT_ROOT / "storage"
LOGS_DIR = PROJECT_ROOT / "logs"

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Application settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# LlamaIndex settings
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 20
EMBED_MODEL = "text-embedding-ada-002"
LLM_MODEL = "gpt-3.5-turbo"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
STORAGE_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
