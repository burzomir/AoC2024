from parsy import string, regex, seq
from dataclasses import dataclass
import sys

integer = regex(r'\d+').map(int)


def coord_parser(coord_id, sign="+"):
    return string(f"{coord_id}{sign}") >> integer


x_parser = coord_parser("X")
y_parser = coord_parser("Y")


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)


@dataclass(frozen=True)
class Button:
    point: Point
    tokens: int

    def __iter__(self):
        yield from self.point
        yield self.tokens

    def __add__(self, button):
        return Button(self.point + button.point, self.tokens + button.tokens)


def button_parser(button_id, token_value):
    return seq(
        string(f"Button {button_id}: "),
        x_parser, string(", "),
        y_parser
    ).map(lambda result: Button(Point(result[1], result[3]), token_value))


button_a_parser = button_parser("A", 3)
button_b_parser = button_parser("B", 1)

prize_parser = seq(
    string("Prize: "),
    coord_parser("X", sign="="),
    string(", "),
    coord_parser("Y", sign="=")
).map(lambda result: Point(result[1], result[3]))

machine_parser = seq(
    button_a_parser,
    string("\n"),
    button_b_parser,
    string("\n"),
    prize_parser,
    string("\n").optional(),
    string("\n").optional()
).map(lambda res: (res[0], res[2], res[4]))


def check(a_presses, b_presses, machine):
    button_a, button_b, prize = machine
    x_a = a_presses * button_a[0]
    y_a = a_presses * button_a[1]
    x_b = b_presses * button_b[0]
    y_b = b_presses * button_b[1]
    return all([
        x_a + x_b == prize[0],
        y_a + y_b == prize[0]
    ])


def solve(machine):
    button_a, button_b, prize = machine
    tokens = dict()
    queue = [button_a, button_b]
    while len(queue) > 0:
        button = queue.pop(0)
        next_a = button + button_a
        if next_a.point.x <= prize.x and next_a.point.y <= prize.y:
            tokens_a = tokens.get(next_a.point, sys.maxsize)
            if tokens_a > next_a.tokens:
                tokens[next_a.point] = next_a.tokens
                queue.append(next_a)

        next_b = button + button_b
        if next_b.point.x <= prize.x and next_b.point.y <= prize.y:
            tokens_b = tokens.get(next_a.point, sys.maxsize)
            if tokens_b > next_b.tokens:
                tokens[next_b.point] = next_b.tokens
                queue.append(next_b)

    try:
        return tokens[prize]
    except:
        return 0


with open("./input.txt", "r") as file:
    machines = machine_parser.many().parse(file.read())
    total = 0
    for machine in machines:
        total += solve(machine)
    print(total)
