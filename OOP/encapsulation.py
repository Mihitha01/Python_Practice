#ENCAPSULATION

class Computer:
    def __init__(self):
        self.__max_price = 900 #we use __ to make the variable private
        
    def sell(self):
        print("Selling Price: {}".format(self.__max_price))

    def set_max_price(self, price):
        self.__max_price = price

com1 = Computer()
com1.sell()
com1.__max_price = 1000
com1.sell()
com1.set_max_price(1200)
com1.sell()


