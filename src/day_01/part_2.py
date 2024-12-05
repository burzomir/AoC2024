from collections import Counter

with open("./input.txt", "r") as file:
    values = [line.strip().split("   ") for line in file]
    column_1, column_2 = zip(*values)
    count = Counter(column_2)
    similarities = [int(v) * count[v] for v in column_1]
    total = sum(similarities)
    print(total)
