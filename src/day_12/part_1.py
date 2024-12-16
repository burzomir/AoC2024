
from grid import Grid, Point


def get_region(grid: Grid, starting_point: Point):
    v = grid.at(starting_point)
    q = [starting_point]
    visited = {starting_point}
    while len(q) > 0:
        point = q.pop(0)
        points_around = grid.get_points_around(point)
        points_around = [p for p in points_around if not p in visited]
        points_around = [p for p in points_around if grid.at(p) == v]
        q.extend(points_around)
        visited.update(points_around)
    return visited


def find_regions(grid: Grid):
    visited = set()
    regions = []
    for point in grid.get_points():
        if point in visited:
            continue
        region = get_region(grid, point)
        regions.append(region)
        visited.update(region)
    return regions


def get_perimeter(region: set[Point]):
    total = 0
    for point in region:
        around = [p for p in point.get_points_around() if not p in region]
        total += len(around)
    return total


def get_price(region: set[Point]):
    area = len(region)
    perimeter = get_perimeter(region)
    return area * perimeter


with open("./input.txt", "r") as file:
    input = file.read()
    grid = Grid.from_input(input)
    prices = [get_price(region) for region in find_regions(grid)]
    total = sum(prices)
    print(total)
