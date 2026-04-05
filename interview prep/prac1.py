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
    return s==s[::-1] # s[start:stop:step]
                      # start -> where to begin , stop -> where to stop , step -> how to move

print(is_palindrome(s))

class A:
    def show(self):
        print("A")


class B(A):
    def show(self):
        print("B")

obj = B()
obj.show()        