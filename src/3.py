import numpy as np
from dataclasses import dataclass, field


def loadfile(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        return lines


def points_to_number(points):
    return int("".join([xy_lines[y, x] for x, y in points]))


@dataclass
class NumberPoints:
    points: list[tuple[int, int]] = field(default_factory=lambda: [])
    close_to_symbol: bool = False
    close_to_gear: bool = False

    def __hash__(self):
        hashed = hash((getattr(self, key) for key in self.__annotations__))
        return hashed


lines = loadfile("data/3.txt")
xy_lines = np.array([list(line) for line in lines])


number_to_points = []
for y, line in enumerate(lines):
    current_number_point = NumberPoints()

    for x, c in enumerate(line):
        if not c.isdigit():
            if len(current_number_point.points) > 0:
                number_to_points.append(current_number_point)
                current_number_point = NumberPoints()
        else:
            current_number_point.points.append((x, y))

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if x + i < 0 or y + j < 0 or x + i >= len(line) or y + j >= len(lines):
                        continue
                    if lines[y + j][x + i] != "*":
                        current_number_point.close_to_gear = True
                    if not lines[y + j][x + i].isdigit() and lines[y + j][x + i] != ".":
                        current_number_point.close_to_symbol = True

    if len(current_number_point.points) > 0:
        number_to_points.append(current_number_point)

point_to_number = {}
for n in number_to_points:
    for p in n.points:
        point_to_number[p] = n

summed = sum([points_to_number(n.points) for n in number_to_points if n.close_to_symbol])
print(summed)

# part 2
gear_points = []
for y in range(xy_lines.shape[0]):
    for x in range(xy_lines.shape[1]):
        if xy_lines[y, x] == "*":
            gear_points.append((x, y))

gear_sum = []
for gear_point in gear_points:
    # find numbers close to gear point
    close_points = []
    x, y = gear_point
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x + i < 0 or y + j < 0 or x + i >= xy_lines.shape[0] or y + j >= xy_lines.shape[1]:
                continue
            elif xy_lines[y + j, x + i].isdigit():
                close_points.append((x + i, y + j))

    gear_numbers = list(set([point_to_number[p] for p in close_points if p in point_to_number]))

    if len(gear_numbers) == 2:
        gear_sum.append(points_to_number(gear_numbers[0].points) * points_to_number(gear_numbers[1].points))

print(sum(gear_sum))
