# Global array
a = []


def MaxMin(i, j, max, min):

    # Small(P)
    if i == j:
        max = a[i]
        min = a[i]

        print(f"{i} {j} {max} {min}")

    # Another case of Small(P)
    elif i == j - 1:

        if a[i] < a[j]:
            max = a[j]
            min = a[i]
        else:
            max = a[i]
            min = a[j]

        print(f"{i} {j} {max} {min}")

    else:
        # Divide P into subproblems
        mid = (i + j) // 2

        # Solve left subproblem
        max1, min1 = MaxMin(i, mid, max, min)

        # Solve right subproblem
        max2, min2 = MaxMin(mid + 1, j, max, min)

        # Combine the solutions
        if max < max1:
            max = max1

        if max < max2:
            max = max2

        if min > min1:
            min = min1

        if min > min2:
            min = min2

    return max, min


# Input
print("Enter Size:")
n = int(input().strip())

print("Enter Elements:")

# Add dummy element at index 0
# This makes the array 1-indexed
a = [0] + list(map(int, input().strip().split()))

# Initial values
max = 0
min = 0

print("i j max min")

# Algorithm starts from index 1
# and ends at index n
max, min = MaxMin(1, n, max, min)

print("Maximum:", max)
print("Minimum:", min)