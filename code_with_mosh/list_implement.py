# --- Creating lists ---
numbers = [1, 2, 3, 4]
names = ["mihitha", "bandara"]
mixed = [1, "hello", 3.14, True]

print("Numbers:", numbers)
print("Names:", names)
print("Mixed:", mixed)
print()

# --- Accessing items ---
print("First number:", numbers[0])
print("Last number:", numbers[-1])
print()

# --- Modifying items ---
numbers[1] = 10
print("After modifying index 1:", numbers)
print()

# --- Adding items ---
numbers.append(5)
print("After append:", numbers)

numbers.insert(1, 99)
print("After insert at index 1:", numbers)
print()

# --- Removing items ---
numbers.remove(99)   # remove by value
print("After remove 99:", numbers)

popped = numbers.pop(2)  # remove by index
print("Popped element:", popped)
print("After pop:", numbers)

numbers_copy = numbers.copy()
numbers.clear()
print("After clear:", numbers)
print()

# --- List length ---
print("Length of names list:", len(names))
print()

# --- Checking existence ---
if "mihitha" in names:
    print("Found 'mihitha' in list")
print()

# --- Looping through a list ---
print("Looping through names:")
for n in names:
    print(" -", n)
print()

# --- Sorting a list ---
num_list = [5, 3, 8, 1]
num_list.sort()
print("Sorted list:", num_list)
print()

# --- List comprehension ---
squares = [x * 2 for x in range(5)]
print("List comprehension:", squares)
