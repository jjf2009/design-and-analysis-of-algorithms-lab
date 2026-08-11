# Global arrays

a = []
b = []

# Stores the current split boundaries
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

        # Divide P into subproblems
        mid = (low + high) // 2

        # Add the split
        split_positions.append(mid)

        # Display the split
        display()

        # Solve the subproblems
        MergeSort(low, mid)
        MergeSort(mid + 1, high)

        # Combine the solutions
        Merge(low, mid, high)

        # Remove the split after merging
        if mid in split_positions:
            split_positions.remove(mid)

        # Display the merged result
        display()


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

        for k in range(j, high + 1):
            b[i] = a[k]
            i = i + 1

    # else
    else:

        for k in range(h, mid + 1):
            b[i] = a[k]
            i = i + 1

    # Copy merged elements back
    for k in range(low, high + 1):
        a[k] = b[k]


# -------------------------
# Input
# -------------------------

print("Enter Size:")
n = int(input().strip())

print("Enter Elements:")
a = [None] + input().strip().split()

# Auxiliary array
b = [None] * (n + 1)


# -------------------------
# Merge Sort
# -------------------------

print("\nMerge Sort Process:")

display()

MergeSort(1, n)


# -------------------------
# Final Result
# -------------------------

print("\nSorted array:")
print(*a[1:])