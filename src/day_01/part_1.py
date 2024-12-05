with open("./input.txt", "r") as file:
    values = [line.strip().split("   ") for line in file]
    column_1, column_2 = zip(*values)
    column_1 = list(column_1)
    column_2 = list(column_2)
    column_1.sort()
    column_2.sort()
    distances = [abs(int(a) - int(b)) for a, b in zip(column_1, column_2)]
    total = sum(distances)
    print(total)
