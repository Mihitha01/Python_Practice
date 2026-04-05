class Stack:
    def __init__(self): #self - Current Object
        self.items = [] #Creates an empty list to store stack elements

    # Push element onto stack
    def push(self, item):
        self.items.append(item)

    # Pop element from stack
    def pop(self):
        if self.is_empty():
            return "Stack is empty"
        return self.items.pop()

    # Peek top element
    def peek(self):
        if self.is_empty():
            return "Stack is empty"
        return self.items[-1]

    # Check if stack is empty
    def is_empty(self):
        return len(self.items) == 0

    # Get size of stack
    def size(self):
        return len(self.items)

    # Display stack
    def display(self):
        print(self.items)


# 🔹 Testing the Stack
s = Stack()

s.push(10)
s.push(20)
s.push(30)

print("Stack:", end=" ")
s.display()

print("Top element:", s.peek())
print("Popped:", s.pop())

print("Stack after pop:", end=" ")
s.display()

print("Is empty?", s.is_empty())
print("Size:", s.size())