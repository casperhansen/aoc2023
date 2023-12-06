from dataclasses import dataclass


def loadfile(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        return lines


def process_input(filename):
    lines = loadfile(filename)

    seeds = [int(v) for v in lines[0].split(":")[-1].split(" ") if v != ""]

    mapper_dict = {}
    for i in range(2, len(lines)):
        line = lines[i]
        # print(line)
        if "map" in line:
            source = line.split("-to-")[0].strip()
            destination = line.split("-to-")[1].split(" ")[0].strip()
            mapper_dict[source] = (destination, [])
        elif len(line) > 0 and line[0].isdigit():
            nums = [int(v) for v in line.split(" ")]
            destination_range_start = nums[0]
            source_range_start = nums[1]
            range_length = nums[2]

            mapper = (destination_range_start, source_range_start, range_length)

            mapper_dict[source][1].append(mapper)

        elif line == "":
            pass

    return mapper_dict, seeds


def apply_mapping(mapping, source_val):
    destination_range_start, source_range_start, range_length = mapping
    return (
        destination_range_start + (source_val - source_range_start)
        if (source_val >= source_range_start) and (source_val < (source_range_start + range_length))
        else None
    )


mapper_dict, seeds = process_input("data/5.txt")
values = []
for seed in seeds:
    source = "seed"
    current_value = seed

    while source != "location":
        source_mapper = mapper_dict[source][1]
        destination = mapper_dict[source][0]

        possible_values = [v for v in [apply_mapping(m, current_value) for m in source_mapper] if v != None]
        current_value = possible_values[0] if len(possible_values) > 0 else current_value
        source = destination

    values.append(current_value)

print(values)
print(min(values))
