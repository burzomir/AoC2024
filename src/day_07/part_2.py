from itertools import product
from tqdm import tqdm
from multiprocessing import Pool, cpu_count


def eval_operator(operator, x, y):
    match(operator):
        case "*":
            return x * y
        case "+":
            return x + y
        case "||":
            return int(f"{x}{y}")


def solve(x):
    test_value, terms, combinations = x
    for combination in combinations:
        value = terms[0]
        for index, operator in enumerate(combination):
            value = eval_operator(operator, value, terms[index + 1])
        if value == test_value:
            return test_value
    return None


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        xs = []
        for line in file:
            test_value_str, equation_str = line.split(": ")
            test_value = int(test_value_str)
            terms = [int(term) for term in equation_str.split(" ")]
            combinations = list(
                product(["*", "+", "||"], repeat=len(terms) - 1))
            xs.append((test_value, terms, combinations))

        res = set()
        with tqdm(total=len(xs), desc="Processing", unit="Line") as progress_bar:
            with Pool(cpu_count()) as pool:
                for solution in pool.imap_unordered(solve, xs):
                    if solution:
                        res.add(solution)
                    progress_bar.update(1)

        print(sum(res))
