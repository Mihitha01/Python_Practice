course = "Python's Course for Beginners"
print(course)

long_string = '''
Hello Mihitha,
here is our first email to you.
Thank you,
    The support team
'''
print(long_string)

character_1 = 'Mihitha'
print(character_1[-2])

for x in character_1:
    print(x)

print(character_1[0:5])
print(character_1[1:5])
print(character_1[:5])
print(character_1[:])

first = 'John'
last = 'Smith'
message = first + ' [' + last + '] is a coder'
print(message)
msg = f'{first} [{last}] is a coder'
print(msg)