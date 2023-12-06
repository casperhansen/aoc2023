from dataclasses import dataclass
import numpy as np
import tqdm


def loadfile(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        return lines


def process_input(filename):
    lines = loadfile(filename)

    seeds = [int(v) for v in lines[0].split(":")[-1].split(" ") if v != ""]

    mapper_dict = {}
    mapper_reverse_dict = {}
    for i in range(2, len(lines)):
        line = lines[i]
        # print(line)
        if "map" in line:
            source = line.split("-to-")[0].strip()
            destination = line.split("-to-")[1].split(" ")[0].strip()
            mapper_dict[source] = (destination, [])
            mapper_reverse_dict[destination] = (source, [])
        elif len(line) > 0 and line[0].isdigit():
            nums = [int(v) for v in line.split(" ")]
            destination_range_start = nums[0]
            source_range_start = nums[1]
            range_length = nums[2]

            mapper = (destination_range_start, source_range_start, range_length)

            mapper_dict[source][1].append(mapper)
            mapper_reverse_dict[destination][1].append(mapper)

        elif line == "":
            pass

    return mapper_dict, mapper_reverse_dict, seeds


def apply_mapping(mapping, source_val):
    destination_range_start, source_range_start, range_length = mapping
    return (
        destination_range_start + (source_val - source_range_start)
        if (source_val >= source_range_start) and (source_val < (source_range_start + range_length))
        else None
    )


def apply_reverse_mapping(mapping, destination_val):
    destination_range_start, source_range_start, range_length = mapping
    return (
        destination_val - destination_range_start + source_range_start
        if (destination_val >= destination_range_start) and (destination_val < (destination_range_start + range_length))
        else None
    )


_, mapper_reverse_dict, seeds = process_input("data/5.txt")


seed_pairs = [seeds[i : i + 2] for i in range(0, len(seeds), 2)]


def searcher(location, location_stop):
    while True:
        source = "location"
        current_value = location

        while source != "seed":
            mapper = mapper_reverse_dict[source][1]
            destination = mapper_reverse_dict[source][0]

            possible_values = [v for v in [apply_reverse_mapping(m, current_value) for m in mapper] if v != None]
            current_value = possible_values[0] if len(possible_values) > 0 else current_value
            source = destination

        for seed_pair in seed_pairs:
            start, end = seed_pair
            if start <= current_value and current_value < start + end:
                print("seed=", current_value, "location=", location)
                # return_dict[step_add] = location
                return location

        location += 1
        if location > location_stop:
            return np.inf


import multiprocessing as mp

# make my shitty code faster
if __name__ == "__main__":
    maximum = 100 * 1000000
    values = [[x * 100000, (x + 1) * 100000] for x in range(maximum // 100000)]

    for i in range(100):
        take_ten = values[i * 10 : (i + 1) * 10]
        with mp.Pool(10) as pool:
            results = pool.starmap(searcher, take_ten)

        print(i, results)
        print(min(results))
        if min(results) != np.inf:
            break
