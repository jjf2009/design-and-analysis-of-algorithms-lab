INF = float("inf")
def Prim(cost, n):
    t = [[0, 0] for _ in range(n)]
    mincost = 0
    k = l = 0
    minedge = INF
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if cost[i][j] < minedge:
                minedge = cost[i][j]
                k = i
                l = j
    mincost = cost[k][l]
    t[1][0] = k
    t[1][1] = l
    near = [0] * (n + 1)
    for i in range(1, n + 1):
        if cost[i][l] < cost[i][k]:
            near[i] = l
        else:
            near[i] = k
    near[k] = 0
    near[l] = 0
    for i in range(2, n):
        j = 0
        minj = INF
        for x in range(1, n + 1):
            if near[x] != 0 and cost[x][near[x]] < minj:
                minj = cost[x][near[x]]
                j = x
        t[i][0] = j
        t[i][1] = near[j]
        mincost = mincost + cost[j][near[j]]
        near[j] = 0
        for x in range(1, n + 1):
            if near[x] != 0 and cost[x][near[x]] > cost[x][j]:
                near[x] = j
    return mincost, t
print("Enter number of vertices:")
n = int(input().strip())
print("Enter number of edges:")
e = int(input().strip())
cost = [[INF] * (n + 1) for _ in range(n + 1)]
print("Enter edges (u v w):")
for _ in range(e):
    u, v, w = map(int, input().strip().split())
    cost[u][v] = w
    cost[v][u] = w
mincost, t = Prim(cost, n)
print("\nEdges in the minimum spanning tree:")
for i in range(1, n):
    print(t[i][0], t[i][1])
print("Minimum cost:", mincost)
