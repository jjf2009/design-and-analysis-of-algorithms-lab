a = []
def Interchange(a, i, j):
    p = a[i]
    a[i] = a[j]
    a[j] = p
def display_array(a, p, q, pivot_index=None, left=None, right=None):
    for i in range(1, len(a) - 1):
        if i == p:
            print("[", end=" ")
        if i == pivot_index:
            print("\033[1m" + str(a[i]) + "\033[0m", end=" ")
        else:
            print(a[i], end=" ")
        if i == q:
            print("]", end=" ")
        elif i < len(a) - 2:
            print(end=" ")
    print()
def display_split(a, p, j, q):
    for i in range(1, len(a) - 1):
        if i == p:
            print("[", end=" ")
        print(a[i], end=" ")
        if i == j - 1:
            print("]", end=" ")
        if i == j:
            print("\033[1m" + str(a[i]) + "\033[0m", end=" ")
        if i == j + 1:
            print("[", end=" ")
        if i == q:
            print("]", end=" ")
        if i < len(a) - 2:
            print(end=" ")
    print()
def Partition(a, m, p):
    v = a[m]
    i = m
    j = p
    print()
    display_array(a, m, p - 1, m)
    while True:
        i = i + 1
        while a[i] < v:
            i = i + 1
        j = j - 1
        while a[j] > v:
            j = j - 1
        if i < j:
            Interchange(a, i, j)
        if i >= j:
            break
    a[m] = a[j]
    a[j] = v
    display_split(a, m, j, p - 1)
    return j
def QuickSort(a, p, q):
    if p < q:
        j = Partition(a, p, q + 1)
        QuickSort(a, p, j - 1)
        QuickSort(a, j + 1, q)
print("Enter Size:")
n = int(input().strip())
print("Enter Elements:")
a = [None] + input().strip().split()
a.append(float("inf"))
print("\nBefore sorting:")
print(*a[1:n + 1])
print("\nQuick Sort Process:")
QuickSort(a, 1, n)
print("\nAfter sorting:")
print(*a[1:n + 1])
