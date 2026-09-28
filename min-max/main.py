a = []
def MaxMin(i, j, max, min):
    if i == j:
        max = a[i]
        min = a[i]
        print(f"{i} {j} {max} {min}")
    elif i == j - 1:
        if a[i] < a[j]:
            max = a[j]
            min = a[i]
        else:
            max = a[i]
            min = a[j]
        print(f"{i} {j} {max} {min}")
    else:
        mid = (i + j) // 2
        max1, min1 = MaxMin(i, mid, max, min)
        max2, min2 = MaxMin(mid + 1, j, max, min)
        max = max1
        min = min1
        if max < max2:
            max = max2
        if min > min2:
            min = min2
    return max, min
print("Enter Size:")
n = int(input().strip())
print("Enter Elements:")
a = [0] + list(map(int, input().strip().split()))
max = 0
min = 0
print("i j max min")
max, min = MaxMin(1, n, max, min)
print("Maximum:", max)
print("Minimum:", min)
