count = 0


def NextValue(graph, x, k, m, n):
    # Choose the next admissible colour for vertex k, or 0 if none remains.
    while True:
        x[k] = (x[k] + 1) % (m + 1)
        if x[k] == 0:
            return
        ok = True
        for j in range(1, n + 1):
            if graph[k][j] == 1 and x[k] == x[j]:  # adjacent, same colour
                ok = False
                break
        if ok:
            return


def MColoring(graph, x, k, m, n):
    # Backtracking m-colouring: assign a colour to vertex k, then recurse.
    global count
    while True:
        NextValue(graph, x, k, m, n)
        if x[k] == 0:
            return
        if k == n:
            count += 1
            print(f"Colouring {count}: {x[1:]}")
        else:
            MColoring(graph, x, k + 1, m, n)


if __name__ == "__main__":
    print("Enter number of vertices:")
    n = int(input().strip())
    print("Enter number of colours m:")
    m = int(input().strip())
    print(f"Enter the {n}x{n} adjacency matrix rows (0/1):")
    graph = [[0] * (n + 1)]
    for _ in range(n):
        row = [0] + list(map(int, input().strip().split()))
        graph.append(row)

    x = [0] * (n + 1)
    MColoring(graph, x, 1, m, n)
    if count == 0:
        print(f"The graph cannot be coloured with {m} colours.")
    else:
        print(f"\nTotal distinct colourings: {count}")
