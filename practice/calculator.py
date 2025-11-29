num1 = float(input("Enter any Number: "))
num2 = float(input("Enter any Number: "))
op = input("Enter an Operator: ")

def Add(num1,num2):
    print(num1 + num2)

def Sub(num1,num2):
    print(num1 - num2)

def Mul(num1,num2):
    print(num1 * num2)

def Div(num1,num2):
    print(num1 / num2)        

match op:
    case '+':
        Add(num1,num2)
    case '-':
        Sub(num1,num2)
    case '*':
        Mul(num1,num2)
    case '/':
        Div(num1,num2)
    case _:
        print("Invalid")