class animal:
    def speak(self):
        print("Animal Speak")

class dog(animal): #inherits Animal
    def bark(self):
        print("Dog Bark")

d = dog()

print(d.speak())
print(d.bark())