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
    # P[i][j] holds the predecessor of j on that shortest path.
    A = [[cost[i][j] for j in range(n + 1)] for i in range(n + 1)]
    P = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j and cost[i][j] != INF:
                P[i][j] = i
    print_matrix(A, n, "A(0) - direct edges")
    print_matrix(P, n, "P(0) - parent")
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if A[i][k] + A[k][j] < A[i][j]:
                    A[i][j] = A[i][k] + A[k][j]
                    P[i][j] = P[k][j]
        print_matrix(A, n, f"A({k}) - allowing intermediate vertex {k}")
        print_matrix(P, n, f"P({k}) - parent")
    return A, P



if __name__ == "__main__":
    n = 6
    cost = [
        [0,0,0,0,0,0,0],
        [INF,0, 12,43,7,24,5],
        [INF,9,0,42,27,8,28],
        [INF,31,25,0,34,20,21],
        [INF,7,14,15,0,29,11],
        [INF,21,14,15,0,29,11],
        [INF,20,14,12,27,14,0]
    ]
    A, P = AllPaths(cost, n)