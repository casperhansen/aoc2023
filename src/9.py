import copy


def loadfile(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        return lines


def process_reading(reading: list[int], part_one: bool = True) -> int:
    readings = [reading]
    while True:
        last_reading = readings[-1]
        next_reading = [last_reading[i] - last_reading[i - 1] for i in range(1, len(last_reading))]
        readings.append(next_reading)
        if all([v == 0 for v in next_reading]):
            break
    for i in range(1, len(readings)):
        if part_one:
            readings[len(readings) - i - 1].append(
                readings[len(readings) - i - 1][-1] + readings[len(readings) - i][-1]
            )
        else:
            readings[len(readings) - i - 1] = [
                readings[len(readings) - i - 1][0] - readings[len(readings) - i][0]
            ] + readings[len(readings) - i - 1]

    if part_one:
        predictions = [readings[i][-1] for i in range(len(readings))]
    else:
        predictions = [readings[i][0] for i in range(len(readings))]
    return predictions[0]


def main():
    lines = loadfile("data/9.txt")
    readings = [[int(v) for v in line.split(" ")] for line in lines]

    preds = []
    for reading in copy.deepcopy(readings):
        preds.append(process_reading(reading, part_one=True))

    print(sum(preds))
    preds = []
    for reading in copy.deepcopy(readings):
        preds.append(process_reading(reading, part_one=False))

    print(sum(preds))


if __name__ == "__main__":
    main()
