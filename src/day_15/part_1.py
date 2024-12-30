from dataclasses import dataclass
from enum import Enum, auto


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


class Direction(Enum):
    Up = auto()
    Right = auto()
    Down = auto()
    Left = auto()


@dataclass
class Robot:
    point: Point
    moves: list[Direction]


def parse_input(input: str):
    walls: set[Point] = set()
    boxes: set[Point] = set()
    robot: Robot = Robot(Point(0, 0), [])
    warehouse_map, moves_map = input.split("\n\n")
    # parse map
    for (y, line) in enumerate(warehouse_map.splitlines()):
        if line == "":
            break
        for (x, c) in enumerate(line):
            point = Point(x, y)
            match c:
                case "#":
                    walls.add(point)
                case "@":
                    robot.point = point
                case "O":
                    boxes.add(point)
    # parse robot moves
    for line in moves_map.splitlines():
        for c in line:
            match c:
                case "^":
                    robot.moves.append(Direction.Up)
                case ">":
                    robot.moves.append(Direction.Right)
                case "v":
                    robot.moves.append(Direction.Down)
                case "<":
                    robot.moves.append(Direction.Left)

    return walls, boxes, robot


def direction_to_vector(direction: Direction) -> Point:
    match direction:
        case Direction.Up:
            return Point(0, -1)
        case Direction.Right:
            return Point(1, 0)
        case Direction.Down:
            return Point(0, 1)
        case Direction.Left:
            return Point(-1, 0)


def line(starting_point: Point, direction: Direction):
    current_point = starting_point
    direction_vector = direction_to_vector(direction)
    while True:
        current_point += direction_vector
        yield current_point


def find_free_space(starting_point: Point, direction: Direction, walls: set[Point], boxes: set[Point]):
    for p in line(starting_point, direction):
        if p in boxes:
            continue

        if p in walls:
            return None

        return p


def get_line_of_boxes(starting_point: Point, direction: Direction, boxes: set[Point]):
    line_of_boxes = []
    for p in line(starting_point, direction):
        if p in boxes:
            line_of_boxes.append(p)
        else:
            return line_of_boxes


def move(robot: Robot, walls: set[Point], boxes: set[Point]):
    direction = robot.moves.pop(0)
    direction_vector = direction_to_vector(direction)
    free_space = find_free_space(robot.point, direction, walls, boxes)
    if free_space == None:
        return
    line_of_boxes = get_line_of_boxes(robot.point, direction, boxes)
    for box in line_of_boxes:
        boxes.remove(box)
    for box in line_of_boxes:
        boxes.add(box + direction_vector)
    robot.point += direction_vector


def render(robot, walls, boxes):
    lines = []
    for y in range(8):
        line = ""
        for x in range(8):
            p = Point(x, y)
            if p in walls:
                line += "#"
            elif p in boxes:
                line += "O"
            elif robot.point == p:
                line += "@"
            else:
                line += "."
        lines.append(line)
    return "\n".join(lines)


with open("./input.txt", "r") as file:
    walls, boxes, robot = parse_input(file.read())
    while len(robot.moves) > 0:
        move(robot, walls, boxes)
    total = 0
    for box in boxes:
        coord = 100 * box.y + box.x
        total += coord
    print(total)
