INF = float("inf")
def print_array(arr, n):
    result = []
    for i in range(1, n + 1):
        if arr[i] == INF:
            result.append("INF")
        else:
            result.append(str(arr[i]))
    return "[ " + " ".join(result) + " ]"

def ShortestPaths(v, cost, dist, n):
    S = [False] * (n + 1)
    for i in range(1, n + 1):
        dist[i] = cost[v][i]
    S[v] = True
    dist[v] = 0
    print("\nINITIAL")
    print("S    =", print_array(S, n))
    print("DIST =", print_array(dist, n))
    for step in range(1, n):
        u = 0
        mincost = INF
        for w in range(1, n + 1):
            if not S[w] and dist[w] < mincost:
                mincost = dist[w]
                u = w
        if u == 0:
            break
        S[u] = True
        for w in range(1, n + 1):
            if not S[w] and cost[u][w] != INF:
                if dist[w] > dist[u] + cost[u][w]:
                    dist[w] = dist[u] + cost[u][w]

        # Display only the required information
        print("\nSTEP", step)
        print("u =", u)
        print("MINCOST =", mincost)
        print("S    =", print_array(S, n))
        print("DIST =", print_array(dist, n))


# ==========================================================
# ADJACENCY MATRIX
# ==========================================================

cost = [

    #       1     2     3     4     5     6     7     8
    [INF,  0,   INF,  70,  INF,  INF,  51,  40,  48],
    [INF, 92,    0,   INF,  20,  13,  14,  34, INF],
    [INF, INF,  56,    0,   INF,  INF, INF, INF,  46],
    [INF, 21,   53,   INF,   0,   13,  INF, INF, INF],
    [INF, INF,  INF,  INF,  74,   0,  INF,  93,  22],
    [INF, INF,  60,   18,  INF,  INF,   0,  INF,  57],
    [INF, 72,   54,   55,   82,  INF,  33,   0,  71],
    [INF, 26,   53,   50,   30,  INF,  43, INF,   0]
]

n = 8

print("Enter source vertex:")
v = int(input())

dist = [INF] * (n + 1)

ShortestPaths(v, cost, dist, n)