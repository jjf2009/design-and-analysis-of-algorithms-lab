INF = float('inf')
N = 15 
stages = [
    [1],
    [2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14],
    [15],
]


matrix = [
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # 0 (pad)
    [0,  0, 10,  3,  5,  9,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # 1
    [0,  0,  0,  0,  0,  0, 13, 14, 11,  6,  2,  0,  0,  0,  0,  0],  # 2
    [0,  0,  0,  0,  0,  0,  9,  0, 13,  8,  0,  0,  0,  0,  0,  0],  # 3
    [0,  0,  0,  0,  0,  0,  7, 15,  8,  0,  0,  0,  0,  0,  0,  0],  # 4
    [0,  0,  0,  0,  0,  0,  7,  4,  2,  1,  2,  0,  0,  0,  0,  0],  # 5
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11,  0,  3,  5,  0],  # 6
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 14, 12, 10,  2,  0],  # 7
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4,  9,  0,  7,  0],  # 8
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  5,  2,  7, 10,  0],  # 9
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2,  8,  1, 10,  0],  # 10
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3],  # 11
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1],  # 12
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4],  # 13
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3],  # 14
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # 15
]


def forward_approach():
    """cost(i) = min over edges i->j of ( c(i,j) + cost(j) ), computed from sink back to source."""
    cost = [INF] * (N + 1)
    d = [0] * (N + 1)
    cost[N] = 0

    print("FORWARD APPROACH")
    print("-" * 40)
    for i in range(N - 1, 0, -1):
        options = []
        for j in range(i + 1, N + 1):
            if matrix[i][j] != 0:
                total = matrix[i][j] + cost[j]
                options.append((j, matrix[i][j], cost[j], total))
                if total < cost[i]:
                    cost[i] = total
                    d[i] = j
        terms = ", ".join(f"{c}+{cj}" for _, c, cj, _ in options)
        print(f"cost({i:2d}) = min({terms}) = {cost[i]}  (d = {d[i]})")

    path = [1]
    while path[-1] != N:
        path.append(d[path[-1]])
    return cost[1], path


def backward_approach():
    """bcost(j) = min over edges i->j of ( bcost(i) + c(i,j) ), computed from source forward to sink."""
    bcost = [INF] * (N + 1)
    d = [0] * (N + 1)
    bcost[1] = 0

    print("\nBACKWARD APPROACH")
    print("-" * 40)
    for j in range(2, N + 1):
        options = []
        for i in range(1, j):
            if matrix[i][j] != 0:
                total = bcost[i] + matrix[i][j]
                options.append((i, bcost[i], matrix[i][j], total))
                if total < bcost[j]:
                    bcost[j] = total
                    d[j] = i
        terms = ", ".join(f"{b}+{c}" for _, b, c, _ in options)
        print(f"bcost({j:2d}) = min({terms}) = {bcost[j]}  (d = {d[j]})")

    path = [N]
    while path[-1] != 1:
        path.append(d[path[-1]])
    path.reverse()
    return bcost[N], path


if __name__ == "__main__":
    f_cost, f_path = forward_approach()
    print("\nForward  -> Min cost:", f_cost, "| Path:", " -> ".join(map(str, f_path)))

    b_cost, b_path = backward_approach()
    print("\nBackward -> Min cost:", b_cost, "| Path:", " -> ".join(map(str, b_path)))