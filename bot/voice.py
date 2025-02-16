# bot/voice.py
import logging
import speech_recognition as sr

log = logging.getLogger(__name__)

def transcribe_audio(audio_file_path):
    """
    Transcribes audio from a file using the speech_recognition library.

    Args:
        audio_file_path: The path to the audio file.

    Returns:
        The transcribed text, or None if transcription fails.
    """
    try:
        r = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio = r.record(source)  # Read the entire audio file

        text = r.recognize_google(audio)  # Use Google Web Speech API for recognition
        log.info(f"Transcribed audio: {text}")
        return text
    except sr.UnknownValueError:
        log.error("Could not understand audio")
        return None
    except sr.RequestError as e:
        log.error(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except Exception as e:
        log.exception(f"Error transcribing audio: {e}")
        return None

# Example usage (assuming you receive an audio file from Telegram):
# audio_file_path = 'path/to/received/audio.wav'
# transcribed_text = transcribe_audio(audio_file_path)
# if transcribed_text:
#     # Send the transcribed text to handlers.py for processing with Gemini
#     response_text = await handlers.process_message(transcribed_text)
#     # Send the response back to the user