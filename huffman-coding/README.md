# Huffman Coding

**DAA Lab — Experiment 15: Huffman Coding for text compression.**

`main.py` builds an optimal prefix-free binary code for the characters of a string
using Huffman's greedy algorithm, then reports the codes and the compression
achieved.

## Algorithm

1. Count each character's frequency.
2. Put every character in a min-heap keyed by frequency.
3. Repeatedly remove the two least-frequent nodes and merge them under a new
   parent whose frequency is their sum; push it back. After `n − 1` merges one
   tree remains.
4. Assign `0` to left edges and `1` to right edges; each leaf's root-to-leaf path
   is its code. Frequent characters end up nearest the root, so they get the
   shortest codes.

Because no code is a prefix of another, the encoded stream decodes unambiguously.

## Run

```bash
python3 main.py
```

Enter the text; the program prints the frequencies, codes, encoded bit-string, and
the size saved against a fixed 8-bit-per-character encoding.

## Complexity

`O(n log n)` for `n` distinct symbols, dominated by the heap operations. Huffman
coding is provably optimal among per-symbol prefix codes.
