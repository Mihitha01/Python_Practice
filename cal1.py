"""
Advanced Scientific Calculator in Python
Features:
- Basic arithmetic operations
- Scientific functions (sin, cos, tan, log, etc.)
- Memory operations (store, recall, clear)
- Calculation history
- Expression evaluation
- Unit conversions
- Statistical functions
- Number system conversions
"""

import math
import statistics
from datetime import datetime


class AdvancedCalculator:
    def __init__(self):
        self.memory = 0
        self.history = []
        self.last_result = 0
    
    # ==================== BASIC OPERATIONS ====================
    def add(self, x, y):
        return x + y
    
    def subtract(self, x, y):
        return x - y
    
    def multiply(self, x, y):
        return x * y
    
    def divide(self, x, y):
        if y == 0:
            raise ValueError("Error! Division by zero.")
        return x / y
    
    def modulus(self, x, y):
        if y == 0:
            raise ValueError("Error! Division by zero.")
        return x % y
    
    def power(self, x, y):
        return x ** y
    
    def floor_divide(self, x, y):
        if y == 0:
            raise ValueError("Error! Division by zero.")
        return x // y
    
    # ==================== SCIENTIFIC FUNCTIONS ====================
    def square_root(self, x):
        if x < 0:
            raise ValueError("Error! Cannot compute square root of negative number.")
        return math.sqrt(x)
    
    def cube_root(self, x):
        return x ** (1/3) if x >= 0 else -(-x) ** (1/3)
    
    def nth_root(self, x, n):
        if n == 0:
            raise ValueError("Error! Root index cannot be zero.")
        return x ** (1/n)
    
    def factorial(self, x):
        if x < 0 or not isinstance(x, int):
            raise ValueError("Error! Factorial requires non-negative integer.")
        return math.factorial(int(x))
    
    def absolute(self, x):
        return abs(x)
    
    def logarithm(self, x, base=10):
        if x <= 0:
            raise ValueError("Error! Logarithm requires positive number.")
        return math.log(x, base)
    
    def natural_log(self, x):
        if x <= 0:
            raise ValueError("Error! Natural log requires positive number.")
        return math.log(x)
    
    def exponential(self, x):
        return math.exp(x)
    
    # ==================== TRIGONOMETRIC FUNCTIONS ====================
    def sine(self, x, degrees=True):
        if degrees:
            x = math.radians(x)
        return math.sin(x)
    
    def cosine(self, x, degrees=True):
        if degrees:
            x = math.radians(x)
        return math.cos(x)
    
    def tangent(self, x, degrees=True):
        if degrees:
            x = math.radians(x)
        return math.tan(x)
    
    def arc_sine(self, x):
        if x < -1 or x > 1:
            raise ValueError("Error! Arc sine requires value between -1 and 1.")
        return math.degrees(math.asin(x))
    
    def arc_cosine(self, x):
        if x < -1 or x > 1:
            raise ValueError("Error! Arc cosine requires value between -1 and 1.")
        return math.degrees(math.acos(x))
    
    def arc_tangent(self, x):
        return math.degrees(math.atan(x))
    
    # ==================== HYPERBOLIC FUNCTIONS ====================
    def sinh(self, x):
        return math.sinh(x)
    
    def cosh(self, x):
        return math.cosh(x)
    
    def tanh(self, x):
        return math.tanh(x)
    
    # ==================== STATISTICAL FUNCTIONS ====================
    def mean(self, numbers):
        return statistics.mean(numbers)
    
    def median(self, numbers):
        return statistics.median(numbers)
    
    def mode(self, numbers):
        try:
            return statistics.mode(numbers)
        except statistics.StatisticsError:
            return "No unique mode"
    
    def std_dev(self, numbers):
        return statistics.stdev(numbers) if len(numbers) > 1 else 0
    
    def variance(self, numbers):
        return statistics.variance(numbers) if len(numbers) > 1 else 0
    
    def sum_list(self, numbers):
        return sum(numbers)
    
    # ==================== NUMBER SYSTEM CONVERSIONS ====================
    def decimal_to_binary(self, x):
        return bin(int(x))[2:]
    
    def decimal_to_octal(self, x):
        return oct(int(x))[2:]
    
    def decimal_to_hex(self, x):
        return hex(int(x))[2:].upper()
    
    def binary_to_decimal(self, binary_str):
        return int(binary_str, 2)
    
    def octal_to_decimal(self, octal_str):
        return int(octal_str, 8)
    
    def hex_to_decimal(self, hex_str):
        return int(hex_str, 16)
    
    # ==================== UNIT CONVERSIONS ====================
    def celsius_to_fahrenheit(self, c):
        return (c * 9/5) + 32
    
    def fahrenheit_to_celsius(self, f):
        return (f - 32) * 5/9
    
    def km_to_miles(self, km):
        return km * 0.621371
    
    def miles_to_km(self, miles):
        return miles * 1.60934
    
    def kg_to_pounds(self, kg):
        return kg * 2.20462
    
    def pounds_to_kg(self, pounds):
        return pounds * 0.453592
    
    def degrees_to_radians(self, degrees):
        return math.radians(degrees)
    
    def radians_to_degrees(self, radians):
        return math.degrees(radians)
    
    # ==================== MEMORY OPERATIONS ====================
    def memory_store(self, value):
        self.memory = value
        return f"Stored {value} in memory"
    
    def memory_recall(self):
        return self.memory
    
    def memory_clear(self):
        self.memory = 0
        return "Memory cleared"
    
    def memory_add(self, value):
        self.memory += value
        return f"Memory: {self.memory}"
    
    def memory_subtract(self, value):
        self.memory -= value
        return f"Memory: {self.memory}"
    
    # ==================== HISTORY OPERATIONS ====================
    def add_to_history(self, operation, result):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history.append(f"[{timestamp}] {operation} = {result}")
        self.last_result = result
    
    def show_history(self):
        if not self.history:
            return "No history available"
        return "\n".join(self.history[-10:])  # Show last 10 entries
    
    def clear_history(self):
        self.history = []
        return "History cleared"
    
    # ==================== EXPRESSION EVALUATION ====================
    def evaluate_expression(self, expression):
        """Safely evaluate mathematical expressions"""
        allowed_names = {
            'sin': lambda x: math.sin(math.radians(x)),
            'cos': lambda x: math.cos(math.radians(x)),
            'tan': lambda x: math.tan(math.radians(x)),
            'sqrt': math.sqrt,
            'log': math.log10,
            'ln': math.log,
            'exp': math.exp,
            'pi': math.pi,
            'e': math.e,
            'abs': abs,
            'pow': pow,
            'ans': self.last_result,
            'mem': self.memory
        }
        try:
            # Replace ^ with ** for power operations
            expression = expression.replace('^', '**')
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return result
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")
    
    # ==================== SPECIAL CALCULATIONS ====================
    def gcd(self, a, b):
        return math.gcd(int(a), int(b))
    
    def lcm(self, a, b):
        return abs(int(a) * int(b)) // math.gcd(int(a), int(b))
    
    def permutation(self, n, r):
        return math.perm(int(n), int(r))
    
    def combination(self, n, r):
        return math.comb(int(n), int(r))
    
    def percentage(self, value, percent):
        return (value * percent) / 100
    
    def percentage_change(self, old_value, new_value):
        if old_value == 0:
            raise ValueError("Error! Old value cannot be zero.")
        return ((new_value - old_value) / old_value) * 100
    
    def quadratic_solver(self, a, b, c):
        """Solve ax² + bx + c = 0"""
        if a == 0:
            raise ValueError("Coefficient 'a' cannot be zero for quadratic equation.")
        discriminant = b**2 - 4*a*c
        if discriminant > 0:
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            return (x1, x2)
        elif discriminant == 0:
            x = -b / (2*a)
            return (x,)
        else:
            real_part = -b / (2*a)
            imag_part = math.sqrt(abs(discriminant)) / (2*a)
            return (complex(real_part, imag_part), complex(real_part, -imag_part))


