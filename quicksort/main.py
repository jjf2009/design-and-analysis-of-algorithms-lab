# Global array

a = []


def Interchange(a, i, j):
    # Exchange a[i] with a[j]
    p = a[i]
    a[i] = a[j]
    a[j] = p


def display_array(a, p, q, pivot_index=None, left=None, right=None):

    for i in range(1, len(a) - 1):

        # Opening bracket
        if i == p:
            print("[", end=" ")

        # Pivot in bold
        if i == pivot_index:
            print("\033[1m" + str(a[i]) + "\033[0m", end=" ")
        else:
            print(a[i], end=" ")

        # Closing bracket
        if i == q:
            print("]", end=" ")

        # Space between elements
        elif i < len(a) - 2:
            print(end=" ")

    print()


def display_split(a, p, j, q):

    for i in range(1, len(a) - 1):

        # Left subarray
        if i == p:
            print("[", end=" ")

        print(a[i], end=" ")

        if i == j - 1:
            print("]", end=" ")

        # Pivot
        if i == j:
            print("\033[1m" + str(a[i]) + "\033[0m", end=" ")

        # Right subarray
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

    # Display current subarray with pivot
    print()
    display_array(a, m, p - 1, m)

    while True:

        # repeat
        i = i + 1

        while a[i] < v:
            i = i + 1

        # repeat
        j = j - 1

        while a[j] > v:
            j = j - 1

        # if (i < j)
        if i < j:
            Interchange(a, i, j)

        # until (i >= j)
        if i >= j:
            break

    a[m] = a[j]
    a[j] = v

    # Display the two partitions
    display_split(a, m, j, p - 1)

    return j


def QuickSort(a, p, q):

    # If there is more than one element
    if p < q:

        # Divide P into two subproblems
        j = Partition(a, p, q + 1)

        # Solve left subproblem
        QuickSort(a, p, j - 1)

        # Solve right subproblem
        QuickSort(a, j + 1, q)


# -------------------------
# Input
# -------------------------

print("Enter Size:")
n = int(input().strip())

print("Enter Elements:")
a = [None] + input().strip().split()

# a[n + 1] = infinity
a.append(float("inf"))


# -------------------------
# Quick Sort
# -------------------------

print("\nBefore sorting:")
print(*a[1:n + 1])

print("\nQuick Sort Process:")

QuickSort(a, 1, n)


# -------------------------
# Output
# -------------------------

print("\nAfter sorting:")
print(*a[1:n + 1])