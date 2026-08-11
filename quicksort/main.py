# Global array

a = []


def Interchange(a, i, j):
    # Exchange a[i] with a[j]
    p = a[i]
    a[i] = a[j]
    a[j] = p


def display_array(p, q, pivot_index=None, split_index=None):

    for i in range(1, len(a) - 1):

        # Print pivot in bold
        if i == pivot_index:
            print("\033[1m" + str(a[i]) + "\033[0m", end=" ")

        else:
            print(a[i], end=" ")

        # Print split
        if i == split_index:
            print("|", end=" ")

    print()


def Partition(a, m, p):

    v = a[m]
    i = m
    j = p

    # Display entire array with current pivot in bold
    print()
    display_array(m, p - 1, m)

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

    # Display entire array after partition
    display_array(m, p - 1, j, j)

    return j


def QuickSort(a, p, q):

    # If there is more than one element
    if p < q:

        # Divide P into two subproblems
        j = Partition(a, p, q + 1)

        # Solve the subproblems
        QuickSort(a, p, j - 1)
        QuickSort(a, j + 1, q)

        # No combining required


# Input

print("Enter Size:")
n = int(input().strip())

print("Enter Elements:")
a = [None] + input().strip().split()

# a[n + 1] = infinity
a.append(float("inf"))

print("\nBefore sorting:")
print(*a[1:n + 1])

print("\nQuick Sort Process:")

# QuickSort starts from index 1
QuickSort(a, 1, n)

print("\nAfter sorting:")
print(*a[1:n + 1])