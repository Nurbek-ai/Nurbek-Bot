# bot/ocr.py
import logging
import pytesseract
from PIL import Image

log = logging.getLogger(__name__)

def extract_text_from_image(image_path):
    """
    Extracts text from an image using pytesseract.

    Args:
        image_path: The path to the image file.

    Returns:
        The extracted text, or None if extraction fails.
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        log.info(f"Extracted text from image: {text}")
        return text
    except FileNotFoundError:
        log.error(f"Image file not found: {image_path}")
        return None
    except Exception as e:
        log.exception(f"Error extracting text from image: {e}")
        return None

# Example usage (assuming you receive an image file from Telegram):
# image_file_path = 'path/to/received/image.jpg'
# extracted_text = extract_text_from_image(image_file_path)
# if extracted_text:
#     # Send the extracted text to handlers.py for processing with Gemini
#     response_text = await handlers.process_message(extracted_text)
#     # Send the response back to the user