from itertools import product


with open("./input.txt", "r") as file:
    res = set()
    for line in file:
        test_value_str, equation_str = line.split(": ")
        test_value = int(test_value_str)
        terms = [int(term) for term in equation_str.split(" ")]
        combinations = list(product(['*', '+'], repeat=len(terms) - 1))
        for combination in combinations:
            value = terms[0]
            for index, operator in enumerate(combination):
                value = eval(f"{value}{operator}{terms[index + 1]}")
            if value == test_value:
                res.add(test_value)
                break
    print(sum(res))
