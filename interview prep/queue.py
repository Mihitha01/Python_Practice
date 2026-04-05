# Queue Implementation in Python (with explanations)

class Queue:
    def __init__(self):
        # This list will store queue elements
        self.items = []

    def enqueue(self, item):
        # Add element to the END of the queue (rear)
        # Example: [10, 20] -> enqueue(30) -> [10, 20, 30]
        self.items.append(item)

    def dequeue(self):
        # Remove element from the FRONT of the queue
        # FIFO: First In First Out
        if self.is_empty():
            return "Queue is empty"
        
        # pop(0) removes first element
        # Example: [10, 20, 30] -> removes 10 -> [20, 30]
        return self.items.pop(0)

    def front(self):
        # Get the first element without removing it
        if self.is_empty():
            return "Queue is empty"
        
        return self.items[0]

    def is_empty(self):
        # Check if queue is empty
        # Returns True if empty, False otherwise
        return len(self.items) == 0

    def size(self):
        # Return number of elements in queue
        return len(self.items)

    def display(self):
        # Print all elements in queue
        print(self.items)


# ------------------- TESTING -------------------

# Create a Queue object
q = Queue()

# Add elements
q.enqueue(10)
q.enqueue(20)
q.enqueue(30)

# Display queue
print("Queue:", end=" ")
q.display()   # Output: [10, 20, 30]

# Get front element
print("Front element:", q.front())   # Output: 10

# Remove element
print("Dequeued:", q.dequeue())     # Output: 10

# Display after removal
print("Queue after dequeue:", end=" ")
q.display()   # Output: [20, 30]

# Check if empty
print("Is empty?", q.is_empty())    # Output: False

# Get size
print("Size:", q.size())           # Output: 2