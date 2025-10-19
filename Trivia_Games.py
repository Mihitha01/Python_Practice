import random

# Dictionary of questions and answers
questions = {
    "What is the keyword to define a function in Python?": "def",
    "Which data type is used to store True or False values?": "boolean",
    "What is the correct file extension for Python files?": ".py",
    "Which symbol is used to comment in Python?": "#",
    "What function is used to get input from the user?": "input",
    "How do you start a for loop in Python?": "for",
    "What is the output of 2 ** 3 in Python?": "8",
    "What keyword is used to import a module in Python?": "import",
    "What does the len() function return?": "length",
    "What is the result of 10 // 3 in Python?": "3"
}

def python_trivia_game():
    questions_list = list(questions.keys())
    total_questions = 5  # Number of questions per game
    score = 0

    # Randomly select questions
    selected_questions = random.sample(questions_list, total_questions)

    for idx, question in enumerate(selected_questions):
        print(f"\nQuestion {idx + 1}: {question}")
        user_answer = input("Your answer: ").strip().lower()
        correct_answer = questions[question].lower()

        if user_answer == correct_answer:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer is '{questions[question]}'.")

    print(f"\nGame Over! Your final score is {score}/{total_questions}.")

# Start the game
if __name__ == "__main__":
    python_trivia_game()
