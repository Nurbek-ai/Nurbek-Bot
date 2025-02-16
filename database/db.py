# database/db.py
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base  # Import the Base and models
from config import settings  # Import settings (including the database URL)

log = logging.getLogger(__name__)

# Database URL from settings
DATABASE_URL = settings.DATABASE_URL

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create the database tables (if they don't exist)
Base.metadata.create_all(engine)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Example functions for database interaction:
def create_task(db, user_id, description, due_date):
    """Creates a new task in the database."""
    from database.models import Task  # Import Task model inside the function to avoid circular import issues
    task = Task(user_id=user_id, description=description, due_date=due_date)
    db.add(task)
    db.commit()
    db.refresh(task)  # Refresh to get the generated ID
    return task


def get_tasks_for_user(db, user_id):
    """Gets all tasks for a given user."""
    from database.models import Task  # Import Task model inside the function to avoid circular import issues
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks


def save_chat_history(db, user_id, message, response):
    """Saves the chat history to the database."""
    from database.models import ChatHistory  # Import ChatHistory model to avoid circular import issues
    history_entry = ChatHistory(user_id=user_id, message=message, response=response)
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)
    return history_entry