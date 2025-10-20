import random
import time
from colorama import Fore, Style, init

init(autoreset=True)

# Questions with categories and difficulty
questions = [
    {"question": "What is the keyword to define a function in Python?", "answer": "def", "category": "Functions", "difficulty": "Easy"},
    {"question": "Which data type is used to store True or False values?", "answer": "boolean", "category": "Basics", "difficulty": "Easy"},
    {"question": "What is the correct file extension for Python files?", "answer": ".py", "category": "Basics", "difficulty": "Easy"},
    {"question": "Which symbol is used to comment in Python?", "answer": "#", "category": "Basics", "difficulty": "Easy"},
    {"question": "What function is used to get input from the user?", "answer": "input", "category": "Functions", "difficulty": "Easy"},
    {"question": "How do you start a for loop in Python?", "answer": "for", "category": "Loops", "difficulty": "Easy"},
    {"question": "What is the output of 2 ** 3 in Python?", "answer": "8", "category": "Operators", "difficulty": "Easy"},
    {"question": "What keyword is used to import a module in Python?", "answer": "import", "category": "Modules", "difficulty": "Medium"},
    {"question": "What does the len() function return?", "answer": "length", "category": "Functions", "difficulty": "Medium"},
    {"question": "What is the result of 10 // 3 in Python?", "answer": "3", "category": "Operators", "difficulty": "Medium"},
    {"question": "What keyword is used to define a class in Python?", "answer": "class", "category": "OOP", "difficulty": "Medium"},
    {"question": "What is a correct syntax to inherit a class in Python?", "answer": "class Child(Parent):", "category": "OOP", "difficulty": "Hard"},
    {"question": "What built-in function returns the memory address of an object?", "answer": "id", "category": "Functions", "difficulty": "Hard"},
    {"question": "Which module in Python is used for regular expressions?", "answer": "re", "category": "Modules", "difficulty": "Hard"},
]

def display_progress(current, total):
    bar_length = 20
    filled_length = int(bar_length * current // total)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    print(f"\rProgress: |{bar}| {current}/{total} questions", end="\r")

def python_trivia_game():
    print(Fore.CYAN + Style.BRIGHT + "\n===== Welcome to the Python Trivia Game! =====\n")
    print(Fore.YELLOW + "Select difficulty: Easy | Medium | Hard")
    difficulty = input("Your choice: ").capitalize().strip()
    print()

    # Filter questions by difficulty
    available_questions = [q for q in questions if q["difficulty"] == difficulty] or questions

    total_questions = 5
    score = 0
    streak = 0

    selected_questions = random.sample(available_questions, min(total_questions, len(available_questions)))

    start_time = time.time()

    for idx, q in enumerate(selected_questions, 1):
        print(Fore.MAGENTA + f"\nQuestion {idx}: {q['question']}")
        print(Fore.CYAN + f"Category: {q['category']}  |  Difficulty: {q['difficulty']}")

        user_answer = input("Your answer: ").strip().lower()
        correct_answer = q["answer"].lower()

        if user_answer == correct_answer:
            print(Fore.GREEN + "✅ Correct!")
            score += 1
            streak += 1
        else:
            print(Fore.RED + f"❌ Wrong! The correct answer is '{q['answer']}'.")
            streak = 0

        display_progress(idx, total_questions)
        time.sleep(0.8)  # just for animation effect

    end_time = time.time()
    total_time = round(end_time - start_time, 2)
    accuracy = (score / total_questions) * 100

    print(Fore.CYAN + "\n\n===== Game Over =====")
    print(Fore.YELLOW + f"Final Score: {score}/{total_questions}")
    print(Fore.YELLOW + f"Accuracy: {accuracy:.1f}%")
    print(Fore.YELLOW + f"Time Taken: {total_time} seconds")

    if streak >= 3:
        print(Fore.GREEN + f"🔥 Impressive! You had a {streak}-question streak!")

    print(Fore.CYAN + "\nThanks for playing!")
    replay = input("\nDo you want to play again? (y/n): ").lower().strip()
    if replay == "y":
        python_trivia_game()

if __name__ == "__main__":
    python_trivia_game()
