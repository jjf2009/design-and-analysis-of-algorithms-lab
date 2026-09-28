a = []
b = []
split_positions = []
def display():
    result = ""
    for i in range(1, len(a)):
        result += str(a[i])
        if i in split_positions:
            result += " | "
        elif i < len(a) - 1:
            result += " "
    print(result)
def MergeSort(low, high):
    if low < high:
        mid = (low + high) // 2
        split_positions.append(mid)
        display()
        MergeSort(low, mid)
        MergeSort(mid + 1, high)
        Merge(low, mid, high)
        if mid in split_positions:
            split_positions.remove(mid)
        display()
def Merge(low, mid, high):
    h = low
    i = low
    j = mid + 1
    while (h <= mid) and (j <= high):
        if a[h] <= a[j]:
            b[i] = a[h]
            h = h + 1
        else:
            b[i] = a[j]
            j = j + 1
        i = i + 1
    if h > mid:
        for k in range(j, high + 1):
            b[i] = a[k]
            i = i + 1
    else:
        for k in range(h, mid + 1):
            b[i] = a[k]
            i = i + 1
    for k in range(low, high + 1):
        a[k] = b[k]
print("Enter Size:")
n = int(input().strip())
print("Enter Elements:")
a = [None] + input().strip().split()
b = [None] * (n + 1)
print("\nMerge Sort Process:")
display()
MergeSort(1, n)
print("\nSorted array:")
print(*a[1:])
