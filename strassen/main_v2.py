import random
import time

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

    if n < 2 or n & (n - 1):
        raise ValueError("Strassen multiplication requires a power-of-two size of at least 2")

    if n == 2:
        return [
            [
                A[0][0] * B[0][0] + A[0][1] * B[1][0],
                A[0][0] * B[0][1] + A[0][1] * B[1][1],
            ],
            [
                A[1][0] * B[0][0] + A[1][1] * B[1][0],
                A[1][0] * B[0][1] + A[1][1] * B[1][1],
            ],
        ]

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


def normal_multiply(A, B):
    """Multiply two square matrices using the standard triple-loop method."""

    n = len(A)
    C = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]

    return C


def generate_matrix(n):
    """Generate an n-by-n matrix containing random integers from 0 through 9."""

    return [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]


def copy_matrix(matrix):
    return [row[:] for row in matrix]


def measure(multiply, A, B, clock):
    """Measure one multiplication, excluding input copying and output printing."""

    start = clock()
    multiply(A, B)
    return clock() - start


def create_datasets():
    sizes = (32, 64, 128, 256, 512)
    return {
        n: (generate_matrix(n), generate_matrix(n))
        for n in sizes
    }


def benchmark(datasets, clock):
    results = {}

    for n, (A, B) in datasets.items():
        normal_A = copy_matrix(A)
        normal_B = copy_matrix(B)
        strassen_A = copy_matrix(A)
        strassen_B = copy_matrix(B)

        results[n] = {
            "Normal Multiplication": measure(normal_multiply, normal_A, normal_B, clock),
            "Strassen Multiplication": measure(Strassen, strassen_A, strassen_B, clock),
        }
    return results


def print_table(title, results):
    print(f"{title}:")
    print("n    | Normal Multiplication | Strassen Multiplication")

    for n, values in results.items():
        print(
            f"{n:<4} | "
            f"{values['Normal Multiplication']:.6f}              | "
            f"{values['Strassen Multiplication']:.6f}"
        )

    print()


def main():
    datasets = create_datasets()

    method_1_results = benchmark(datasets, time.time)
    method_2_results = benchmark(datasets, time.perf_counter)

    print_table("Method 1", method_1_results)
    print_table("Method 2", method_2_results)


if __name__ == "__main__":
    main()
