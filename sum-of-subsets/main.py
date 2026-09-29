def SumOfSubsets(w, x, k, remaining, current, target, n):
    # Backtracking with two bounding conditions (Horowitz-Sahni). The weights w
    # are assumed sorted in non-decreasing order. 'current' is the sum chosen so
    # far, 'remaining' is the sum of the not-yet-considered weights.
    x[k] = 1  # include w[k]
    if current + w[k] == target:
        print("Subset:", [w[i] for i in range(1, k + 1) if x[i] == 1])
    elif k < n and current + w[k] + w[k + 1] <= target:
        SumOfSubsets(w, x, k + 1, remaining - w[k], current + w[k], target, n)

    # exclude w[k], only worth trying if the rest can still reach the target
    if k < n and current + remaining - w[k] >= target and current + w[k + 1] <= target:
        x[k] = 0
        SumOfSubsets(w, x, k + 1, remaining - w[k], current, target, n)


if __name__ == "__main__":
    print("Enter number of elements:")
    n = int(input().strip())
    print("Enter elements (will be sorted ascending):")
    w = [0] + sorted(map(int, input().strip().split()))
    print("Enter target sum:")
    target = int(input().strip())

    total = sum(w)
    x = [0] * (n + 1)
    print(f"\nSubsets of {w[1:]} summing to {target}:")
    if total < target:
        print("No subset possible (total is less than the target).")
    else:
        SumOfSubsets(w, x, 1, total, 0, target, n)
