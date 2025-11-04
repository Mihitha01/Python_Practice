n = int(input("Height of triangle: "))  # e.g. 6

row = 0
while row < n:
    cols = n - row
    col = 0
    line = ""
    while col < cols:
        # print star on borders (first or last column) or top row
        if row == 0 or col == 0 or col == cols - 1:
            line += "*"
        else:
            line += " "
        col += 1
    print(line)
    row += 1
