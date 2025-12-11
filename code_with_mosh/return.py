def square(number: float) -> float:
    return number * number

def add(number: float) -> float:
    return number + number

def div(number: float) -> float:
    if number == 0:
        return "Error: Cannot divide by zero."
    return number / number

def calculate(choice: str, value: float):
    if choice == "1":
        return square(value)
    elif choice == "2":
        return add(value)
    elif choice == "3":
        return div(value)
    else:
        return "Invalid choice."

def main():
    print("=== Simple Math Utility ===")
    print("1. Square a number")
    print("2. Double a number")
    print("3. Divide a number by itself")

    choice = input("Enter your choice (1/2/3): ").strip()

    try:
        value = float(input("Enter a number: "))
    except ValueError:
        print("Invalid number.")
        return

    result = calculate(choice, value)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
