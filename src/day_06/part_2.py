from dataclasses import dataclass, field
from enum import Enum, auto
import copy
import os
from multiprocessing import Pool, cpu_count
from tqdm import tqdm


class Direction(Enum):
    North = auto()
    East = auto()
    South = auto()
    West = auto()

    def rotate(self):
        match(self):
            case Direction.North:
                return Direction.East
            case Direction.East:
                return Direction.South
            case Direction.South:
                return Direction.West
            case Direction.West:
                return Direction.North


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Step:
    point: Point
    direction: Direction


@dataclass
class Guard:
    steps: list[Step]
    steps_lookup: set[Step]
    _in_a_loop: bool = False

    def __init__(self, x, y):
        first_step = Step(Point(x, y), Direction.North)
        self.steps = [first_step]
        self.steps_lookup = set([first_step])

    def get_last_step(self):
        return self.steps[-1]

    def is_in_a_loop(self):
        return self._in_a_loop

    def move(self, obstacles: set[Point]):
        last_step = self.get_last_step()
        next_point = move_point(last_step.point, last_step.direction)
        next_step = Step(next_point, last_step.direction)
        if next_point in obstacles:
            next_step = Step(last_step.point, last_step.direction.rotate())
        self._in_a_loop = next_step in self.steps_lookup
        self.steps.append(next_step)
        self.steps_lookup.add(next_step)


def move_point(p: Point, d: Direction):
    match(d):
        case Direction.North:
            return Point(p.x, p.y - 1)
        case Direction.East:
            return Point(p.x + 1, p.y)
        case Direction.South:
            return Point(p.x, p.y + 1)
        case Direction.West:
            return Point(p.x - 1, p.y)


@dataclass
class Board:
    guard: Guard
    obstacles: set[Point] = field(default_factory=set)
    boundary: Point = field(default=Point(0, 0))

    def run(self):
        while True:
            if self.is_in_a_loop():
                return

            if self.is_out_of_bounds():
                return

            self.guard.move(self.obstacles)

    def is_in_a_loop(self):
        return self.guard.is_in_a_loop()

    def is_out_of_bounds(self):
        last_step = self.guard.get_last_step()
        return any([
            last_step.point.x > self.boundary.x - 1,
            last_step.point.y > self.boundary.y - 1,
            last_step.point.x < 1,
            last_step.point.y < 1
        ])


def parse_board(input: str):
    board_data = [list(line) for line in input.split("\n")]
    obstacles = set()
    guard = Guard(0, 0)
    for y, row_data in enumerate(board_data):
        for x, char in enumerate(row_data):
            match(char):
                case "#":
                    obstacles.add(Point(x, y))
                case "^":
                    guard = Guard(x, y)
    return Board(guard, obstacles, boundary=Point(len(board_data[0]), len(board_data)))


def init_board():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "input_simple.txt")
    with open(file_path, "r") as file:
        board = parse_board(file.read())
        return board


board = init_board()
board.run()


def solve_at_index(index):
    _board = copy.deepcopy(board)
    obstacle = _board.guard.steps[-index]
    _board.guard.steps = _board.guard.steps[:-index]
    _board.obstacles.add(obstacle.point)
    _board.guard.steps_lookup = set(_board.guard.steps)
    _board.run()
    if _board.is_in_a_loop():
        return obstacle
    else:
        return None


if __name__ == '__main__':
    indices = range(1, len(board.guard.steps))
    obstacles: set[Point] = set()
    with Pool(cpu_count()) as p:
        with tqdm(total=len(indices), desc="Processing", unit="task") as pbar:
            for obstacle in p.imap_unordered(solve_at_index, indices):
                pbar.update(1)
                if obstacles != None:
                    obstacles.add(obstacle)
    print(f"Res: {len(obstacles) - 1}")
