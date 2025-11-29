numbers = [5, 2, 1, 7, 4]
numbers.append(20) #add number to the end of the list
print(numbers)

numbers.insert(0, 10)
numbers.insert(1, 20)
print(numbers)

numbers.remove(5) # remove any item from the list
numbers.remove(2)
print(numbers)

numbers.pop() # remove the last item
print(numbers)

print(10 in numbers)
print(50 in numbers)

numbers.sort() #ascending order sort
print(numbers)

numbers.reverse()
print(numbers) #reverse order sort

num = [2, 3, 4, 6, 3, 4, 6, 1]
u = []
for n in num:
    if n not in u:
        u.append(n)
print(u)