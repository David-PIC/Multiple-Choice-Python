import json
import random

QUESTIONS_FILE = 'questions.json'
MAX_ATTEMPTS = 3

def load_questions():
    try:
        with open(QUESTIONS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def get_random_question(questions):
    available_questions = [q for q in questions if isinstance(q, dict) and q.get('attempts', 0) < MAX_ATTEMPTS]
    if not available_questions:
        return None
    question = random.choice(available_questions)
    return question

def ask_question(question):
    print(question['question'])
    for i, option in enumerate(question['options']):
        print(f"{chr(i + 97)}) {option}")
    answer = input('Your answer (a, b, c or d): ').strip().lower()
    if answer == question['answer'].lower():
        print('Correct!')
        question['attempts'] = question.get('attempts', 0) + 1
        if question['attempts'] == MAX_ATTEMPTS:
            print('You have answered this question correctly 3 times. It will be removed from the question pool.')
    else:
        print(f'Incorrect. The correct answer is {question["answer"].upper()}.')
        question.pop('attempts', None)
    return question

def main():
    questions = load_questions()
    while True:
        question = get_random_question(questions)
        if not question:
            print('You have answered all available questions correctly 3 times. There are no more questions left.')
            break
        question = ask_question(question)
        answer = question['options'][ord(question['answer'].lower()) - 97]
        print(f'The correct answer was: {answer}')
        print('')

if __name__ == '__main__':
    main()