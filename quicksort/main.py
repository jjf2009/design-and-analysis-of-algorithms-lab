# Global array
a = []


def Interchange(a, i, j):
    # Exchange a[i] with a[j]
    p = a[i]
    a[i] = a[j]
    a[j] = p


def Partition(a, m, p):

    v = a[m]
    i = m
    j = p

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

print("Before sorting:", *a[1:n + 1])

# QuickSort starts from index 1
QuickSort(a, 1, n)

print("After sorting:", *a[1:n + 1])