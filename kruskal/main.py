INF = float('inf')

def find(i, parent):
    while parent[i] >= 0:
        i = parent[i]
    return i

def union(i, j, parent):
    parent[i] = j

def adjust(A, i, n):
    j = 2 * i
    item = A[i]
    while j <= n:
        if j < n and A[j][0] > A[j + 1][0]:
            j += 1
        if item[0] <= A[j][0]:
            break
        A[j // 2] = A[j]
        j = 2 * j
    A[j // 2] = item

def heapify(A, n):
    for i in range(n // 2, 0, -1):
        adjust(A, i, n)

def delete(A, n):
    if n == 0:
        return None
    x = A[1]
    A[1] = A[n]
    adjust(A, 1, n - 1)
    return x

def print_t_table(t):
    print("t | 1 | 2 ")
    print("----------")
    for idx in range(1, len(t)):
        print(f"{idx} | {t[idx][1]} | {t[idx][2]}")

def kruskals(e, cost, n, t):
    A = [None]
    for u, v in e:
        A.append([cost[(u, v)], u, v])
    l = len(e)
    heapify(A, l)

    parent = [-1] * (n + 1)
    mincost = 0
    i = 0

    while i < n - 1 and l > 0:
        minEdge = delete(A, l)
        l -= 1
        if minEdge is None:
            break

        weight, u, v = minEdge
        j = find(u, parent)
        k = find(v, parent)

        if j != k:
            i += 1
            t[i][1], t[i][2] = u, v
            mincost += weight
            union(j, k, parent)
            
            print(f"Step {i}:")
            print(f"({u},{v})  Cost = {weight}  MinCost = {mincost}")
            print("parent : ", parent)
            print("t table :")
            print_t_table(t)
            print()

    if i != n - 1:
        print("No spanning tree")
    return mincost

if __name__ == "__main__":
    cost_matrix = [
        [INF, INF, INF,  96,  49,  81,  47,  92,  12,  10],
        [INF, INF, INF, INF,  31,  34,  87,  29,  73,  78],
        [INF,  96, INF, INF,  61,  50,  65,  64,  79,  73],
        [INF,  49,  31,  61, INF, INF,  63,  90,  80,  28],
        [INF,  81,  34,  50, INF, INF,  45,  92,  50, INF],
        [INF,  47,  87,  65,  63,  45, INF,  52,  29,  42],
        [INF,  93,  18,  88,  38,  11,  37,  85,  27,  39],
        [INF,  92,  29,  64,  90,  92,  52, INF, INF,  96],
        [INF,  92,  73,  79,  80,  50,  29, INF, INF,  59],
        [INF,  98,  72,  28, INF,  42,  39,  59,  34,  34],
    ]
    n = len(cost_matrix)
    e = []
    cost = {}
    for i in range(n):
        for j in range(i + 1, n):
            if cost_matrix[i][j] != INF:
                u, v = i + 1, j + 1
                e.append([u, v])
                cost[(u, v)] = cost_matrix[i][j]

    t = [[0, 0, 0] for _ in range(n)]

    mcost = kruskals(e, cost, n, t)

    print("Final t table:")
    print_t_table(t)
    print("\nMin cost = ", mcost)