def print_menu():
    print("\n" + "="*60)
    print("          🧮 ADVANCED SCIENTIFIC CALCULATOR 🧮")
    print("="*60)
    print("""
┌─────────────────────────────────────────────────────────────┐
│  BASIC OPERATIONS                                           │
│  1.  Add (+)              2.  Subtract (-)                  │
│  3.  Multiply (×)         4.  Divide (÷)                    │
│  5.  Modulus (%)          6.  Power (^)                     │
│  7.  Floor Division (//)                                    │
├─────────────────────────────────────────────────────────────┤
│  SCIENTIFIC FUNCTIONS                                       │
│  10. Square Root (√)      11. Cube Root (∛)                 │
│  12. Nth Root             13. Factorial (n!)                │
│  14. Absolute Value       15. Log (base 10)                 │
│  16. Natural Log (ln)     17. Exponential (e^x)             │
├─────────────────────────────────────────────────────────────┤
│  TRIGONOMETRIC (degrees)                                    │
│  20. Sine                 21. Cosine                        │
│  22. Tangent              23. Arc Sine                      │
│  24. Arc Cosine           25. Arc Tangent                   │
│  26. Sinh                 27. Cosh                          │
│  28. Tanh                                                   │
├─────────────────────────────────────────────────────────────┤
│  STATISTICAL FUNCTIONS                                      │
│  30. Mean                 31. Median                        │
│  32. Mode                 33. Standard Deviation            │
│  34. Variance             35. Sum                           │
├─────────────────────────────────────────────────────────────┤
│  NUMBER CONVERSIONS                                         │
│  40. Decimal → Binary     41. Decimal → Octal               │
│  42. Decimal → Hex        43. Binary → Decimal              │
│  44. Octal → Decimal      45. Hex → Decimal                 │
├─────────────────────────────────────────────────────────────┤
│  UNIT CONVERSIONS                                           │
│  50. °C → °F              51. °F → °C                       │
│  52. Km → Miles           53. Miles → Km                    │
│  54. Kg → Pounds          55. Pounds → Kg                   │
│  56. Degrees → Radians    57. Radians → Degrees             │
├─────────────────────────────────────────────────────────────┤
│  SPECIAL CALCULATIONS                                       │
│  60. GCD                  61. LCM                           │
│  62. Permutation          63. Combination                   │
│  64. Percentage           65. Percentage Change             │
│  66. Quadratic Solver                                       │
├─────────────────────────────────────────────────────────────┤
│  MEMORY & HISTORY                                           │
│  70. Memory Store (MS)    71. Memory Recall (MR)            │
│  72. Memory Clear (MC)    73. Memory Add (M+)               │
│  74. Memory Subtract (M-) 75. Show History                  │
│  76. Clear History                                          │
├─────────────────────────────────────────────────────────────┤
│  EXPRESSION MODE                                            │
│  80. Evaluate Expression (use: sin, cos, sqrt, log, etc.)   │
│      Variables: ans (last result), mem (memory value)       │
│      Constants: pi, e                                       │
└─────────────────────────────────────────────────────────────┘
│  'q' or 'quit' to exit    'h' or 'help' for menu            │
└─────────────────────────────────────────────────────────────┘
""")


