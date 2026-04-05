class Bird:
    def sound(self):
        print("Bird making a sound")

class Cat:
    def sound(self):
        print("Cat Meow")

for obj in [Bird(), Cat()]:
    print(obj.sound())