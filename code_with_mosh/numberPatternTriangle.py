n = int(input("Height of triangle: "))  # e.g. 5

row = 0
while row < n:
    num = 1
    line = ""
    while num <= n - row:
        line += str(num) + " "
        num += 1
    print(line)
    row += 1
