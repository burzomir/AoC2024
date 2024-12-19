
TopoMap = list[list[int]]
Point = tuple[int, int]
Dimensions = tuple[int, int]


def read_topo_map(input: str) -> TopoMap:
    return [[int(c) for c in line] for line in input.split("\n")]


def get_dimensions(topo_map: TopoMap) -> Dimensions:
    width = len(topo_map[0])
    height = len(topo_map)
    return (width, height)


def get_trailheads(topo_map: TopoMap) -> list[Point]:
    trailheads: list[Point] = []
    for y, row in enumerate(topo_map):
        for x, p in enumerate(row):
            if p == 0:
                trailheads.append((x, y))
    return trailheads


def get_peaks(topo_map: TopoMap) -> list[Point]:
    peaks: list[Point] = []
    for y, row in enumerate(topo_map):
        for x, p in enumerate(row):
            if p == 9:
                peaks.append((x, y))
    return peaks


def get_points_around(point: Point) -> list[Point]:
    x, y = point
    n = (x, y - 1)
    e = (x + 1, y)
    s = (x, y + 1)
    w = (x - 1, y)
    return [n, e, s, w]


def is_in_bounds(dimensions: Dimensions, point: Point):
    w, h = dimensions
    x, y = point
    return 0 <= x < w and 0 <= y < h


def get_height_at(topo_map: TopoMap, point: Point):
    x, y = point
    return topo_map[y][x]


def is_reachable(topo_map: TopoMap, from_: Point, to: Point):
    h1 = get_height_at(topo_map, from_)
    h2 = get_height_at(topo_map, to)
    return h2 - h1 == 1


def get_next_points(topo_map: TopoMap, point: Point):
    dimensions = get_dimensions(topo_map)

    def is_next_point(p):
        return is_in_bounds(dimensions, p) and is_reachable(topo_map, point, p)

    return [p for p in get_points_around(point) if is_next_point(p)]


def get_trails(topo_map: TopoMap, trailhead: Point):
    if not get_next_points(topo_map, trailhead):
        return [[trailhead]]
    else:
        paths = []
        for next_point in get_next_points(topo_map, trailhead):
            for path in get_trails(topo_map, next_point):
                paths.append([trailhead] + path)
        return paths


with open("./input.txt", "r") as file:
    input = file.read()
    topo_map = read_topo_map(input)
    trailheads = get_trailheads(topo_map)
    total = 0
    for trailhead in trailheads:
        peaks = set()
        trails = get_trails(topo_map, trailhead)
        for trail in trails:
            if len(trail) == 10:
                peaks.add(trail[-1])
        total += len(peaks)
    print(total)
