from abc import ABC, abstractmethod

class shape:
    pass

class Circle(shape):

    @abstractmethod
    def area(self):
        pass
    
class Square(shape):
    pass
class Triangle(shape):
    pass

shapes = [Circle(), Square(), Triangle()]