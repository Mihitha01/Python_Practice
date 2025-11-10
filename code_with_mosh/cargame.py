def show_help():
    print("""
Available commands:
  start - to start the car
  stop  - to stop the car
  status - to check car status
  help  - to show this help message
  quit  - to exit the game
    """)


def main():
    command = ""
    started = False

    print("🚘 Welcome to the Car Game! Type 'help' to see available commands.")

    while True:
        command = input("> ").strip().lower()

        if command == "start":
            if started:
                print("⚠️ Car is already started!")
            else:
                started = True
                print("✅ Car started... Ready to go!")
        elif command == "stop":
            if not started:
                print("⚠️ Car is already stopped!")
            else:
                started = False
                print("🛑 Car stopped.")
        elif command == "status":
            print(f"🚗 The car is currently {'running' if started else 'stopped'}.")
        elif command == "help":
            show_help()
        elif command == "quit":
            print("👋 Exiting the game... Goodbye!")
            break
        elif command == "":
            print("⚙️ Please type a command. Type 'help' if you’re not sure what to do.")
        else:
            print("❌ Invalid command. Type 'help' for a list of valid commands.")


if __name__ == "__main__":
    main()
