# Singly Linked List Implementation in Python (with explanations)

from __future__ import annotations
from typing import Optional

# Step 1: Create a Node class
class Node:
    def __init__(self, data):
        # Each node has data and a pointer to next node
        self.data = data
        self.next: Optional[Node] = None


# Step 2: Create LinkedList class
class LinkedList:
    def __init__(self):
        # Head is the first node of the list
        self.head: Optional[Node] = None

    def insert_at_beginning(self, data):
        # Create new node
        new_node = Node(data)
        
        # Point new node to current head
        new_node.next = self.head
        
        # Move head to new node
        self.head = new_node

    def insert_at_end(self, data):
        # Create new node
        new_node = Node(data)

        # If list is empty
        if self.head is None:
            self.head = new_node
            return

        # Traverse to last node
        temp = self.head
        while temp.next:
            temp = temp.next

        # Attach new node at end
        temp.next = new_node

    def delete(self, key):
        # Delete first occurrence of value
        
        temp = self.head

        # If head itself holds the value
        if temp and temp.data == key:
            self.head = temp.next
            temp = None
            return

        # Search for the key
        prev: Optional[Node] = None
        while temp and temp.data != key:
            prev = temp
            temp = temp.next

        # If key not found
        if temp is None:
            print("Value not found")
            return

        # Unlink the node
        assert prev is not None
        prev.next = temp.next
        temp = None

    def search(self, key):
        # Search for a value in list
        
        temp = self.head
        while temp:
            if temp.data == key:
                return True
            temp = temp.next
        
        return False

    def display(self):
        # Print all elements
        
        temp = self.head
        while temp:
            print(temp.data, end=" -> ")
            temp = temp.next
        print("None")


# ------------------- TESTING -------------------

# Create Linked List
ll = LinkedList()

# Insert elements
ll.insert_at_beginning(10)
ll.insert_at_beginning(5)
ll.insert_at_end(20)
ll.insert_at_end(30)

# Display list
print("Linked List:")
ll.display()   # Output: 5 -> 10 -> 20 -> 30 -> None

# Search element
print("Search 10:", ll.search(10))   # True
print("Search 99:", ll.search(99))   # False

# Delete element
ll.delete(10)

print("After deleting 10:")
ll.display()   # Output: 5 -> 20 -> 30 -> None