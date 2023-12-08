from math import lcm


def loadfile(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        return lines


def main():
    lines = loadfile("data/8.txt")
    lr_instruction = list(lines[0])
    map = {}
    for i in range(2, len(lines)):
        line = lines[i]
        here = line.split("=")[0].strip()
        left, right = line.split("=")[1].strip()[1:-1].replace(" ", "").split(",")

        map[here] = {"L": left, "R": right}

    here = "AAA"
    end = "ZZZ"
    counter = 0
    while here != end:
        for instruction in lr_instruction:
            here = map[here][instruction]
            counter += 1
            if here == end:
                break

    print(counter)


def main2():
    lines = loadfile("data/8.txt")
    lr_instruction = list(lines[0])
    map = {}
    for i in range(2, len(lines)):
        line = lines[i]
        here = line.split("=")[0].strip()
        left, right = line.split("=")[1].strip()[1:-1].replace(" ", "").split(",")

        map[here] = {"L": left, "R": right}

    here_nodes = [s for s in map.keys() if s.endswith("A")]
    steps_before_end = []
    for here in here_nodes:
        steps = 0
        while not here.endswith("Z"):
            for instruction in lr_instruction:
                here = map[here][instruction]
                steps += 1
        steps_before_end.append(steps)
    print(lcm(*steps_before_end))


if __name__ == "__main__":
    main()
    main2()
