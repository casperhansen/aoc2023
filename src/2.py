import numpy as np


def loadfile(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        return lines


inp = loadfile("data/2.txt")

colors = ["red", "blue", "green"]
rules = {"red": 12, "green": 13, "blue": 14}
num_balls = 3

possible_games = []
part_2_minimum_sets = []
for line in inp:
    game_num = int(line.split(":")[0].split(" ")[1])
    rounds = line.split(":")[1].split(";")
    round_arr = np.array([np.zeros(num_balls) for _ in range(len(rounds))])
    for i, round in enumerate(rounds):
        balls = round.split(",")
        for ball in balls:
            ball = ball.strip()
            ball_num, ball_color = ball.split(" ")
            round_arr[i, colors.index(ball_color)] = int(ball_num)

    possible = True
    for hand in round_arr:
        if any([hand[colors.index(color)] > rules[color] for color in colors]):
            possible = False
            break

    if possible:
        possible_games.append(game_num)

    part_2_minimum_sets.append(np.max(round_arr, axis=0))

print(sum(possible_games))

print(np.sum([np.prod(elm) for elm in part_2_minimum_sets]))
