# utils/helpers.py
import re
from datetime import datetime

def format_date(date_obj):
    """Formats a datetime object into a user-friendly string."""
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")

def validate_email(email):
    """Validates an email address using a regular expression."""
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None

# Add other utility functions as needed