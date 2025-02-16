# bot/quiz.py
import logging
import random

log = logging.getLogger(__name__)


class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.current_question_index = 0
        self.score = 0

    def get_current_question(self):
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        else:
            return None  # Quiz is finished

    def check_answer(self, answer):
        current_question = self.get_current_question()
        if current_question and answer.lower() == current_question['correct_answer'].lower():
            self.score += 1
            return True
        return False

    def next_question(self):
        self.current_question_index += 1

    def is_finished(self):
        return self.current_question_index >= len(self.questions)

    def get_score(self):
        return self.score

# Example usage (you'll likely load questions from a database or file):
sample_questions = [
    {
        'question': 'What is the capital of France?',
        'options': ['Paris', 'London', 'Berlin', 'Rome'],
        'correct_answer': 'Paris'
    },
    {
        'question': 'What is 2 + 2?',
        'options': ['3', '4', '5', '6'],
        'correct_answer': '4'
    }
]

# Example of how you might start a quiz:
# quiz = Quiz(sample_questions)
# current_question = quiz.get_current_question()
# print(current_question['question']) # Send this to the user in Telegram