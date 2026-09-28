import heapq
parent = []
def Find(i):
    while parent[i] >= 0:
        i = parent[i]
    return i
def Union(j, k):
    parent[j] = k
def Kruskal(edges, n):
    global parent
    heap = list(edges)
    heapq.heapify(heap)
    for i in range(1, n + 1):
        parent[i] = -1
    i = 0
    mincost = 0.0
    t = [[0, 0] for _ in range(n)]
    while i < n - 1 and heap:
        c, u, v = heapq.heappop(heap)
        j = Find(u)
        k = Find(v)
        if j != k:
            i = i + 1
            t[i][0] = u
            t[i][1] = v
            mincost = mincost + c
            Union(j, k)
    if i != n - 1:
        print("No spanning tree")
        return None, None
    return mincost, t
print("Enter number of vertices:")
n = int(input().strip())
print("Enter number of edges:")
e = int(input().strip())
parent = [-1] * (n + 1)
edges = []
print("Enter edges (u v w):")
for _ in range(e):
    u, v, w = map(int, input().strip().split())
    edges.append((w, u, v))
mincost, t = Kruskal(edges, n)
if mincost is not None:
    print("\nEdges in the minimum spanning tree:")
    for i in range(1, n):
        print(t[i][0], t[i][1])
    print("Minimum cost:", mincost)
