from itertools import combinations


def anti_node_generator(map_width, map_height, p1, p2):
    while True:
        n = make_anti_node(p1, p2)
        if is_on_map(map_width, map_height, n):
            yield n
            p1, p2 = p2, n
        else:
            return


def find_anti_nodes(map_width: int, map_height: int, antennas: list[tuple[int, int]]):
    pairs = combinations(antennas, 2)
    anti_nodes = set()
    for p1, p2 in pairs:
        anti_nodes.add(p1)
        anti_nodes.add(p2)
        for anti_node in anti_node_generator(map_width, map_height, p1, p2):
            anti_nodes.add(anti_node)
        for anti_node in anti_node_generator(map_width, map_height, p2, p1):
            anti_nodes.add(anti_node)
    return anti_nodes


def is_on_map(map_width, map_heigth, point):
    x, y = point
    return x >= 0 and y >= 0 and x < map_width and y < map_heigth


def get_distance(p1: tuple[int, int], p2: tuple[int, int]):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)


def get_direction(p1: tuple[int, int], p2: tuple[int, int]):
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    return (dx, dy)


def make_anti_node(p1: tuple[int, int], p2: tuple[int, int]):
    x2, y2 = p2
    distance = get_distance(p1, p2)
    dx, dy = get_direction(p1, p2)
    if abs(dx) >= distance:
        x3 = x2 + (distance if dx > 0 else -distance)
        y3 = y2
    else:
        x3 = x2 + dx
        remaining_distance = distance - abs(dx)
        y3 = y2 + (remaining_distance if dy > 0 else -remaining_distance)
    return (x3, y3)


with open("./input.txt", "r") as file:
    lines = file.read().split("\n")
    height = len(lines)
    width = len(lines[0])
    frequencies: dict = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            antennas = frequencies.get(c, [])
            antennas.append((x, y))
            frequencies[c] = antennas
    frequencies.pop(".")
    res = set()
    for frequency in frequencies.values():
        for anti_node in find_anti_nodes(width, height, frequency):
            res.add(anti_node)
    print(len(set(res)))
