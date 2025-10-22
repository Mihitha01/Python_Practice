import random
import time

print("🎮 Welcome to Rock, Paper, Scissors Battle!")
print("First to 5 points wins the match!\n")

choices = ["rock", "paper", "scissors"]
score = {"player": 0, "computer": 0}
player_history = []

def computer_choice():
    # Simple adaptive AI — computer tries to counter your frequent moves
    if not player_history:
        return random.choice(choices)
    most_common = max(set(player_history), key=player_history.count)
    if most_common == "rock":
        return "paper"
    elif most_common == "paper":
        return "scissors"
    else:
        return "rock"

def print_scores():
    print(f"\n🏆 Score — You: {score['player']} | Computer: {score['computer']}\n")

while True:
    player = input("Enter Rock, Paper, or Scissors (or 'quit' to stop): ").lower()

    if player == "quit":
        print("👋 Thanks for playing!")
        break

    if player not in choices:
        print("❌ Invalid choice, try again!")
        continue

    comp = computer_choice()
    player_history.append(player)

    print("Computer is choosing", end="")
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print(f" 🤖 {comp.capitalize()}!\n")

    if player == comp:
        print("😐 It's a tie!")
    elif (player == "rock" and comp == "scissors") or \
         (player == "paper" and comp == "rock") or \
         (player == "scissors" and comp == "paper"):
        print("✅ You win this round!")
        score["player"] += 1
    else:
        print("💥 Computer wins this round!")
        score["computer"] += 1

    print_scores()

    if score["player"] == 5:
        print("🎉 You defeated the computer! Champion!")
        break
    elif score["computer"] == 5:
        print("🤖 Computer wins the match! Try again next time.")
        break
