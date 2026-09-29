# String Matching — KMP and Boyer–Moore

**DAA Lab — Experiment 14: String matching algorithms — (a) KMP (b) Boyer–Moore.**

`main.py` implements both classical exact string-matching algorithms and reports
every position where the pattern occurs in the text.

## Algorithms

**Knuth–Morris–Pratt (KMP).** Precomputes the **LPS** table (longest proper
prefix that is also a suffix) for the pattern. On a mismatch it shifts the pattern
using the table instead of re-comparing text characters, so the text pointer never
moves backward — `O(n + m)`.

**Boyer–Moore (bad-character heuristic).** Aligns the pattern and compares from the
**right**. On a mismatch it jumps the pattern past the offending text character
using a last-occurrence table, often skipping large sections of the text —
sub-linear on typical input, `O(nm)` worst case.

## Run

```bash
python3 main.py
```

Enter the text and the pattern; both algorithms print the match indexes and agree.

## Complexity

| Algorithm | Preprocessing | Search |
|---|---|---|
| KMP | `O(m)` | `O(n)` |
| Boyer–Moore | `O(m + σ)` | `O(nm)` worst, sub-linear typical |
