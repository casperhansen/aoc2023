from shapely.geometry import Point as shapePoint
from shapely.geometry.polygon import Polygon


def loadfile(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        return lines


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y


class World:
    def __init__(self, world: list[list[str]]) -> None:
        self.world = world
        self.visited_world = [["." for _ in row] for row in world]

    def get(self, p: Point) -> str:
        return self.world[p.y][p.x]

    def visit(self, p: Point) -> None:
        self.visited_world[p.y][p.x] = "#"

    def count_visits(self) -> int:
        return sum([sum([1 if c == "#" else 0 for c in row]) for row in self.visited_world])

    def __repr__(self) -> str:
        return "\n".join(["".join(row) for row in self.world])

    def print_visited(self) -> None:
        print("\n".join(["".join(row) for row in self.visited_world]))

    def find(self, symbol: str) -> Point:
        for y, row in enumerate(self.world):
            for x, c in enumerate(row):
                if c == symbol:
                    return Point(x, y)
        raise ValueError(f"Could not find {symbol} in world")


UP = Point(0, -1)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)
TERMINAL = "S"


def get_possible_moves(world, p):
    symbol = world.get(p)
    match symbol:
        case "|":
            return [p + UP, p + DOWN]
        case "-":
            return [p + LEFT, p + RIGHT]
        case "L":
            return [p + RIGHT, p + UP]
        case "J":
            return [p + LEFT, p + UP]
        case "F":
            return [p + RIGHT, p + DOWN]
        case "7":
            return [p + LEFT, p + DOWN]
    return []


def make_world(fname):
    lines = loadfile(fname)
    world = []
    for line in lines:
        world.append([c for c in line])

    return World(world)


def main():
    world = make_world("data/10.txt")
    start_point = world.find(TERMINAL)
    print(world)
    print(start_point)

    # find points around S that can lead to S
    check_start_neighbours = [start_point + UP, start_point + DOWN, start_point + LEFT, start_point + RIGHT]
    start_points = []
    for p in check_start_neighbours:
        possible_moves = get_possible_moves(world, p)
        symbols = [world.get(p) for p in possible_moves]
        if TERMINAL in symbols:
            start_points.append(p)

    # in the inputs there's only 2 connecting points to the start point, so we can just pick the first

    visited_points = [start_point, start_points[0]]
    world.visit(start_point)
    world.visit(start_points[0])
    print((visited_points[0], world.get(visited_points[0])), "to", (visited_points[1], world.get(visited_points[1])))
    print("-")
    while True:
        last_point = visited_points[-1]
        possible_moves = get_possible_moves(world, last_point)
        for p in possible_moves:
            if p not in visited_points:
                visited_points.append(p)
                world.visit(p)
                print((last_point, world.get(last_point)), "to", (p, world.get(p)))
                break
        else:
            break

    assert any([world.get(p) == TERMINAL for p in possible_moves]), "last possible move does not contain S, oh no..."

    world.print_visited()
    print(world.count_visits() // 2)

    print("#" * 30)
    count = 0
    polygon = Polygon([(p.x, p.y) for p in visited_points])
    for y in range(len(world.world)):
        for x in range(len(world.world[0])):
            shapelyPoint = shapePoint(x, y)
            if polygon.contains(shapelyPoint) and Point(x, y) not in visited_points:
                count += 1
    print(count)


if __name__ == "__main__":
    main()
