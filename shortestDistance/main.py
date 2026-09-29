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
    P = [0]*(n+1)
    for i in range(1, n + 1):
        S[i] = False
        P[i]=v
        dist[i] = cost[v][i]
    S[v] = True
    dist[v] = 0
    print("\nINITIAL")
    print("S    =", print_array(S, n))
    print("DIST =", print_array(dist, n))
    for num in range(2, n):
        u = 0
        minu = INF
        for w in range(1, n + 1):
            if not S[w] and dist[w] < minu:
                minu = dist[w]
                u = w
        S[u] = True
        for w in range(1, n + 1):
            if not S[w] and cost[u][w] != INF:
                if dist[w] > dist[u] + cost[u][w]:
                    P[w]=u
                    dist[w] = dist[u] + cost[u][w]

        print("\nSTEP", num)
        print("u =", u)
        print("S    =", print_array(S, n))
        print("DIST =", print_array(dist, n))

    print("PATH =",print_array(P,n))    


cost = [
    [INF,INF,INF,INF,INF,INF,INF,INF],
    [INF,  0,   INF,  INF,  28,  INF,  29,  29,  24],
    [INF, INF,    0,   14,  30,  27,  INF,  26, INF],
    [INF, 25,  INF,    0,   31,  23, 17, 28,  17],
    [INF, 22,   34,   27,   0,   20,  INF, 10, 17],
    [INF, 15,  INF,  14,  INF,   0,  INF,  INF,  23],
    [INF, INF,  INF,  INF,  32,  23,   0,  29,  INF],
    [INF, INF,   32,   32,   13,  22,  11,   0,  23],
    [INF, 29,   14,   14,   INF,  INF,  INF, INF,   0]
]

n = 8

print("Enter source vertex:")
v = int(input())

dist = [INF] * (n + 1)

ShortestPaths(v, cost, dist, n)


