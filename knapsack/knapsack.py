def knapsack(w, p, m, order):
    n = len(w)
    x = [0] * n
    weight = 0
    profit = 0

    for i in order:
        if weight + w[i] <= m:
            x[i] = 1
            weight += w[i]
            profit += p[i]
        else:
            x[i] = (m - weight) / w[i]
            weight = m
            profit += p[i] * x[i]
            break

    return x, weight, profit


n = int(input("Enter number of objects: "))

w = list(map(float, input("Enter weights: ").split()))
p = list(map(float, input("Enter profits: ").split()))

m = float(input("Enter knapsack capacity: "))


orders = [
    ("Maximum Profit First", sorted(range(n), key=lambda i: p[i], reverse=True)),
    ("Minimum Weight First", sorted(range(n), key=lambda i: w[i])),
    ("Maximum Profit/Weight Ratio First",
     sorted(range(n), key=lambda i: p[i] / w[i], reverse=True))
]


for name, order in orders:
    x, weight, profit = knapsack(w, p, m, order)

    print("\n", name)
    print("Order:", [i + 1 for i in order])
    print("x =", x)
    print("Total Weight =", weight)
    print("Total Profit =", profit)


print("\nFractions: 1/2, 1/3, 1/4, 1/5 ...")

x = []
weight = 0
profit = 0

for i in range(n):
    fraction = 1 / (i + 2)
    x.append(fraction)
    weight += w[i] * fraction
    profit += p[i] * fraction

print("x =", x)
print("Total Weight =", weight)
print("Total Profit =", profit)