def get_number(prompt):
    """Get a number from user input"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.")


def get_numbers_list(prompt):
    """Get a list of numbers from user input"""
    while True:
        try:
            user_input = input(prompt)
            numbers = [float(x.strip()) for x in user_input.split(',')]
            return numbers
        except ValueError:
            print("❌ Invalid input! Please enter numbers separated by commas.")


def main():
    calc = AdvancedCalculator()
    print_menu()
    
    while True:
        print("\n" + "-"*40)
        choice = input("Enter choice (or 'h' for help): ").strip().lower()
        
        if choice in ('q', 'quit', 'exit'):
            print("\n✨ Thank you for using Advanced Calculator! Goodbye! ✨")
            break
        
        if choice in ('h', 'help', 'menu'):
            print_menu()
            continue
        
        try:
            # Basic Operations
            if choice == '1':
                num1 = get_number("Enter first number: ")
                num2 = get_number("Enter second number: ")
                result = calc.add(num1, num2)
                print(f"✅ Result: {num1} + {num2} = {result}")
                calc.add_to_history(f"{num1} + {num2}", result)
            
            elif choice == '2':
                num1 = get_number("Enter first number: ")
                num2 = get_number("Enter second number: ")
                result = calc.subtract(num1, num2)
                print(f"✅ Result: {num1} - {num2} = {result}")
                calc.add_to_history(f"{num1} - {num2}", result)
            
            elif choice == '3':
                num1 = get_number("Enter first number: ")
                num2 = get_number("Enter second number: ")
                result = calc.multiply(num1, num2)
                print(f"✅ Result: {num1} × {num2} = {result}")
                calc.add_to_history(f"{num1} × {num2}", result)
            
            elif choice == '4':
                num1 = get_number("Enter first number: ")
                num2 = get_number("Enter second number: ")
                result = calc.divide(num1, num2)
                print(f"✅ Result: {num1} ÷ {num2} = {result}")
                calc.add_to_history(f"{num1} ÷ {num2}", result)
            
            elif choice == '5':
                num1 = get_number("Enter first number: ")
                num2 = get_number("Enter second number: ")
                result = calc.modulus(num1, num2)
                print(f"✅ Result: {num1} % {num2} = {result}")
                calc.add_to_history(f"{num1} % {num2}", result)
            
            elif choice == '6':
                num1 = get_number("Enter base: ")
                num2 = get_number("Enter exponent: ")
                result = calc.power(num1, num2)
                print(f"✅ Result: {num1}^{num2} = {result}")
                calc.add_to_history(f"{num1}^{num2}", result)
            
            elif choice == '7':
                num1 = get_number("Enter first number: ")
                num2 = get_number("Enter second number: ")
                result = calc.floor_divide(num1, num2)
                print(f"✅ Result: {num1} // {num2} = {result}")
                calc.add_to_history(f"{num1} // {num2}", result)
            
            # Scientific Functions
            elif choice == '10':
                num = get_number("Enter number: ")
                result = calc.square_root(num)
                print(f"✅ Result: √{num} = {result}")
                calc.add_to_history(f"√{num}", result)
            
            elif choice == '11':
                num = get_number("Enter number: ")
                result = calc.cube_root(num)
                print(f"✅ Result: ∛{num} = {result}")
                calc.add_to_history(f"∛{num}", result)
            
            elif choice == '12':
                num = get_number("Enter number: ")
                n = get_number("Enter root index: ")
                result = calc.nth_root(num, n)
                print(f"✅ Result: {n}√{num} = {result}")
                calc.add_to_history(f"{n}√{num}", result)
            
            elif choice == '13':
                num = int(get_number("Enter non-negative integer: "))
                result = calc.factorial(num)
                print(f"✅ Result: {num}! = {result}")
                calc.add_to_history(f"{num}!", result)
            
            elif choice == '14':
                num = get_number("Enter number: ")
                result = calc.absolute(num)
                print(f"✅ Result: |{num}| = {result}")
                calc.add_to_history(f"|{num}|", result)
            
            elif choice == '15':
                num = get_number("Enter number: ")
                result = calc.logarithm(num)
                print(f"✅ Result: log₁₀({num}) = {result}")
                calc.add_to_history(f"log₁₀({num})", result)
            
            elif choice == '16':
                num = get_number("Enter number: ")
                result = calc.natural_log(num)
                print(f"✅ Result: ln({num}) = {result}")
                calc.add_to_history(f"ln({num})", result)
            
            elif choice == '17':
                num = get_number("Enter exponent: ")
                result = calc.exponential(num)
                print(f"✅ Result: e^{num} = {result}")
                calc.add_to_history(f"e^{num}", result)
            
            # Trigonometric Functions
            elif choice == '20':
                num = get_number("Enter angle in degrees: ")
                result = calc.sine(num)
                print(f"✅ Result: sin({num}°) = {result}")
                calc.add_to_history(f"sin({num}°)", result)
            
            elif choice == '21':
                num = get_number("Enter angle in degrees: ")
                result = calc.cosine(num)
                print(f"✅ Result: cos({num}°) = {result}")
                calc.add_to_history(f"cos({num}°)", result)
            
            elif choice == '22':
                num = get_number("Enter angle in degrees: ")
                result = calc.tangent(num)
                print(f"✅ Result: tan({num}°) = {result}")
                calc.add_to_history(f"tan({num}°)", result)
            
            elif choice == '23':
                num = get_number("Enter value (-1 to 1): ")
                result = calc.arc_sine(num)
                print(f"✅ Result: arcsin({num}) = {result}°")
                calc.add_to_history(f"arcsin({num})", result)
            
            elif choice == '24':
                num = get_number("Enter value (-1 to 1): ")
                result = calc.arc_cosine(num)
                print(f"✅ Result: arccos({num}) = {result}°")
                calc.add_to_history(f"arccos({num})", result)
            
            elif choice == '25':
                num = get_number("Enter value: ")
                result = calc.arc_tangent(num)
                print(f"✅ Result: arctan({num}) = {result}°")
                calc.add_to_history(f"arctan({num})", result)
            
            elif choice == '26':
                num = get_number("Enter value: ")
                result = calc.sinh(num)
                print(f"✅ Result: sinh({num}) = {result}")
                calc.add_to_history(f"sinh({num})", result)
            
            elif choice == '27':
                num = get_number("Enter value: ")
                result = calc.cosh(num)
                print(f"✅ Result: cosh({num}) = {result}")
                calc.add_to_history(f"cosh({num})", result)
            
            elif choice == '28':
                num = get_number("Enter value: ")
                result = calc.tanh(num)
                print(f"✅ Result: tanh({num}) = {result}")
                calc.add_to_history(f"tanh({num})", result)
            
            # Statistical Functions
            elif choice == '30':
                numbers = get_numbers_list("Enter numbers (comma-separated): ")
                result = calc.mean(numbers)
                print(f"✅ Mean: {result}")
                calc.add_to_history(f"mean({numbers})", result)
            
            elif choice == '31':
                numbers = get_numbers_list("Enter numbers (comma-separated): ")
                result = calc.median(numbers)
                print(f"✅ Median: {result}")
                calc.add_to_history(f"median({numbers})", result)
            
            elif choice == '32':
                numbers = get_numbers_list("Enter numbers (comma-separated): ")
                result = calc.mode(numbers)
                print(f"✅ Mode: {result}")
                calc.add_to_history(f"mode({numbers})", result)
            
            elif choice == '33':
                numbers = get_numbers_list("Enter numbers (comma-separated): ")
                result = calc.std_dev(numbers)
                print(f"✅ Standard Deviation: {result}")
                calc.add_to_history(f"std_dev({numbers})", result)
            
            elif choice == '34':
                numbers = get_numbers_list("Enter numbers (comma-separated): ")
                result = calc.variance(numbers)
                print(f"✅ Variance: {result}")
                calc.add_to_history(f"variance({numbers})", result)
            
            elif choice == '35':
                numbers = get_numbers_list("Enter numbers (comma-separated): ")
                result = calc.sum_list(numbers)
                print(f"✅ Sum: {result}")
                calc.add_to_history(f"sum({numbers})", result)
            
            # Number Conversions
            elif choice == '40':
                num = int(get_number("Enter decimal number: "))
                result = calc.decimal_to_binary(num)
                print(f"✅ Binary: {result}")
                calc.add_to_history(f"dec_to_bin({num})", result)
            
            elif choice == '41':
                num = int(get_number("Enter decimal number: "))
                result = calc.decimal_to_octal(num)
                print(f"✅ Octal: {result}")
                calc.add_to_history(f"dec_to_oct({num})", result)
            
            elif choice == '42':
                num = int(get_number("Enter decimal number: "))
                result = calc.decimal_to_hex(num)
                print(f"✅ Hexadecimal: {result}")
                calc.add_to_history(f"dec_to_hex({num})", result)
            
            elif choice == '43':
                binary = input("Enter binary number: ").strip()
                result = calc.binary_to_decimal(binary)
                print(f"✅ Decimal: {result}")
                calc.add_to_history(f"bin_to_dec({binary})", result)
            
            elif choice == '44':
                octal = input("Enter octal number: ").strip()
                result = calc.octal_to_decimal(octal)
                print(f"✅ Decimal: {result}")
                calc.add_to_history(f"oct_to_dec({octal})", result)
            
            elif choice == '45':
                hex_num = input("Enter hexadecimal number: ").strip()
                result = calc.hex_to_decimal(hex_num)
                print(f"✅ Decimal: {result}")
                calc.add_to_history(f"hex_to_dec({hex_num})", result)
            
            # Unit Conversions
            elif choice == '50':
                num = get_number("Enter temperature in Celsius: ")
                result = calc.celsius_to_fahrenheit(num)
                print(f"✅ Result: {num}°C = {result}°F")
                calc.add_to_history(f"{num}°C to °F", result)
            
            elif choice == '51':
                num = get_number("Enter temperature in Fahrenheit: ")
                result = calc.fahrenheit_to_celsius(num)
                print(f"✅ Result: {num}°F = {result}°C")
                calc.add_to_history(f"{num}°F to °C", result)
            
            elif choice == '52':
                num = get_number("Enter distance in Kilometers: ")
                result = calc.km_to_miles(num)
                print(f"✅ Result: {num} km = {result} miles")
                calc.add_to_history(f"{num} km to miles", result)
            
            elif choice == '53':
                num = get_number("Enter distance in Miles: ")
                result = calc.miles_to_km(num)
                print(f"✅ Result: {num} miles = {result} km")
                calc.add_to_history(f"{num} miles to km", result)
            
            elif choice == '54':
                num = get_number("Enter weight in Kilograms: ")
                result = calc.kg_to_pounds(num)
                print(f"✅ Result: {num} kg = {result} lbs")
                calc.add_to_history(f"{num} kg to lbs", result)
            
            elif choice == '55':
                num = get_number("Enter weight in Pounds: ")
                result = calc.pounds_to_kg(num)
                print(f"✅ Result: {num} lbs = {result} kg")
                calc.add_to_history(f"{num} lbs to kg", result)
            
            elif choice == '56':
                num = get_number("Enter angle in Degrees: ")
                result = calc.degrees_to_radians(num)
                print(f"✅ Result: {num}° = {result} radians")
                calc.add_to_history(f"{num}° to radians", result)
            
            elif choice == '57':
                num = get_number("Enter angle in Radians: ")
                result = calc.radians_to_degrees(num)
                print(f"✅ Result: {num} radians = {result}°")
                calc.add_to_history(f"{num} radians to °", result)
            
            # Special Calculations
            elif choice == '60':
                num1 = int(get_number("Enter first number: "))
                num2 = int(get_number("Enter second number: "))
                result = calc.gcd(num1, num2)
                print(f"✅ GCD({num1}, {num2}) = {result}")
                calc.add_to_history(f"GCD({num1}, {num2})", result)
            
            elif choice == '61':
                num1 = int(get_number("Enter first number: "))
                num2 = int(get_number("Enter second number: "))
                result = calc.lcm(num1, num2)
                print(f"✅ LCM({num1}, {num2}) = {result}")
                calc.add_to_history(f"LCM({num1}, {num2})", result)
            
            elif choice == '62':
                n = int(get_number("Enter n: "))
                r = int(get_number("Enter r: "))
                result = calc.permutation(n, r)
                print(f"✅ P({n}, {r}) = {result}")
                calc.add_to_history(f"P({n}, {r})", result)
            
            elif choice == '63':
                n = int(get_number("Enter n: "))
                r = int(get_number("Enter r: "))
                result = calc.combination(n, r)
                print(f"✅ C({n}, {r}) = {result}")
                calc.add_to_history(f"C({n}, {r})", result)
            
            elif choice == '64':
                value = get_number("Enter value: ")
                percent = get_number("Enter percentage: ")
                result = calc.percentage(value, percent)
                print(f"✅ {percent}% of {value} = {result}")
                calc.add_to_history(f"{percent}% of {value}", result)
            
            elif choice == '65':
                old_val = get_number("Enter old value: ")
                new_val = get_number("Enter new value: ")
                result = calc.percentage_change(old_val, new_val)
                print(f"✅ Percentage change: {result:.2f}%")
                calc.add_to_history(f"% change ({old_val} to {new_val})", result)
            
            elif choice == '66':
                print("Solve: ax² + bx + c = 0")
                a = get_number("Enter coefficient a: ")
                b = get_number("Enter coefficient b: ")
                c = get_number("Enter coefficient c: ")
                result = calc.quadratic_solver(a, b, c)
                if len(result) == 1:
                    print(f"✅ Solution: x = {result[0]}")
                else:
                    print(f"✅ Solutions: x₁ = {result[0]}, x₂ = {result[1]}")
                calc.add_to_history(f"Quadratic({a}x² + {b}x + {c})", result)
            
            # Memory Operations
            elif choice == '70':
                num = get_number("Enter value to store: ")
                print(f"✅ {calc.memory_store(num)}")
            
            elif choice == '71':
                result = calc.memory_recall()
                print(f"✅ Memory value: {result}")
            
            elif choice == '72':
                print(f"✅ {calc.memory_clear()}")
            
            elif choice == '73':
                num = get_number("Enter value to add to memory: ")
                print(f"✅ {calc.memory_add(num)}")
            
            elif choice == '74':
                num = get_number("Enter value to subtract from memory: ")
                print(f"✅ {calc.memory_subtract(num)}")
            
            elif choice == '75':
                print("\n📜 Calculation History:")
                print("-" * 40)
                print(calc.show_history())
            
            elif choice == '76':
                print(f"✅ {calc.clear_history()}")
            
            # Expression Evaluation
            elif choice == '80':
                print("\n📝 Expression Mode")
                print("Available functions: sin, cos, tan, sqrt, log, ln, exp, abs, pow")
                print("Constants: pi, e")
                print("Variables: ans (last result), mem (memory)")
                print("Use ^ for power (e.g., 2^3)")
                expr = input("Enter expression: ").strip()
                result = calc.evaluate_expression(expr)
                print(f"✅ Result: {result}")
                calc.add_to_history(expr, result)
            
            else:
                print("❌ Invalid choice. Enter 'h' to see the menu.")
        
        except ValueError as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
