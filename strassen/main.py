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
    if n == 1:
        return [[A[0][0] * B[0][0]]]
    mid = n // 2
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]
    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]
    P = Strassen(add_matrix(A11, A22), add_matrix(B11, B22))
    Q = Strassen(add_matrix(A21, A22), B11)
    R = Strassen(A11, subtract_matrix(B12, B22))
    S = Strassen(A22, subtract_matrix(B21, B11))
    T = Strassen(add_matrix(A11, A12), B22)
    U = Strassen(subtract_matrix(A21, A11), add_matrix(B11, B12))
    V = Strassen(subtract_matrix(A12, A22), add_matrix(B21, B22))
    C11 = add_matrix(subtract_matrix(add_matrix(P, S), T), V)
    C12 = add_matrix(R, T)
    C21 = add_matrix(Q, S)
    C22 = add_matrix(subtract_matrix(add_matrix(P, R), Q), U)
    C = []
    for i in range(mid):
        C.append(C11[i] + C12[i])
    for i in range(mid):
        C.append(C21[i] + C22[i])
    return C
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
C = Strassen(A, B)
print("\nResult:")
for row in C:
    print(*row)
