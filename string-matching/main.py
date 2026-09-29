# DAA Lab - Experiment 14: String matching - (a) KMP  (b) Boyer-Moore


def compute_lps(pattern):
    # Longest proper Prefix that is also a Suffix, for each pattern position.
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def kmp_search(text, pattern):
    # Knuth-Morris-Pratt: never re-compares text characters, using the LPS table
    # to skip ahead on a mismatch. O(n + m).
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    matches = []
    i = j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                matches.append(i - j)
                j = lps[j - 1]
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
    return matches


def last_occurrence(pattern):
    table = {}
    for i, ch in enumerate(pattern):
        table[ch] = i
    return table


def boyer_moore_search(text, pattern):
    # Boyer-Moore with the bad-character heuristic: match from the right and, on
    # a mismatch, jump the pattern past the offending text character.
    n, m = len(text), len(pattern)
    if m == 0:
        return []
    last = last_occurrence(pattern)
    matches = []
    s = 0  # alignment of the pattern against the text
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            matches.append(s)
            s += 1
        else:
            bad = last.get(text[s + j], -1)
            s += max(1, j - bad)
    return matches


if __name__ == "__main__":
    text = input("Enter text: ").strip()
    pattern = input("Enter pattern: ").strip()

    kmp = kmp_search(text, pattern)
    bm = boyer_moore_search(text, pattern)

    print("\nKMP matches at indexes:        ", kmp if kmp else "none")
    print("Boyer-Moore matches at indexes:", bm if bm else "none")
