def sum_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(sum_all(1,2,3))
print(sum_all(10,20,30,40))

    