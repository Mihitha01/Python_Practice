import random
import time

# --- INTRO ---
print("🎮 Welcome to ROCK • PAPER • SCISSORS — ARENA EDITION!")
player_name = input("Enter your name, warrior: ").strip() or "Player"
print(f"\n⚔️ Welcome {player_name}! Prepare for battle.\n")

# --- SETTINGS ---
choices = ["rock", "paper", "scissors"]
score = {"player": 0, "computer": 0}
player_history = []
rounds_played = 0

# Choose match length
while True:
    try:
        max_score = int(input("Play best of how many points? (e.g., 3, 5, or 7): "))
        if max_score > 0:
            break
        else:
            print("Please enter a positive number.")
    except ValueError:
        print("Enter a valid number!")

# --- FUNCTIONS ---
def computer_choice():
    # Smarter adaptive AI: predicts your frequent move and counters it
    if not player_history:
        return random.choice(choices)
    most_common = max(set(player_history), key=player_history.count)
    if most_common == "rock":
        return "paper"
    elif most_common == "paper":
        return "scissors"
    else:
        return "rock"

def display_loading(text="Computer is thinking"):
    print(text, end="", flush=True)
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()

def show_score():
    print(f"\n🏆 SCOREBOARD — {player_name}: {score['player']} | Computer: {score['computer']}\n")

def battle_emoji(move):
    return {"rock": "🪨", "paper": "📜", "scissors": "✂️"}[move]

# --- MAIN LOOP ---
while True:
    player = input("Choose (rock / paper / scissors) or 'quit': ").lower()

    if player == "quit":
        print("\n👋 Exiting the arena...")
        break

    if player not in choices:
        print("❌ Invalid choice! Try again.")
        continue

    comp = computer_choice()
    player_history.append(player)
    rounds_played += 1

    display_loading()
    print(f"{player_name} chose {battle_emoji(player)}  vs  🤖 Computer chose {battle_emoji(comp)}\n")

    # --- Outcome ---
    if player == comp:
        print("😐 It's a tie!")
    elif (player == "rock" and comp == "scissors") or \
         (player == "paper" and comp == "rock") or \
         (player == "scissors" and comp == "paper"):
        print("🔥 You won this round!")
        score["player"] += 1
    else:
        print("💥 Computer won this round!")
        score["computer"] += 1

    show_score()

    # --- End of Match Check ---
    if score["player"] == max_score:
        print(f"🎉 VICTORY! {player_name} wins the Arena Battle!")
        break
    elif score["computer"] == max_score:
        print("🤖 Computer reigns supreme! You have been defeated.")
        break

# --- STATS ---
if rounds_played > 0:
    win_rate = (score["player"] / rounds_played) * 100
    print(f"\n📊 Game Stats — Rounds Played: {rounds_played}")
    print(f"✅ Wins: {score['player']}, ❌ Losses: {score['computer']}, 😐 Draws: {rounds_played - (score['player'] + score['computer'])}")
    print(f"🎯 Win Rate: {win_rate:.1f}%")

# --- Rematch Option ---
choice = input("\nWould you like to play again? (yes/no): ").lower()
if choice.startswith("y"):
    print("\nRestart the script to challenge the computer again! ⚡")
else:
    print("\nThanks for playing, warrior! 👑")
