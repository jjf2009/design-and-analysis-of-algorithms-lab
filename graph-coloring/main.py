import matplotlib.pyplot as plt
import networkx as nx

count = 0
solutions = []


def NextValue(graph, x, k, m, n):
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
    global count
    while True:
        NextValue(graph, x, k, m, n)
        if x[k] == 0:
            return
        if k == n:
            count += 1
            solutions.append(x[1:].copy())
            print(f"Colouring {count}: {x[1:]}")
        else:
            MColoring(graph, x, k + 1, m, n)


def draw_coloring(graph, colouring, n, title):
    """Draw the graph with each vertex filled in its assigned colour."""
    palette = {1: "#ef4444", 2: "#3b82f6", 3: "#22c55e",
               4: "#eab308", 5: "#a855f7", 6: "#f97316"}

    G = nx.Graph()
    G.add_nodes_from(range(1, n + 1))
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if graph[i][j] == 1:
                G.add_edge(i, j)

    pos = nx.spring_layout(G, seed=7)
    node_colors = [palette[colouring[v - 1]] for v in G.nodes]

    plt.figure(figsize=(6, 5))
    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            node_size=900, font_size=14, font_color="white",
            font_weight="bold", edge_color="#6b7280", width=2)
    plt.title(title)
    plt.show()


if __name__ == "__main__":
    # Static graph:
    # 1: 2, 4
    # 2: 1, 3, 4, 5
    # 3: 2, 5
    # 4: 1, 2
    # 5: 2, 3
    n = 5
    m = 3
    graph = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0],
    ]

    x = [0] * (n + 1)
    MColoring(graph, x, 1, m, n)

    if count == 0:
        print(f"The graph cannot be coloured with {m} colours.")
    else:
        print(f"\nTotal distinct colourings: {count}")
        draw_coloring(graph, solutions[0], n, f"{m}-Colouring of the Graph (solution 1)")