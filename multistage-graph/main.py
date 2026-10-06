from collections import deque
INF = float("inf")
V = [1, 2, 3, 4, 5]
source = 1
sink = 2
edges = {
    (1, 3): 7,
    (1, 5): 10,
    (3, 4): 3,
    (3, 5): 8,
    (4, 5): 2,
    (4, 2): 8,
    (5, 2): 5,
}
adj = {v: [] for v in V}
radj = {v: [] for v in V}
indeg = {v: 0 for v in V}
for (u, v), w in edges.items():
    adj[u].append((v, w))
    radj[v].append((u, w))
    indeg[v] += 1
q = deque([v for v in V if indeg[v] == 0])
order = []
deg = dict(indeg)
while q:
    u = q.popleft()
    order.append(u)
    for v, w in adj[u]:
        deg[v] -= 1
        if deg[v] == 0:
            q.append(v)
stageno = {v: 1 for v in V}
for u in order:
    for v, w in adj[u]:
        if stageno[u] + 1 > stageno[v]:
            stageno[v] = stageno[u] + 1
k = max(stageno.values())
stages = {}
for v in V:
    stages.setdefault(stageno[v], []).append(v)
cost = {v: INF for v in V}
d = {v: 0 for v in V}
cost[sink] = 0
for u in reversed(order):
    for v, w in adj[u]:
        if w + cost[v] < cost[u]:
            cost[u] = w + cost[v]
            d[u] = v
bcost = {v: INF for v in V}
p = {v: 0 for v in V}
bcost[source] = 0
for v in order:
    for u, w in radj[v]:
        if bcost[u] + w < bcost[v]:
            bcost[v] = bcost[u] + w
            p[v] = u
print("FORWARD PASS (cost = min cost from vertex to sink)")
for s in range(k, 0, -1):
    print(f"stage:{s}")
    for v in sorted(stages[s]):
        print(f"Cost({s},{v}) = {cost[v]}")
        print(f"parent({s},{v}) = {d[v]}")
print("\nBACKWARD PASS (Bcost = min cost from source to vertex)")
for s in range(1, k + 1):
    print(f"stage:{s}")
    for v in sorted(stages[s]):
        print(f"Bcost({s},{v}) = {bcost[v]}")
        print(f"parent({s},{v}) = {p[v]}")
path = [source]
v = source
while v != sink:
    v = d[v]
    path.append(v)
print("\nMinimum cost path:", " -> ".join(map(str, path)))
print("Minimum cost:", cost[source])
