names = ['john','Maria','Anne','kane','Duke']
print(names[2:4])
print(names)
names[0] = 'jon'
print(names)

#finding the largest number

numbers = [3,6,2,7,8,16,2,9,3,16]
max = numbers[0]
for number in numbers:
    if number > max:
        max = number
print(max)