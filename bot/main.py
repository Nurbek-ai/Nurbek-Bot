# bot/main.py
import logging
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

from config import settings  # Import settings (including the Telegram bot token)
from bot import handlers

# Configure logging
log = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext):
    """Handles the /start command."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your Smart Bot.  Ask me anything!")


async def handle_message(update: Update, context: CallbackContext):
    """Handles general text messages."""
    message_text = update.message.text
    log.info(f"Received message: {message_text} from {update.effective_user.username}")

    # Call the handler function to process the message and get a response
    response_text = await handlers.process_message(message_text, update, context)  # Await the async function

    # Send the response back to the user
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)



def main():
    """Main function to start the bot."""
    TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN  # Access the token from settings
    if not TELEGRAM_TOKEN:
        log.error("Telegram token not found in environment variables.")
        print("Error: Telegram token not found.  Set the TELEGRAM_TOKEN environment variable.")
        return

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Register command handlers
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Add the quiz command handler
    quiz_handler = CommandHandler('quiz', handlers.start_quiz)
    application.add_handler(quiz_handler)

    # Add handler to handle the number options by user after the quiz begins.
    quiz_answer_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handlers.handle_quiz_answer)
    application.add_handler(quiz_answer_handler)

    # Register message handler (for all other text messages)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)

    # Start the bot
    try:
        application.run_polling()
    except Exception as e:
        log.exception("An error occurred while running the bot: %s", e)
        print(f"Error running bot: {e}")


if __name__ == '__main__':
    main()