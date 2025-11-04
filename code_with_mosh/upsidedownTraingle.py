n = int(input("Height of triangle: "))  # e.g. 5

row = 0
while row < n:
    # leading spaces = row
    spaces = 0
    line = ""
    while spaces < row:
        line += " "
        spaces += 1

    # stars count = 2*(n-row)-1 for centered shape
    stars = 0
    star_count = 2 * (n - row) - 1
    while stars < star_count:
        line += "*"
        stars += 1

    print(line)
    row += 1
