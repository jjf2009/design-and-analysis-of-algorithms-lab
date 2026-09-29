INF = float("inf")


def MultistageForward(cost, stages, n, stage_of):
    # cost[i][j] is the edge weight i -> j (INF if no edge). Vertices are
    # 1-indexed; vertex 1 is the source, vertex n is the sink.
    bcost = [INF] * (n + 1)
    d = [0] * (n + 1)
    bcost[n] = 0
    for j in range(n - 1, 0, -1):
        best = INF
        for r in range(1, n + 1):
            if cost[j][r] != INF and cost[j][r] + bcost[r] < best:
                best = cost[j][r] + bcost[r]
                d[j] = r
        bcost[j] = best
    # Reconstruct the minimum-cost path stage by stage.
    path = [1]
    v = 1
    while v != n:
        v = d[v]
        path.append(v)
    return bcost[1], path


if __name__ == "__main__":
    # Classic 5-stage, 12-vertex multistage graph (Horowitz-Sahni).
    n = 12
    edges = {
        (1, 2): 9, (1, 3): 7, (1, 4): 3, (1, 5): 2,
        (2, 6): 4, (2, 7): 2, (2, 8): 1,
        (3, 6): 2, (3, 7): 7,
        (4, 8): 11,
        (5, 7): 11, (5, 8): 8,
        (6, 9): 6, (6, 10): 5,
        (7, 9): 4, (7, 10): 3,
        (8, 10): 5, (8, 11): 6,
        (9, 12): 4,
        (10, 12): 2,
        (11, 12): 5,
    }
    cost = [[INF] * (n + 1) for _ in range(n + 1)]
    for (u, v), w in edges.items():
        cost[u][v] = w

    mincost, path = MultistageForward(cost, 5, n, None)
    print("Minimum cost:", mincost)
    print("Path:", " -> ".join(map(str, path)))
