def greet(name):
    print("Hello", name)

greet("John")

def add(a, b):
    return a + b

r1 = add(5, 3)
print(r1)

def sub(a, b):
    return a - b

r2 = sub(5, 3)
print(r2)

def mul(a, b):
    return a/b

r3 = mul(5, 3)
print(r3)

def welcome(name = "Guest"):
    print("Hello", name)

welcome()
welcome("Alex")

def student(name, age):
    print(f"My name is {name} I'm {age} years old")

student(age=20, name="John")

def total(*numbers):
    return sum(numbers)

print(total(1,2,3,4,5))

def details(**info):
    return(info)

print(details(name="John", age=20))

