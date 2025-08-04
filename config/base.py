# config/base.py

import os
from dotenv import load_dotenv

# Load variables from .env at project root
load_dotenv()

class Config:
    """Base configuration."""
    # Environment: dev or prod
    REFLEX_ENV = os.getenv("REFLEX_ENV", "dev")

    # Database URL (fallback to SQLite for local dev)
    # DB_URL = os.getenv("DB_URL", f"sqlite:///data/{REFLEX_ENV}.db")

    # Add other shared settings here:
    # SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
