import time
import sys
import random

def show_help():
    print("""
==================== 🚘 HELP MENU ====================
  start   - start the car
  stop    - stop the car
  status  - check car condition
  drive   - go for a drive
  refuel  - fill up the tank
  repair  - fix the car if it's broken
  help    - show this help menu
  quit    - exit the simulator
======================================================
""")


def loading_animation(text, duration=2, dots=3):
    print(text, end="")
    for _ in range(dots):
        sys.stdout.flush()
        time.sleep(duration / dots)
        print(".", end="")
    print("\n")


def car_engine_sound():
    for sound in ["Vroom", "Vrooooom", "VROOOOOM!!!"]:
        print(sound)
        time.sleep(0.4)


def random_event():
    """Returns a random driving event."""
    events = [
        ("🌧️ It started raining. Visibility is low!", -5, 0),
        ("🚨 Police checkpoint ahead. You slow down.", -2, 0),
        ("🚦 Traffic jam! You waste fuel idling.", -3, 5),
        ("🔥 Engine getting hot! Temperature rising.", 0, 15),
        ("💨 Smooth road ahead — you cruise comfortably.", -4, -5),
        ("🐦 A bird almost hit your windshield!", -1, 0),
    ]
    return random.choice(events)


def go_for_drive(car):
    """Simulate a driving session with random events."""
    if not car["started"]:
        print("🚫 You need to start the car first!")
        return
    if car["broken"]:
        print("🧰 The car is broken! Repair it before driving.")
        return
    if car["fuel"] <= 0:
        print("⛽ No fuel left! You can’t drive.")
        return

    print("\n🚗 You hit the road...")
    for i in range(random.randint(2, 4)):
        event, fuel_loss, temp_gain = random_event()
        loading_animation(event, 1.5)
        car["fuel"] = max(0, car["fuel"] + fuel_loss)
        car["temperature"] += temp_gain

        if car["fuel"] <= 0:
            print("💀 You ran out of fuel on the road!")
            car["started"] = False
            break
        if car["temperature"] >= 100:
            print("🔥 The engine overheated! The car broke down.")
            car["broken"] = True
            car["started"] = False
            break

        time.sleep(1)

    if not car["broken"] and car["fuel"] > 0:
        print("🅿️ You safely return home after your drive!\n")


def show_status(car):
    print(f"""
================== 🚘 CAR STATUS ==================
  Engine:      {'Running' if car['started'] else 'Stopped'}
  Fuel Level:  {car['fuel']}%
  Temperature: {car['temperature']}°C
  Condition:   {'Broken 😢' if car['broken'] else 'Good 👍'}
===================================================
""")


def main():
    car = {
        "started": False,
        "fuel": 100,
        "temperature": 25,
        "broken": False
    }

    print("==============================================")
    print("🏎️ Welcome to *Car Simulator 2.0 – The Adventure!*")
    print("==============================================")
    print("Type 'help' to see all commands.\n")

    while True:
        command = input("> ").strip().lower()

        if command == "start":
            if car["broken"]:
                print("🚫 The car is broken! Repair it first.")
            elif car["started"]:
                print("⚠️  Car is already running!")
            elif car["fuel"] <= 0:
                print("⛽ The tank is empty. Refuel first!")
            else:
                loading_animation("🔑 Turning the key", 1.5)
                print("💨 Engine roaring to life...")
                car_engine_sound()
                car["started"] = True
                print("✅ Car started successfully!")
        elif command == "stop":
            if not car["started"]:
                print("⚠️  Car is already stopped.")
            else:
                loading_animation("🛑 Shutting down engine", 1.5)
                car["started"] = False
                print("💤 Car is now stopped.")
        elif command == "drive":
            go_for_drive(car)
        elif command == "refuel":
            if car["fuel"] == 100:
                print("⛽ Tank already full!")
            else:
                loading_animation("⛽ Refueling", 2)
                car["fuel"] = 100
                print("✅ Tank is now full!")
        elif command == "repair":
            if not car["broken"]:
                print("🔧 Car is already in good condition!")
            else:
                loading_animation("🔧 Repairing the car", 3)
                car["broken"] = False
                car["temperature"] = 25
                print("✅ Car repaired and ready to go!")
        elif command == "status":
            show_status(car)
        elif command == "help":
            show_help()
        elif command == "quit":
            print("\n👋 Exiting Car Simulator 2.0...")
            time.sleep(1)
            print("Thanks for playing! Drive safe! 🚦")
            break
        elif command == "":
            print("⚙️  Type something! Need help? Type 'help'.")
        else:
            print("❌ Unknown command. Type 'help' for a list of commands.")


if __name__ == "__main__":
    main()
