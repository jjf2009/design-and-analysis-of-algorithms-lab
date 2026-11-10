import heapq
import matplotlib.pyplot as plt


class Node:
    def __init__(self, level, profit, weight, bound, taken):
        self.level = level      # index of the item decided at this node
        self.profit = profit    # profit accumulated so far
        self.weight = weight    # weight accumulated so far
        self.bound = bound      # upper bound on profit reachable below this node
        self.taken = taken      # list of chosen item indexes

    # heapq is a min-heap; reverse the comparison so the highest bound is popped first
    # (Least-Cost / best-first branch and bound).
    def __lt__(self, other):
        return self.bound > other.bound


def upper_bound(node, n, capacity, w, p):
    # Relax to the fractional knapsack from the current level to get the bound.
    if node.weight >= capacity:
        return 0
    bound = node.profit
    total_weight = node.weight
    j = node.level + 1
    while j < n and total_weight + w[j] <= capacity:
        total_weight += w[j]
        bound += p[j]
        j += 1
    if j < n:
        bound += (capacity - total_weight) * (p[j] / w[j])
    return bound


# ---- bookkeeping for the drawing only (does not affect the algorithm) ----
tree_nodes = {}   # id -> {"label", "status"}
tree_edges = []   # (parent_id, child_id, "include"/"exclude")


def record(node, parent_id, edge_label, order, status):
    node.id = len(tree_nodes)
    if node.level == -1:
        label = f"Start\nUB={node.bound:.1f}"
    else:
        label = (f"Item {order[node.level] + 1}\n"
                 f"P={node.profit} W={node.weight}\nUB={node.bound:.1f}")
    tree_nodes[node.id] = {"label": label, "status": status}
    if parent_id is not None:
        tree_edges.append((parent_id, node.id, edge_label))


def knapsack_bb(w, p, capacity, n):
    # Items must be ordered by profit/weight ratio, descending.
    order = sorted(range(n), key=lambda i: p[i] / w[i], reverse=True)
    w = [w[i] for i in order]
    p = [p[i] for i in order]

    root = Node(-1, 0, 0, 0, [])
    root.bound = upper_bound(root, n, capacity, w, p)
    record(root, None, "", order, "expanded")
    heap = [root]
    max_profit = 0
    best_taken = []
    best_id = None

    while heap:
        node = heapq.heappop(heap)
        if node.bound <= max_profit:      # prune: cannot beat the best found
            tree_nodes[node.id]["status"] = "pruned"
            continue
        tree_nodes[node.id]["status"] = "expanded"
        level = node.level + 1
        if level >= n:
            continue

        # Branch 1: include item[level]
        with_w = node.weight + w[level]
        with_p = node.profit + p[level]
        is_best = False
        if with_w <= capacity and with_p > max_profit:
            max_profit = with_p
            best_taken = node.taken + [level]
            is_best = True
        inc = Node(level, with_p, with_w, 0, node.taken + [level])
        inc.bound = upper_bound(inc, n, capacity, w, p)
        infeasible = with_w > capacity
        record(inc, node.id, "include", order,
               "pruned" if (infeasible or inc.bound <= max_profit) else "live")
        if is_best:
            best_id = inc.id
        if inc.bound > max_profit:
            heapq.heappush(heap, inc)

        # Branch 2: exclude item[level]
        exc = Node(level, node.profit, node.weight, 0, node.taken)
        exc.bound = upper_bound(exc, n, capacity, w, p)
        record(exc, node.id, "exclude", order,
               "pruned" if exc.bound <= max_profit else "live")
        if exc.bound > max_profit:
            heapq.heappush(heap, exc)

    # Map the chosen (reordered) indexes back to the original item numbers.
    chosen = sorted(order[i] + 1 for i in best_taken)
    return max_profit, chosen, best_id


def draw_tree(best_id, max_profit, chosen, capacity):
    """Draw the branch and bound state-space tree."""
    children = {}
    parent = {}
    for a, b, _ in tree_edges:
        children.setdefault(a, []).append(b)
        parent[b] = a

    # Simple tidy layout: leaves get consecutive x, parents sit above their children.
    pos = {}
    counter = [0]

    def place(u, depth):
        kids = children.get(u, [])
        if not kids:
            x = counter[0]
            counter[0] += 1
        else:
            xs = [place(k, depth + 1) for k in kids]
            x = sum(xs) / len(xs)
        pos[u] = (x, -depth)
        return x

    place(0, 0)

    # Nodes on the path from the root to the best solution are shown in green.
    best_path = set()
    u = best_id
    while u is not None:
        best_path.add(u)
        u = parent.get(u)

    colors = {"expanded": "#3b82f6", "live": "#9ca3af", "pruned": "#ef4444"}

    width = max(12, counter[0] * 1.3)
    fig, ax = plt.subplots(figsize=(width, 8))

    for a, b, label in tree_edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.plot([x1, x2], [y1, y2], color="#6b7280", linewidth=1.2, zorder=1)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, label[:3], fontsize=7,
                color="#374151", ha="center",
                bbox={"fc": "white", "ec": "none", "pad": 0.5})

    for nid, info in tree_nodes.items():
        x, y = pos[nid]
        c = "#22c55e" if nid in best_path else colors[info["status"]]
        ax.scatter(x, y, s=260, color=c, edgecolor="#1f2937", zorder=2)
        ax.text(x, y - 0.12, info["label"], ha="center", va="top", fontsize=7)

    ax.set_title(f"Knapsack Branch and Bound Tree  |  Max profit = {max_profit}, "
                 f"items {chosen}, capacity {capacity}")
    ax.axis("off")

    # Legend
    for label, c in [("Best path", "#22c55e"), ("Expanded", "#3b82f6"),
                     ("Pruned / infeasible", "#ef4444"), ("Not expanded", "#9ca3af")]:
        ax.scatter([], [], s=120, color=c, edgecolor="#1f2937", label=label)
    ax.legend(loc="upper right")

    ax.margins(0.08)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    profit = [39, 45, 12, 22, 25, 23]
    weight = [3, 4, 2, 6, 7, 8]
    M = 17
    n = len(profit)

    max_profit, chosen, best_id = knapsack_bb(weight, profit, M, n)
    print(f"Maximum profit: {max_profit}")
    print(f"Items chosen: {chosen}")
    print(f"Total weight: {sum(weight[i - 1] for i in chosen)} / {M}")

    draw_tree(best_id, max_profit, chosen, M)