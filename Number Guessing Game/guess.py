import random

number_to_guess = random.randint(1,100)
attempts = 0;
user_guess = 0;

print("Welcome to the Number Guessing Game!")
print("I'm thinking of a Number between 1 and 100...")

while(user_guess != number_to_guess):
    user_guess = int(input("Enter Your Guess : "))
    attempts += 1

    


