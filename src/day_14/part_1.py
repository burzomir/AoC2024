from dataclasses import dataclass, field
from parsy import string, regex, seq

integer = regex(r'-?\d+').map(int)

vector_parser = seq(
    integer,
    string(","),
    integer
).map(lambda res: Vector(res[0], res[2]))

guard_parser = seq(
    string("p="),
    vector_parser,
    string(" v="),
    vector_parser,
    string("\n").optional()
).map(lambda res: Guard(position=res[1], velocity=res[3]))


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __mul__(self, n):
        return Vector(self.x * n, self.y * n)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mod__(self, other):
        return Vector(self.x % other.x, self.y % other.y)

    def __truediv__(self, n):
        return Vector(self.x // n, self.y // n)

    def __lt__(self, other):
        return (self.x < other.x) and (self.y < other.y)

    def __le__(self, other):
        return (self.x <= other.x) and (self.y <= other.y)

    def __gt__(self, other):
        return (self.x > other.x) and (self.y > other.y)


@dataclass(frozen=True)
class Guard:
    position: Vector
    velocity: Vector

    def move(self, seconds: int, boundary: Vector):
        new_position = (self.position + (self.velocity * seconds)) % boundary
        return Guard(new_position, self.velocity)


class Quadrants:
    def __init__(self, boundary: Vector):
        self.mid_point = boundary / 2
        print(self.mid_point)
        self.boundary = boundary
        self.q1: list[Guard] = []
        self.q2: list[Guard] = []
        self.q3: list[Guard] = []
        self.q4: list[Guard] = []

    def get_safety_factor(self):
        return len(quadrants.q1) * len(quadrants.q2) * len(quadrants.q3) * len(quadrants.q4)

    def append(self, guard: Guard):
        if guard.position < self.mid_point:
            self.q1.append(guard)
            return

        if Vector(self.mid_point.x + 1, 0) <= guard.position < Vector(self.boundary.x, self.mid_point.y):
            self.q2.append(guard)
            return

        if Vector(0, self.mid_point.y + 1) <= guard.position < Vector(self.mid_point.x, self.boundary.y):
            self.q3.append(guard)
            return

        if self.mid_point < guard.position < self.boundary:
            print("q4", guard.position)
            self.q4.append(guard)
            return


with open("./input.txt", "r") as file:
    boundary = Vector(101, 103)
# with open("./input_simple.txt", "r") as file:
    # boundary = Vector(11, 7)
    guards = guard_parser.many().parse(file.read())
    quadrants = Quadrants(boundary)
    for guard in guards:
        quadrants.append(guard.move(100, boundary))
    print(quadrants.get_safety_factor())
