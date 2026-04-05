arr = [1,2,3,4,5,5]

def count_freq(arr):
    freq = {}
    for i in arr:
        freq[i] = freq.get(i, 0) + 1
    return freq

print(count_freq(arr))

def find_max(arr):
    return max(arr)

print("Maximum value is : ", find_max(arr))

