# config/dev.py

from .base import Config
import os

class DevConfig(Config):
    DEBUG = True
    # You can override just DEV-specific vars if needed
    # DB_URL = os.getenv("DEV_DB_URL", Config.DB_URL)
