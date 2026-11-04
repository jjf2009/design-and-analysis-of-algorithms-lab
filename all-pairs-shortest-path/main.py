INF = float("inf")

def print_matrix(A, n, label):
    print(f"\n{label}")
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            row.append("INF" if A[i][j] == INF else str(A[i][j]))
        print(" ".join(f"{x:>4}" for x in row))

def AllPaths(cost, n):

    # Copy the cost matrix into A (original matrix remains unchanged)
    # A[i][j] stores the shortest distance from node i to node j
    A = [[cost[i][j] for j in range(n + 1)] for i in range(n + 1)]

    # P[i][j] stores the predecessor (parent) of node j on the shortest path from i to j
    P = [[0] * (n + 1) for _ in range(n + 1)]

    # Initialize the predecessor matrix using direct edges
    for i in range(1, n + 1):
        for j in range(1, n + 1):

            # If i and j are different nodes and a direct edge exists,
            # the predecessor of j is i
            if i != j and cost[i][j] != INF:
                P[i][j] = i

    # Display initial distance matrix (direct edge costs)
    print_matrix(A, n, "A(0) - direct edges")

    # Display initial predecessor matrix
    print_matrix(P, n, "P(0) - parent")

    # Consider each node k as an intermediate vertex
    for k in range(1, n + 1):

        # Check every source node i
        for i in range(1, n + 1):

            # Check every destination node j
            for j in range(1, n + 1):

                # Check if the path i -> k -> j is shorter than i -> j
                if A[i][k] + A[k][j] < A[i][j]:

                    # Update the shortest distance through intermediate node k
                    A[i][j] = A[i][k] + A[k][j]

                    # Update predecessor of j to the predecessor of j on path k -> j
                    P[i][j] = P[k][j]

        # Display updated distance matrix after considering vertex k
        print_matrix(A, n, f"A({k}) - allowing intermediate vertex {k}")

        # Display updated predecessor matrix
        print_matrix(P, n, f"P({k}) - parent")

    # Return the final shortest-distance matrix and predecessor matrix
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