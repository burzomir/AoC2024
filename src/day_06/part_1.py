from dataclasses import dataclass, field
from enum import Enum, auto


@dataclass
class FloorTile:
    pass


@dataclass
class ObstacleTile:
    pass


@dataclass
class GuardTile:
    pass


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


@dataclass
class Guard:
    x: int
    y: int
    d: Direction

    def next_step(self):
        match(self.d):
            case Direction.North:
                return Point(self.x, self.y - 1)
            case Direction.East:
                return Point(self.x + 1, self.y)
            case Direction.South:
                return Point(self.x, self.y + 1)
            case Direction.West:
                return Point(self.x - 1, self.y)

    def move(self, point: Point):
        self.x = point.x
        self.y = point.y

    def turn_right(self):
        self.d = self.d.rotate()


@dataclass
class Board:
    guard: Guard
    tiles: list[list[FloorTile | ObstacleTile]]
    visited_tiles: set[Point] = field(default_factory=set)

    def __post_init__(self):
        self.visited_tiles.add(Point(self.guard.x, self.guard.y))

    def run(self):
        next_step = self.guard.next_step()
        if (next_step.x > len(self.tiles[0]) - 1 or next_step.y > len(self.tiles) - 1):
            return True
        tile = self.tiles[next_step.y][next_step.x]
        match(tile):
            case FloorTile():
                self.guard.move(next_step)
                self.visited_tiles.add(next_step)
            case ObstacleTile():
                self.guard.turn_right()
        return False


def parse_tile(tile: str):
    match(tile):
        case ".":
            return FloorTile()
        case "#":
            return ObstacleTile()
        case "^":
            return GuardTile()


def parse_board(input: str):
    board_data = [list(line) for line in input.split("\n")]
    board = []
    guard = Guard(0, 0, Direction.North)
    for y, row_data in enumerate(board_data):
        row = []
        for x, char in enumerate(row_data):
            tile = parse_tile(char)
            if isinstance(tile, GuardTile):
                guard = Guard(x, y, Direction.North)
                row.append(FloorTile())
            else:
                row.append(tile)
        board.append(row)
    return Board(guard, board)


with open("./input.txt", "r") as file:
    board = parse_board(file.read())
    while True:
        if (board.run()):
            break
    print(len(board.visited_tiles))
