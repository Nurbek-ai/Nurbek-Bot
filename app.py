# app.py
import logging
import os

from bot import main  # Import the bot's main module
from config import settings  # Import settings
from utils import logger

# Configure logging (using the logger.py module)
logger.setup_logging()
log = logging.getLogger(__name__)


def main_app():
    """Main function to start the bot."""
    try:
        main.main()  # Start the Telegram bot
    except Exception as e:
        log.exception("An error occurred during bot startup: %s", e)
        print(f"Error during startup: {e}")  # Print to console for immediate visibility


if __name__ == "__main__":
    main_app()