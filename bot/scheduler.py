# bot/scheduler.py
import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import CallbackContext

log = logging.getLogger(__name__)

scheduler = BackgroundScheduler()  # Create a background scheduler

async def send_reminder(context: CallbackContext):
    """Sends a reminder message."""
    job = context.job
    chat_id = job.chat_id  # Get the chat ID from the job's context
    text = job.data['text']  # Get the reminder text from the job's data
    try:
        await context.bot.send_message(chat_id=chat_id, text=f"Reminder: {text}")
    except Exception as e:
        log.error(f"Failed to send reminder to chat {chat_id}: {e}")

async def set_timer(update: Update, context: CallbackContext):
    """Sets a timer for a reminder."""
    chat_id = update.effective_chat.id
    try:
        # Extract time and text from the command arguments
        # Example command: /timer 5 Reminder text
        due = int(context.args[0])
        if due < 0:
            await update.effective_message.reply_text("Sorry, I can't go back to the future!")
            return

        text = ' '.join(context.args[1:])
        if not text:
            await update.effective_message.reply_text("Reminder text is missing.")
            return

        # Calculate the due time
        due_time = datetime.now() + timedelta(seconds=due)

        # Add the job to the scheduler
        context.job_queue.run_once(send_reminder, due, chat_id=chat_id, data={'text':text})

        await update.effective_message.reply_text(
            f"Reminder set! You will be reminded in {due} seconds."
        )

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /timer <seconds> <reminder_text>")

def start_scheduler(application):
    """Starts the scheduler."""
    application.job_queue.scheduler.start()
    log.info("Scheduler started")

def stop_scheduler(application):
    """Stops the scheduler."""
    application.job_queue.scheduler.shutdown()
    log.info("Scheduler stopped")