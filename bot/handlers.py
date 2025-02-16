# bot/handlers.py
import logging
import os

import google.generativeai as genai
from telegram import Update
from telegram.ext import CallbackContext

from config import settings  # Import settings (including the Gemini API key)
import json  # Import the json module

log = logging.getLogger(__name__)


async def process_message(message_text: str, update: Update, context: CallbackContext) -> str:
    # (Existing process_message function - leave it as is)
    # ...
    pass


def generate_quiz_questions(topic: str, num_questions: int = 5):
    """
    Generates multiple-choice quiz questions about a topic using the Gemini API.

    Args:
        topic: The topic of the quiz.
        num_questions: The number of questions to generate.

    Returns:
        A list of dictionaries, where each dictionary represents a question.
        Returns None if there is an error.
    """
    try:
        gemini_api_key = settings.GEMINI_API_KEY
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"Generate {num_questions} multiple-choice quiz questions about {topic}.  For each question, provide the question text, four answer options, and the correct answer. Format the output as a JSON list of dictionaries, where each dictionary has the following keys: 'question', 'options' (a list of strings), and 'correct_answer'."
        log.info(f"Sending quiz generation request to Gemini: {prompt}")
        response = model.generate_content(prompt)

        log.info(f"Received quiz generation response from Gemini: {response.text}")

        # Attempt to parse the JSON response
        try:
            questions = json.loads(response.text)  # Parse the JSON string
            if not isinstance(questions, list):  # Verify is list
              raise ValueError("Gemini's response is not a valid JSON list.")
            for question in questions: # Verify structure of each element
              if not isinstance(question, dict) or not all(key in question for key in ('question','options','correct_answer')) or not isinstance(question['options'], list):
                raise ValueError("Incorrect format: each quiz should be a dictionary with keys 'question', 'options', 'correct_answer' and 'options' value should be a list ")
            return questions  # Return the parsed questions

        except json.JSONDecodeError as e:
            log.error(f"Failed to decode JSON from Gemini: {e}")
            return None
        except ValueError as e:
            log.error(f"Gemini returned incorrectly formatted data: {e}")
            return None

    except Exception as e:
        log.exception(f"Error generating quiz questions: {e}")
        return None


async def start_quiz(update: Update, context: CallbackContext):
    """Handles the /quiz command."""
    chat_id = update.effective_chat.id
    try:
        topic = context.args[0]  # Get the topic from the command arguments
        num_questions = 5 # Setting Default
        if len(context.args) > 1:
            num_questions = int(context.args[1]) # get the optional parameter of number of questions
        # Generate the quiz questions
        questions = generate_quiz_questions(topic, num_questions)

        if questions:
            # Create a Quiz object
            from bot.quiz import Quiz  # Import the Quiz class here to avoid circular import issues
            quiz = Quiz(questions)

            # Store the Quiz object in the context for this user (chat_id)
            context.chat_data['quiz'] = quiz
            context.chat_data['current_question_index'] = 0  # Start from the first question
            # Get the first question
            current_question = quiz.get_current_question()

            # Format the question and options for display
            question_text = current_question['question']
            options_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(current_question['options'])])

            # Send the question to the user
            await context.bot.send_message(chat_id=chat_id, text=f"{question_text}\n{options_text}")
            # Update the state to show user it's waiting for input. This is a placeholder
            await context.bot.send_message(chat_id=chat_id, text="Please enter the number of your answer (1-4).")
        else:
            await context.bot.send_message(chat_id=chat_id, text="Failed to generate quiz questions. Please try again later.")

    except (IndexError, ValueError):
        await context.bot.send_message(chat_id=chat_id, text="Usage: /quiz <topic> [number of questions]")
    except Exception as e:
        log.exception(f"Error starting quiz: {e}")
        await context.bot.send_message(chat_id=chat_id, text="An error occurred while starting the quiz. Please try again later.")

async def handle_quiz_answer(update: Update, context: CallbackContext):
  """Handles the user's answer to a quiz question."""
  chat_id = update.effective_chat.id

  if 'quiz' not in context.chat_data:
      await context.bot.send_message(chat_id=chat_id, text="There is no active quiz.")
      return

  quiz = context.chat_data['quiz']
  current_question_index = context.chat_data['current_question_index']
  try:
      answer = int(update.message.text) -1 # getting the array index from number 1-4
      if answer < 0 or answer > 3:
        raise ValueError("Choice out of scope") # out of index cases

      is_correct = quiz.check_answer(quiz.get_current_question()['options'][answer]) # Check based on the selected option

      if is_correct:
          await context.bot.send_message(chat_id=chat_id, text="Correct!")
      else:
          await context.bot.send_message(chat_id=chat_id,
                                        text=f"Incorrect. The correct answer was: {quiz.get_current_question()['correct_answer']}")

      # Move to the next question
      quiz.next_question()
      context.chat_data['current_question_index'] += 1
      if quiz.is_finished():
          score = quiz.get_score()
          await context.bot.send_message(chat_id=chat_id, text=f"Quiz finished! Your score: {score}/{len(quiz.questions)}")
          del context.chat_data['quiz']  # Remove the quiz from the context

      else:
        current_question = quiz.get_current_question()

        # Format the question and options for display
        question_text = current_question['question']
        options_text = "\n".join([f"{i + 1}. {option}" for i, option in enumerate(current_question['options'])])

        # Send the question to the user
        await context.bot.send_message(chat_id=chat_id, text=f"{question_text}\n{options_text}")
        # Update the state to show user it's waiting for input. This is a placeholder
        await context.bot.send_message(chat_id=chat_id, text="Please enter the number of your answer (1-4).")

  except ValueError as e:
      await context.bot.send_message(chat_id=chat_id, text=f"Invalid Input. Please enter a number between 1-4 {e}")
  except Exception as e:
      log.exception(f"Error handling quiz answer: {e}")
      await context.bot.send_message(chat_id=chat_id, text="An error occurred. Please try again.")