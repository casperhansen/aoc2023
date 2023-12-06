from dataclasses import dataclass


def loadfile(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        return lines


lines = loadfile("data/4.txt")


@dataclass
class Card:
    winning_numbers: set
    numbers: list
    order_number: int


points = []
initial_cards = []
for i, line in enumerate(lines):
    all_numbers = line.split(":")[-1]
    winning_numbers = set([int(v) for v in all_numbers.split("|")[0].strip().split(" ") if v != ""])
    numbers = [int(v) for v in all_numbers.split("|")[1].strip().split(" ") if v != ""]
    card = Card(winning_numbers, numbers, i + 1)
    initial_cards.append(card)
    matches = sum([1 for n in card.numbers if n in card.winning_numbers])
    if matches > 0:
        points.append(2 ** (matches - 1))

print(sum(points))


# part 2
def eval_card(card):
    return sum([1 for n in card.numbers if n in card.winning_numbers])


card_to_moreCards = {card.order_number: 0 for card in initial_cards}
card_to_moreCards[initial_cards[-1].order_number] = 0

# initial pass
for card in initial_cards[::-1][1:]:
    score = eval_card(card)
    order_number = card.order_number
    new_cards = [num for num in range(order_number + 1, order_number + score + 1)]
    card_to_moreCards[order_number] = score

for card in initial_cards[::-1][1:]:
    score = eval_card(card)
    order_number = card.order_number
    new_cards = [num for num in range(order_number + 1, order_number + score + 1)]
    card_to_moreCards[order_number] = sum([card_to_moreCards[num] for num in new_cards]) + score

print(sum([card_to_moreCards[card.order_number] for card in initial_cards]) + len(initial_cards))
