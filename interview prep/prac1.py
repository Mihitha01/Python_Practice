def func(a, b=10):
    return a+b

print(func(5))  

a = [1,2,3] #using a reference
#b = a
#b.append(5)
#print(a)

a.append(5)
print(a)

s="leval"

def is_palindrome(s):
    return s==s[::-1]

print(is_palindrome(s))