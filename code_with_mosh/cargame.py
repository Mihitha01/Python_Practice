import time
import sys
import random

def show_help():
    print("""
==================== 🚘 HELP MENU ====================
  start   - to start the car
  stop    - to stop the car
  status  - to check the car's status
  rev     - to rev the engine
  drive   - to go for a short drive
  help    - to show this help menu
  quit    - to exit the game
======================================================
""")


def loading_animation(text, duration=2, dots=3):
    """Creates a little loading animation for realism."""
    print(text, end="")
    for _ in range(dots):
        sys.stdout.flush()
        time.sleep(duration / dots)
        print(".", end="")
    print("\n")


def car_engine_sound():
    """Simulate a car rev sound with text."""
    for sound in ["Vroom", "Vrooooom", "VROOOOOM!!!"]:
        print(sound)
        time.sleep(0.4)


def go_for_drive():
    """Simulate a mini driving sequence."""
    print("\n🚗 Starting your drive...")
    for scene in ["Leaving the driveway", "Cruising down the road", "Turning the corner", "Heading back home"]:
        loading_animation(f"🏁 {scene}", duration=1.5)
    print("🅿️  You parked safely back home!\n")


def main():
    started = False
    print("==============================================")
    print("🚘 Welcome to the *Ultimate Car Simulator*! 🏎️")
    print("==============================================")
    print("Type 'help' to see available commands.\n")

    while True:
        command = input("> ").strip().lower()

        if command == "start":
            if started:
                print("⚠️  Car is already running!")
            else:
                loading_animation("🔑 Turning the key", 1.5)
                print("💨 Engine roaring to life...")
                car_engine_sound()
                started = True
                print("✅ Car started successfully!")
        elif command == "stop":
            if not started:
                print("⚠️  Car is already stopped.")
            else:
                loading_animation("🛑 Shutting down engine", 1.5)
                started = False
                print("💤 Car is now stopped.")
        elif command == "rev":
            if not started:
                print("🚫 You need to start the car first!")
            else:
                car_engine_sound()
        elif command == "drive":
            if not started:
                print("🚫 The car is off! Start it first.")
            else:
                go_for_drive()
        elif command == "status":
            print(f"📊 Car status: {'Running' if started else 'Stopped'}")
        elif command == "help":
            show_help()
        elif command == "quit":
            print("\n👋 Exiting the Car Simulator...")
            time.sleep(1)
            print("Thanks for playing! Drive safe! 🚦")
            break
        elif command == "":
            print("⚙️  Type something! Need help? Type 'help'.")
        else:
            print("❌ Unknown command. Type 'help' for a list of commands.")


if __name__ == "__main__":
    main()
