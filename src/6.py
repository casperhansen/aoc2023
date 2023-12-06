from dataclasses import dataclass
from math import sqrt, ceil, floor
import re
import numpy as np


def loadfile(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        return lines


def process_input(fname):
    inp = loadfile(fname)
    times = re.findall(r"\d+", inp[0])
    dists = re.findall(r"\d+", inp[1])
    all_times_one = re.findall(r"\d+", inp[0].replace(" ", ""))
    all_dists_one = re.findall(r"\d+", inp[1].replace(" ", ""))

    rounds = [(int(v[0]), int(v[1])) for v in zip(times, dists)]
    rounds += [(int(v[0]), int(v[1])) for v in zip(all_times_one, all_dists_one)]
    return rounds


inp = process_input("data/6.txt")


values = []
for T, D in inp:
    d = T**2 - 4 * D
    eps = 0.0000000000001
    vals = (-T + sqrt(d)) / -2, (-T - sqrt(d)) / -2
    from_val = ceil(min(vals) + eps)
    to_val = floor(max(vals) - eps)
    values.append(to_val - from_val + 1)

print(np.prod(values[:-1]))
print(values[-1])
