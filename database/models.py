# database/models.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from config import settings  # Import settings (including the database URL)

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)  # Telegram user ID
    description = Column(String)
    due_date = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Task(description='{self.description}', due_date='{self.due_date}')>"


class User(Base):  # Example: Store user-specific data
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)  # Store Telegram user ID
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    # Add other user-related fields as needed (e.g., preferred language)

    def __repr__(self):
        return f"<User(username='{self.username}')>"


class ChatHistory(Base):  # Example: Store conversation history
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)  # Telegram user ID
    message = Column(String)
    response = Column(String)
    timestamp = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<ChatHistory(message='{self.message[:50]}...', response='{self.response[:50]}...')>"