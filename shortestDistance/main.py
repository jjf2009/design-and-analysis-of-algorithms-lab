INF = float("inf")
def ShortestPaths(v, cost, dist, n):
    S = [False] * (n + 1)
    for i in range(1, n + 1):
        S[i] = False
        dist[i] = cost[v][i]
    S[v] = True
    dist[v] = 0.0
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
                    dist[w] = dist[u] + cost[u][w]
print("Enter number of vertices:")
n = int(input().strip())
print("Enter number of edges:")
e = int(input().strip())
cost = [[INF] * (n + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    cost[i][i] = 0.0
print("Enter directed edges (u v w):")
for _ in range(e):
    u, v, w = map(int, input().strip().split())
    cost[u][v] = w
print("Enter source vertex:")
v = int(input().strip())
dist = [INF] * (n + 1)
ShortestPaths(v, cost, dist, n)
print("\nShortest distances from vertex", v)
for i in range(1, n + 1):
    print(i, dist[i])
