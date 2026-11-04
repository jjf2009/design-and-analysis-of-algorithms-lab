INF = float("inf")

def print_array(arr, n):
    result = []

    # Visit vertices from 1 to n
    for i in range(1, n + 1):

        # Display INF if the vertex is unreachable
        if arr[i] == INF:
            result.append("INF")
        else:
            result.append(str(arr[i]))

    # Return array as a formatted string
    return "[ " + " ".join(result) + " ]"


def ShortestPaths(v, cost, dist, n):

    # S[i] = True if vertex i is permanently visited
    S = [False] * (n + 1)

    # P[i] stores the predecessor (parent) of vertex i
    P = [0] * (n + 1)

    # Initialize distances using direct edges from source v
    for i in range(1, n + 1):
        S[i] = False
        P[i] = v
        dist[i] = cost[v][i]

    # Mark source vertex as visited
    S[v] = True

    # Distance from source to itself is zero
    dist[v] = 0

    # Display initial values
    print("\nINITIAL")
    print("S    =", print_array(S, n))
    print("DIST =", print_array(dist, n))

    # Repeat to select the next nearest unvisited vertex
    for num in range(2, n):

        u = 0
        minu = INF

        # Find the unvisited vertex with minimum distance
        for w in range(1, n + 1):
            if not S[w] and dist[w] < minu:
                minu = dist[w]
                u = w

        # Mark the selected vertex as permanently visited
        S[u] = True

        # Update distances to the remaining unvisited vertices
        for w in range(1, n + 1):

            # Check that w is unvisited and an edge u -> w exists
            if not S[w] and cost[u][w] != INF:

                # Check whether the path through u is shorter
                if dist[w] > dist[u] + cost[u][w]:

                    # Update predecessor of w to u
                    P[w] = u

                    # Update the shortest known distance to w
                    dist[w] = dist[u] + cost[u][w]

        # Display the current step's results
        print("\nSTEP", num)
        print("u =", u)
        print("S    =", print_array(S, n))
        print("DIST =", print_array(dist, n))

    # Display the predecessor array
    print("PATH =", print_array(P, n))


# Cost adjacency matrix (INF means no direct edge)
cost = [
    [INF, INF, INF, INF, INF, INF, INF, INF, INF],
    [INF,  0, INF, INF, 28, INF, 29, 29, 24],
    [INF, INF, 0, 14, 30, 27, INF, 26, INF],
    [INF, 25, INF, 0, 31, 23, 17, 28, 17],
    [INF, 22, 34, 27, 0, 20, INF, 10, 17],
    [INF, 15, INF, 14, INF, 0, INF, INF, 23],
    [INF, INF, INF, INF, 32, 23, 0, 29, INF],
    [INF, INF, 32, 32, 13, 22, 11, 0, 23],
    [INF, 29, 14, 14, INF, INF, INF, INF, 0]
]

n = 8

# Read the source vertex
print("Enter source vertex:")
v = int(input())

# Initialize all distances to infinity
dist = [INF] * (n + 1)

# Run Dijkstra's shortest-path algorithm
ShortestPaths(v, cost, dist, n)