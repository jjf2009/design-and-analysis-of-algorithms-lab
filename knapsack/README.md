# Fractional Knapsack (Greedy)

**DAA Lab — Experiment 4: Fractional Knapsack problem using the greedy method.**

`knapsack.py` solves the fractional knapsack problem: given `n` objects with
weights and profits and a knapsack of capacity `m`, choose fractions
`0 ≤ xᵢ ≤ 1` of each object to maximise total profit without exceeding capacity.
Unlike 0/1 knapsack, an object may be taken partially.

## Algorithm

The `knapsack(w, p, m, order)` function fills the sack by considering objects in
a given `order`, taking each one whole while it fits and taking a **fraction** of
the object that first overflows the capacity, then stopping.

The script compares three greedy selection strategies to show which is optimal:

| Strategy | Order objects by |
|---|---|
| Maximum Profit First | profit, descending |
| Minimum Weight First | weight, ascending |
| Maximum Profit/Weight Ratio First | `p/w` ratio, descending |

Only the **profit/weight ratio** strategy is guaranteed to give the optimal
fractional solution. The script also prints a fixed-fraction (`1/2, 1/3, …`)
selection for contrast.

## Run

```bash
python3 knapsack.py
```

Enter the object count, then space-separated weights, profits, and the capacity.

## Complexity

`O(n log n)`, dominated by sorting the objects; the fill itself is `O(n)`.
