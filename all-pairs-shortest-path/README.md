# All Pairs Shortest Path (Floyd–Warshall)

**DAA Lab — Experiment 9: All pairs shortest path using Dynamic Programming.**

`main.py` computes the shortest distance between **every** pair of vertices of a
weighted directed graph with the Floyd–Warshall algorithm, printing the distance
matrix `A(k)` after each intermediate vertex is allowed.

## Algorithm

`A(k)[i][j]` is the shortest path from `i` to `j` whose intermediate vertices are
all drawn from `{1 … k}`:

```
A(0)[i][j] = cost[i][j]                       (direct edge, ∞ if none)
A(k)[i][j] = min( A(k-1)[i][j],
                  A(k-1)[i][k] + A(k-1)[k][j] )
```

Increasing `k` from `1` to `n` progressively admits more intermediate vertices
until every path has been considered.

## Run

```bash
python3 main.py
```

Uses a 3-vertex `cost` matrix (`∞` for absent edges); edit it to try others.

## Complexity

`O(n³)` time and `O(n²)` space. Works with negative edge weights, but not
negative cycles.
