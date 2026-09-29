import heapq


class Node:
    def __init__(self, level, profit, weight, bound, taken):
        self.level = level      # index of the item decided at this node
        self.profit = profit    # profit accumulated so far
        self.weight = weight    # weight accumulated so far
        self.bound = bound      # upper bound on profit reachable below this node
        self.taken = taken      # list of chosen item indexes

    # heapq is a min-heap; negate the bound so the highest bound is popped first
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


if __name__ == "__main__":
    print("Enter number of objects:")
    n = int(input().strip())
    print("Enter weights:")
    w = list(map(float, input().strip().split()))
    print("Enter profits:")
    p = list(map(float, input().strip().split()))
    print("Enter knapsack capacity:")
    capacity = float(input().strip())

    profit, chosen = knapsack_bb(w, p, capacity, n)
    print("\nMaximum profit:", profit)
    print("Items selected (1-indexed):", chosen)
