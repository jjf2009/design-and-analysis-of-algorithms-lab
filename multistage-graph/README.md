# Multistage Graph (Dynamic Programming)

**DAA Lab — Experiment 8: Multistage graph using Dynamic Programming.**

`main.py` finds the minimum-cost path from the source to the sink of a multistage
graph — a directed graph whose vertices are partitioned into ordered stages, with
edges only from one stage to the next — using the **backward-cost** DP formulation
(Horowitz–Sahni).

## Algorithm

`bcost[j]` is the cheapest cost from vertex `j` to the sink `n`:

```
bcost[n] = 0
bcost[j] = min over edges (j, r) of  cost[j][r] + bcost[r]
```

Computed for `j = n-1 … 1`, storing the chosen successor `d[j]` so the optimal
path can be traced from the source forward.

## Run

```bash
python3 main.py
```

Uses the classic 5-stage, 12-vertex example; edit the `edges` dict to try
another graph.

## Complexity

`O(V + E)` — each edge is relaxed exactly once.
