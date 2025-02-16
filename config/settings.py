# config/settings.py
import os
from dotenv import load_dotenv
import logging

log = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get Telegram token from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    log.warning("TELEGRAM_TOKEN not found in environment variables.  Bot will likely fail to start.")

# Get Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    log.warning("GEMINI_API_KEY not found in environment variables.  Gemini integration will not work.")

# Database settings (example)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./smart_bot.db")  # Default to SQLite

# Other settings can be added here as needed