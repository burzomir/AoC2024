from dataclasses import dataclass


@dataclass(frozen=True)
class Point():
    x: int
    y: int

    def get_points_around(self):
        x, y = self
        n = Point(x, y - 1)
        e = Point(x + 1, y)
        s = Point(x, y + 1)
        w = Point(x - 1, y)
        return [n, e, s, w]

    def __iter__(self):
        for attr in ['x', 'y']:
            yield getattr(self, attr)


class Grid:

    @classmethod
    def from_input(cls, input: str):
        grid = [[c for c in line] for line in input.split("\n")]
        return Grid(grid)

    def __init__(self, grid: list[list[str]]):
        self._grid = grid

    @property
    def width(self):
        return len(self._grid[0])

    @property
    def height(self):
        return len(self._grid)

    @property
    def dimensions(self):
        return (self.width, self.height)

    def at(self, point: Point):
        x, y = point
        return self._grid[y][x]

    def get_points_around(self, point: Point):
        points_around = point.get_points_around()
        return [point for point in points_around if self.is_in_bounds(point)]

    def is_in_bounds(self, point: Point):
        w, h = self.dimensions
        x, y = point
        return 0 <= x < w and 0 <= y < h

    def get_points(self):
        for y, row in enumerate(self._grid):
            for x, _ in enumerate(row):
                yield Point(x, y)
