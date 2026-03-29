from abc import ABC, abstractmethod

class shape:
        
    @abstractmethod
    def area(self) -> float:    
        pass

class Circle(shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

class Square(shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

class Triangle(shape):      
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height    

shapes = [Circle(5), Square(4), Triangle(3, 6)]

for s in shapes:
    print(s.area())