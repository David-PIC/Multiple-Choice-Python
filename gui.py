import json
import random
import tkinter as tk
from tkinter import messagebox


QUESTIONS_FILE = 'questions.json'
MAX_ATTEMPTS = 3

def load_questions():
    try:
        with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
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
    root = tk.Tk()
    root.tk.call('encoding', 'system', 'utf-8')
    root.title(question['question'])
    root.geometry('800x800')
    root.attributes('-fullscreen', True)
    
    question_label = tk.Label(root, text=question['question'], font=('Arial', 14))
    question_label.pack(side='top', padx=10, pady=10)
    
    options_frame = tk.Frame(root)
    options_frame.pack(pady=30, anchor="center")
    
    for i, option in enumerate(question['options']):
        button = tk.Button(options_frame, text=option, font=('Arial', 12), command=lambda idx=i: check_answer(question, idx, root))
        button.pack(pady=5)
        
    root.mainloop()

def check_answer(question, idx, root):
    answer = chr(idx + 97).upper()
    if answer == question['answer']:
        result = 'Correct!'
        question['attempts'] = question.get('attempts', 0) + 1
        if question['attempts'] == MAX_ATTEMPTS:
            result += ' You have answered this question correctly {} times. It will be removed from the question pool.'.format(MAX_ATTEMPTS)
    else:
        result = f'Incorrect. The correct answer is {question["answer"]}.'
    tk.messagebox.showinfo(title='Result', message=result)
    root.destroy()
    
def main():
    questions = load_questions()
    while True:
        question = get_random_question(questions)
        if not question:
            print('You have answered all available questions correctly 3 times. There are no more questions left.')
            break
        ask_question(question)

if __name__ == '__main__':
    main()
