class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def deposite(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance
    
acc = BankAccount(1000)
print(acc.get_balance())

acc.deposite(1000)

print(acc.get_balance())
