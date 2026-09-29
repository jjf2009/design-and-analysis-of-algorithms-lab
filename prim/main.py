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


cost = [
    [INF, INF ,INF ,96  ,49   ,81,  47,  92,  12,  10],
    [INF, INF ,INF ,INF ,31   ,34,  87,  29,  73,  78],
    [INF, 96  ,INF ,INF ,61   ,50,  65,  64,  79,  73],
    [INF, 49  ,31  ,61  ,INF  ,INF, 63,  90,  80,  28],
    [INF, 81  ,34  ,50  ,INF  ,INF, 45,  92,  50,  INF],
    [INF, 47  ,87  ,65  ,63   ,45,  INF, 52,  29,  42],
    [INF, 93  ,18  ,88  ,38   ,11,  37,  85,  27,  39],
    [INF, 92  ,29  ,64  ,90   ,92,  52,  INF, INF, 96],
    [INF, 92  ,73  ,79  ,80   ,50,  29,  INF, INF, 59],
    [INF, 98  ,72  ,28  ,INF  ,42,  39,  59,  34,  34],
    [INF, INF ,INF ,INF]
]
