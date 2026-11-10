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


def knapsack_bb(w, p, capacity, n):
    # Items must be ordered by profit/weight ratio, descending.
    order = sorted(range(n), key=lambda i: p[i] / w[i], reverse=True)
    w = [w[i] for i in order]
    p = [p[i] for i in order]

    root = Node(-1, 0, 0, 0, [])
    root.bound = upper_bound(root, n, capacity, w, p)
    heap = [root]
    max_profit = 0
    best_taken = []

    while heap:
        node = heapq.heappop(heap)
        if node.bound <= max_profit:      # prune: cannot beat the best found
            continue
        level = node.level + 1
        if level >= n:
            continue

        # Branch 1: include item[level]
        with_w = node.weight + w[level]
        with_p = node.profit + p[level]
        if with_w <= capacity and with_p > max_profit:
            max_profit = with_p
            best_taken = node.taken + [level]
        inc = Node(level, with_p, with_w, 0, node.taken + [level])
        inc.bound = upper_bound(inc, n, capacity, w, p)
        if inc.bound > max_profit:
            heapq.heappush(heap, inc)

        # Branch 2: exclude item[level]
        exc = Node(level, node.profit, node.weight, 0, node.taken)
        exc.bound = upper_bound(exc, n, capacity, w, p)
        if exc.bound > max_profit:
            heapq.heappush(heap, exc)

    # Map the chosen (reordered) indexes back to the original item numbers.
    chosen = sorted(order[i] + 1 for i in best_taken)
    return max_profit, chosen


def draw_solution(profit, weight, capacity, max_profit, chosen):
    """Bar chart of item profits: green = in the knapsack, grey = left out."""
    n = len(profit)
    items = list(range(1, n + 1))
    colors = ["#22c55e" if i in chosen else "#d1d5db" for i in items]
    used = sum(weight[i - 1] for i in chosen)

    plt.figure(figsize=(8, 5))
    bars = plt.bar(items, profit, color=colors, edgecolor="#1f2937")
    for bar, i in zip(bars, items):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
                 f"w = {weight[i - 1]}", ha="center", fontsize=10)

    plt.xticks(items, [f"Item {i}" for i in items])
    plt.ylabel("Profit")
    plt.title(f"0/1 Knapsack (Branch and Bound)\n"
              f"Max profit = {max_profit}, weight used = {used}/{capacity}")
    plt.ylim(0, max(profit) + 8)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    profit = [39, 45, 12, 22, 25, 23]
    weight = [3, 4, 2, 6, 7, 8]
    M = 17
    n = len(profit)

    max_profit, chosen = knapsack_bb(weight, profit, M, n)
    print(f"Maximum profit: {max_profit}")
    print(f"Items chosen: {chosen}")
    print(f"Total weight: {sum(weight[i - 1] for i in chosen)} / {M}")

    draw_solution(profit, weight, M, max_profit, chosen)