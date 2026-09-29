# Design and Analysis of Algorithms Lab

Python implementations of classic algorithm-design techniques — divide and
conquer, greedy, and dynamic programming — done as college lab practicals for
**CMP-307 Design and Analysis of Algorithms Lab**, B.E. Computer Engineering
(Goa University, NEP 2024-25 curriculum).

Several programs are written in the 1-indexed Horowitz–Sahni style and print
step-by-step traces so the algorithm's working can be followed by hand.

## Contents

| Exp | Folder | Technique | Algorithm |
|---|---|---|---|
| 1 | [min-max](min-max) | Divide & Conquer | Find max and min |
| 2a | [mergesort](mergesort) | Divide & Conquer | Merge Sort |
| 2b | [quicksort](quicksort) | Divide & Conquer | Quick Sort |
| 3 | [strassen](strassen) | Divide & Conquer | Strassen's Matrix Multiplication |
| 4 | [knapsack](knapsack) | Greedy | Fractional Knapsack |
| 5 | [prim](prim) | Greedy | Prim's Minimum Spanning Tree |
| 6 | [kruskal](kruskal) | Greedy | Kruskal's Minimum Spanning Tree |
| 7 | [shortestDistance](shortestDistance) | Greedy | Dijkstra's Single Source Shortest Path |
| 8 | [multistage-graph](multistage-graph) | Dynamic Programming | Multistage Graph shortest path |
| 9 | [all-pairs-shortest-path](all-pairs-shortest-path) | Dynamic Programming | Floyd–Warshall all pairs shortest path |
| 10 | [n-queens](n-queens) | Backtracking | N-Queens problem |
| 11 | [sum-of-subsets](sum-of-subsets) | Backtracking | Sum of Subsets |
| 12 | [graph-coloring](graph-coloring) | Backtracking | Graph m-Colouring |
| 13 | [knapsack-branch-bound](knapsack-branch-bound) | Branch & Bound | 0/1 Knapsack (LC strategy) |
| 14 | [string-matching](string-matching) | String matching | KMP and Boyer–Moore |
| 15 | [huffman-coding](huffman-coding) | Greedy | Huffman Coding (text compression) |
| — | [assignment](assignment) | All techniques | Streamlit app visualizing every algorithm in this repo |

Each folder has its own README with the algorithm, run instructions, and
complexity. Console programs run with `python3 main.py` (Python 3, standard
library only); the visualizer needs the packages in its `requirements.txt`.

## Syllabus reference

Covers all 15 CMP-307 experiments across the four course outcomes: divide and
conquer (Exp 1–3, CO1), greedy and shortest path (Exp 4–7, CO2), dynamic
programming (Exp 8–9), backtracking and branch and bound (Exp 10–13, CO3), and
string matching and compression (Exp 14–15, CO4).
