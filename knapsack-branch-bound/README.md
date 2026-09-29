# 0/1 Knapsack (Branch and Bound)

**DAA Lab — Experiment 13: 0/1 Knapsack using Branch and Bound (LC strategy).**

`main.py` solves the 0/1 knapsack problem — each item taken whole or not at all —
with **least-cost (LC) branch and bound**, exploring the most promising node
first and pruning any node whose optimistic bound cannot beat the best solution
found so far.

## Algorithm

- Items are ordered by profit/weight ratio (descending).
- Each `Node` fixes the include/exclude decision for one more item. Its **bound**
  is the profit obtainable by relaxing the rest of the problem to the *fractional*
  knapsack — an upper bound on any completion of that node.
- A max-heap (via negated bound) always expands the node with the highest bound
  (the LC rule). Each node branches into *include* and *exclude* children; a child
  is queued only if its bound exceeds the best profit so far.

## Run

```bash
python3 main.py
```

Enter the object count, weights, profits, and capacity.

## Complexity

Worst case `O(2ⁿ)`, but bounding typically explores far fewer nodes than brute
force. The fractional bound is what makes the pruning effective.
