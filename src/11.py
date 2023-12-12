import numpy as np
from dataclasses import dataclass
from itertools import combinations


def print_map(map):
    for i in range(len(map)):
        print("".join(map[i]))


def print_map_int(map):
    for i in range(len(map)):
        print(" ".join([str(elm) for elm in map[i]]))


def loadfile(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        return lines


def distance_map(map, weight=1):
    distance_map = np.ones((len(map), len(map[0])))
    expand_horizontal = []
    expand_vertical = []

    small_add = 0.000001
    adder = 0.000001

    for i in range(len(map)):
        if all([elm == "." for elm in map[i]]):
            distance_map[i, :] += weight + small_add
            small_add += adder

    for j in range(len(map[0])):
        column = [map[i][j] for i in range(len(map))]
        if all([elm == "." for elm in column]):
            distance_map[:, j] += weight + small_add
            small_add += adder

    # distance_map = distance_map.astype(int)
    # add_something = 0.00000000001
    # adder = 0.00000000001
    # for y in range(len(map)):
    #     for x in range(len(map[0])):
    #         distance_map[y, x] += add_something
    #         add_something += adder

    return distance_map.astype(float)


def expand_map(map):
    expand_horizontal = []
    expand_vertical = []

    for i in range(len(map)):
        if all([elm == "." for elm in map[i]]):
            expand_horizontal.append(i)

    for j in range(len(map[0])):
        column = [map[i][j] for i in range(len(map))]
        if all([elm == "." for elm in column]):
            expand_vertical.append(j)

    new_horizontal = ["."] * len(map[0])

    for i in range(len(expand_horizontal)):
        map.insert(expand_horizontal[i] + i, new_horizontal)
    for i in range(len(expand_vertical)):
        for j in range(len(map)):
            map[j][expand_vertical[i]] = [".", "."]

    for i in range(len(map)):
        map[i] = [elm if type(elm) == list else [elm] for elm in map[i]]
        map[i] = [elm for sublist in map[i] for elm in sublist]
    return map


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"


def hamming_distance(p1, p2, dist_map, weight):
    extra_dists = []
    assert np.floor(dist_map[p1.y, p1.x]) == 1
    assert np.floor(dist_map[p2.y, p2.x]) == 1

    xmin = min(p1.x, p2.x)
    for y in range(min(p1.y, p2.y), max(p1.y, p2.y) + 1):
        if dist_map[y, xmin] > 1:
            extra_dists.append(dist_map[y, xmin])
    ymin = min(p1.y, p2.y)
    for x in range(min(p1.x, p2.x), max(p1.x, p2.x) + 1):
        if dist_map[ymin, x] > 1:
            extra_dists.append(dist_map[ymin, x])

    set_extra_dists = set(extra_dists)
    extra_dists = len(set(extra_dists))
    dist = abs(p1.x - p2.x) + abs(p1.y - p2.y) + extra_dists * weight - extra_dists
    print(p1, p2, dist, extra_dists, set_extra_dists)
    return dist


def main():
    map = loadfile("data/11.txt")
    map = [list(l) for l in map]

    dist_map = distance_map(map)
    print_map(map)
    print_map_int(dist_map)

    galaxies = []
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == "#":
                galaxies.append(Point(x, y))

    print(len(galaxies))

    galaxy_pairs = list(combinations(galaxies, 2))
    print(len(galaxy_pairs))

    hamming_distances = [hamming_distance(p1, p2, dist_map, weight=1000000.0) for p1, p2 in galaxy_pairs]
    print(sum(hamming_distances))


if __name__ == "__main__":
    main()
