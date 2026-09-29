count = 0


def Place(x, k):
    # Can a queen be placed in row k, column x[k]? Check earlier queens.
    for i in range(1, k):
        if x[i] == x[k] or abs(x[i] - x[k]) == abs(i - k):
            return False
    return True


def board(x, n):
    lines = []
    for i in range(1, n + 1):
        row = ["Q" if x[i] == j else "." for j in range(1, n + 1)]
        lines.append(" ".join(row))
    return "\n".join(lines)


def NQueens(x, k, n):
    # Backtracking: place a queen in each row k, trying every column.
    global count
    for col in range(1, n + 1):
        x[k] = col
        if Place(x, k):
            if k == n:
                count += 1
                print(f"\nSolution {count}: columns = {x[1:]}")
                print(board(x, n))
            else:
                NQueens(x, k + 1, n)


if __name__ == "__main__":
    print("Enter board size n:")
    n = int(input().strip())
    x = [0] * (n + 1)
    NQueens(x, 1, n)
    print(f"\nTotal solutions for {n}-Queens: {count}")
