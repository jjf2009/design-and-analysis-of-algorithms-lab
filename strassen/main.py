def add_matrix(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]

    return C


def subtract_matrix(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]

    return C


def Strassen(A, B):

    n = len(A)

    # Base case
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    # Find middle
    mid = n // 2

    # Divide A into four submatrices
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]

    # Divide B into four submatrices
    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]

    # P = (A11 + A22)(B11 + B22)
    P = Strassen(
        add_matrix(A11, A22),
        add_matrix(B11, B22)
    )

    # Q = (A21 + A22)B11
    Q = Strassen(
        add_matrix(A21, A22),
        B11
    )

    # R = A11(B12 - B22)
    R = Strassen(
        A11,
        subtract_matrix(B12, B22)
    )

    # S = A22(B21 - B11)
    S = Strassen(
        A22,
        subtract_matrix(B21, B11)
    )

    # T = (A11 + A12)B22
    T = Strassen(
        add_matrix(A11, A12),
        B22
    )

    # U = (A21 - A11)(B11 + B12)
    U = Strassen(
        subtract_matrix(A21, A11),
        add_matrix(B11, B12)
    )

    # V = (A12 - A22)(B21 + B22)
    V = Strassen(
        subtract_matrix(A12, A22),
        add_matrix(B21, B22)
    )

    # C11 = P + S - T + V
    C11 = add_matrix(
        subtract_matrix(
            add_matrix(P, S),
            T
        ),
        V
    )

    # C12 = R + T
    C12 = add_matrix(R, T)

    # C21 = Q + S
    C21 = add_matrix(Q, S)

    # C22 = P + R - Q + U
    C22 = add_matrix(
        subtract_matrix(
            add_matrix(P, R),
            Q
        ),
        U
    )

    # Combine C11, C12, C21, C22
    C = []

    for i in range(mid):
        C.append(C11[i] + C12[i])

    for i in range(mid):
        C.append(C21[i] + C22[i])

    return C


# --------------------------------
# Input
# --------------------------------

print("Enter size of matrix:")
n = int(input().strip())

print("Enter Matrix A:")

A = []

for i in range(n):
    row = list(map(int, input().strip().split()))
    A.append(row)

print("Enter Matrix B:")

B = []

for i in range(n):
    row = list(map(int, input().strip().split()))
    B.append(row)


# --------------------------------
# Strassen Matrix Multiplication
# --------------------------------

C = Strassen(A, B)


# --------------------------------
# Output
# --------------------------------

print("\nResult:")

for row in C:
    print(*row)