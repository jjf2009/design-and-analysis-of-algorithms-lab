INF = float("inf")


def print_matrix(A, n, label):
    print(f"\n{label}")
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            row.append("INF" if A[i][j] == INF else str(A[i][j]))
        print(" ".join(f"{x:>4}" for x in row))


def AllPaths(cost, n):
    # Floyd-Warshall dynamic programming: A[i][j] holds the shortest path from
    # i to j using intermediate vertices drawn from {1..k} as k increases.
    A = [[cost[i][j] for j in range(n + 1)] for i in range(n + 1)]
    print_matrix(A, n, "A(0) - direct edges")
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if A[i][k] + A[k][j] < A[i][j]:
                    A[i][j] = A[i][k] + A[k][j]
        print_matrix(A, n, f"A({k}) - allowing intermediate vertex {k}")
    return A


if __name__ == "__main__":
    n = 3
    cost = [
        [0, 0, 0, 0],
        [0, 0, 4, 11],
        [0, 6, 0, 2],
        [0, 3, INF, 0],
    ]
    AllPaths(cost, n)
