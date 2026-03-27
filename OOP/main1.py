from car import Car

car_1 = Car("Toyota", "Camry", 2020, "Red")
car_2 = Car("Honda", "Civic", 2019, "Blue")

print(car_1.make)  # Output: Toyota
print(car_1.model) # Output: Camry
print(car_1.year)  # Output: 2020
print(car_1.color) # Output: Red

car_1.drive()      # Output: This car is driving.
car_1.stop()       # Output: This car has stopped.

print(car_2.make)  # Output: Honda
print(car_2.model) # Output: Civic
print(car_2.year)  # Output: 2019
print(car_2.color) # Output: Blue

car_2.drive()      # Output: This car is driving.
car_2.stop()       # Output: This car has stopped.