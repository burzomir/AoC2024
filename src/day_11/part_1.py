from itertools import chain


def split(xs):
    mid = len(xs) // 2
    return [xs[:mid], xs[mid:]]


def apply_rule(stone: str):
    match stone:
        case "0":
            return ["1"]

        case s if len(s) % 2 == 0:
            return list(map(lambda x: str(int(x)), split(s)))

        case _:
            return [str(int(stone) * 2024)]


with open("./input.txt", "r") as file:
    stones = [stone for stone in file.read().split(" ")]
    for blink in range(25):
        stones = list(chain(*map(apply_rule, stones)))
    print(len(stones))
