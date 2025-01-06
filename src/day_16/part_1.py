from enum import Enum, auto
import networkx as nx


class Dir(Enum):
    N = auto()
    E = auto()
    S = auto()
    W = auto()

    def __repr__(self):
        return self.name


def get_next_nodes(from_node: tuple[int, int, Dir]) -> list[tuple[int, int, Dir]]:
    x, y, direction = from_node
    n = (x, y - 1)
    e = (x + 1, y)
    s = (x, y + 1)
    w = (x - 1, y)
    if direction == Dir.N:
        return [(*n, Dir.N), (*e, Dir.E), (*w, Dir.W)]
    if direction == Dir.E:
        return [(*e, Dir.E), (*s, Dir.S), (*n, Dir.N)]
    if direction == Dir.S:
        return [(*s, Dir.S), (*w, Dir.W), (*e, Dir.E)]
    if direction == Dir.W:
        return [(*w, Dir.W), (*n, Dir.N), (*s, Dir.S)]


filename = "./input.txt"
# filename = "./input_simple.txt"
# filename = "./input_first_example.txt"
# filename = "./input_second_example.txt"

with open(filename, "r") as file:
    nodes: set[tuple[int, int]] = set()
    for y, line in enumerate(file.read().splitlines()):
        for x, c in enumerate(line):
            p = (x, y)
            match c:
                case "S":
                    start_node = p
                case "E":
                    end_node = p
                    nodes.add(end_node)
                case ".":
                    nodes.add(p)

    g = nx.DiGraph()
    queue = [(*start_node, Dir.E)]
    visited = set()
    while queue:
        cx, cy, cd = queue.pop(0)
        if (cx, cy, cd) in visited:
            continue
        visited.add((cx, cy, cd))
        for x, y, d in get_next_nodes((cx, cy, cd)):
            if not (x, y) in nodes:
                continue
            if (x, y) == end_node:
                if cd == d:
                    g.add_node("end")
                    g.add_edge((cx, cy, cd), "end", weight=1)
                else:
                    g.add_edge((cx, cy, cd), (cx, cy, d), weight=1000)
                    g.add_edge((cx, cy, d), "end", weight=1)
                continue
            if cd == d:
                g.add_edge((cx, cy, cd), (x, y, d), weight=1)
            else:
                g.add_edge((cx, cy, cd), (cx, cy, d), weight=1000)
                g.add_edge((cx, cy, d), (x, y, d), weight=1)
            queue.append((x, y, d))

    for edge in g.edges:
        print(edge, g.edges[edge])

    total = nx.shortest_path_length(
        g, (*start_node, Dir.E), "end", "weight")
    print(total)
