
INF = float('inf')
N = 15

matrix = [
    [0]*16,
    [0,0,10,3,5,9,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,13,14,11,6,2,0,0,0,0,0],
    [0,0,0,0,0,0,9,0,13,8,0,0,0,0,0,0],
    [0,0,0,0,0,0,7,15,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,7,4,2,1,2,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,11,0,3,5,0],
    [0,0,0,0,0,0,0,0,0,0,0,14,12,10,2,0],
    [0,0,0,0,0,0,0,0,0,0,0,4,9,0,7,0],
    [0,0,0,0,0,0,0,0,0,0,0,5,2,7,10,0],
    [0,0,0,0,0,0,0,0,0,0,0,2,8,1,10,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [0]*16
]

def forward_approach():
    # cost(i) = minimum cost from node i to the destination N

    cost = [INF] * (N + 1)  # Stores minimum cost from each node to N
    d = [0] * (N + 1)       # Stores the next node in the minimum-cost path
    cost[N] = 0             # Destination cost is 0

    print("FORWARD APPROACH")
    print("-" * 40)

    # Calculate costs from the last node backwards to the first node
    for i in range(N - 1, 0, -1):

        options = []  # Stores all possible costs from node i

        # Check every node j that comes after node i
        for j in range(i + 1, N + 1):

            # Check whether an edge exists from i to j
            if matrix[i][j] != 0:

                # Total cost = edge cost + minimum cost from j to destination
                total = matrix[i][j] + cost[j]

                # Store destination, edge cost, remaining cost, and total cost
                options.append((j, matrix[i][j], cost[j], total))

                # Update minimum cost and next node if a cheaper path is found
                if total < cost[i]:
                    cost[i] = total
                    d[i] = j

        # Display all possible cost calculations
        terms = ", ".join(f"{c}+{cj}" for _, c, cj, _ in options)

        # Print minimum cost and the next node in the optimal path
        print(f"cost({i:2d}) = min({terms}) = {cost[i]}  (d = {d[i]})")

    # Start constructing the optimal path from source node 1
    path = [1]

    # Follow the stored next nodes until destination N is reached
    while path[-1] != N:
        path.append(d[path[-1]])

    # Return minimum cost from source and the complete optimal path
    return cost[1], path

# BACKWARD APPROACH
def backward():
    cost = [INF] * (N+1)
    d = [0] * (N+1)
    cost[1] = 0

    for j in range(2, N+1):
        for i in range(1, j):
            if matrix[i][j] != 0:
                cost[j] = min(cost[j],
                              cost[i] + matrix[i][j])
        for i in range(1, j):
            if matrix[i][j] != 0 and cost[j] == cost[i] + matrix[i][j]:
                d[j] = i
                break

    path = [N]
    while path[-1] != 1:
        path.append(d[path[-1]])

    path.reverse()
    print("Backward cost:", cost[N])
    print("Path:", path)


forward()
backward()
