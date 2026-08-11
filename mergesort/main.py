# Global arrays
a = []
b = []


def MergeSort(low, high):

    # If there is more than one element
    if low < high:

        # Divide P into subproblems
        mid = (low + high) // 2

        # Solve the subproblems
        MergeSort(low, mid)
        MergeSort(mid + 1, high)

        # Combine the solutions
        Merge(low, mid, high)


def Merge(low, mid, high):

    # h := low, i := low, j := mid + 1
    h = low
    i = low
    j = mid + 1

    # while (h <= mid) and (j <= high)
    while (h <= mid) and (j <= high):

        if a[h] <= a[j]:
            b[i] = a[h]
            h = h + 1

        else:
            b[i] = a[j]
            j = j + 1

        i = i + 1

    # if (h > mid)
    if h > mid:

        # for k := j to high
        for k in range(j, high + 1):
            b[i] = a[k]
            i = i + 1

    # else
    else:

        # for k := h to mid
        for k in range(h, mid + 1):
            b[i] = a[k]
            i = i + 1

    # for k := low to high
    for k in range(low, high + 1):
        a[k] = b[k]


# Input
print("Enter Size:")
n = int(input().strip())

print("Enter Elements:")

# Make array 1-indexed
a = [None] + input().strip().split()

# Auxiliary array
b = [None] * (n + 1)

# Merge Sort
MergeSort(1, n)

# Output
print("Sorted array:", *a[1:])