def loadfile(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        return lines


inp = loadfile("data/1.txt")

word_to_digit_mapper = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

nums = []
for line in inp:
    numbers = []
    for i in range(len(line)):
        if line[i].isdigit():
            numbers.append(line[i])
        for word in word_to_digit_mapper:
            if line[i:].startswith(word):
                numbers.append(word_to_digit_mapper[word])
                break

    nums.append(numbers[0] + numbers[-1])

print(sum([int(n) for n in nums]))
