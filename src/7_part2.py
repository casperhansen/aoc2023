import numpy as np


def loadfile(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        return lines


card_mapper = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 1,  # Joker
    "Q": 12,
    "K": 13,
    "A": 14,
}


class Hand:
    def __init__(self, bid, cards):
        self.bid = int(bid)
        self.cards = cards

    def __lt__(self, other):
        myscore = self.score()
        otherscore = other.score()
        if myscore == otherscore:
            for i in range(len(self.cards)):
                if self.cards[i] == other.cards[i]:
                    continue
                return self.cards[i] < other.cards[i]
        return myscore < otherscore

    def __repr__(self) -> str:
        return f"Hand({self.bid}, {self.cards}, {self.score()})"

    def _sum(self):
        return 0

    def score(self):
        if self.cards.count(card_mapper["J"]) > 0:
            # create a hand with each possible value of the joker
            hands = [self.cards]
            while any([card_mapper["J"] in h for h in hands]):
                new_hands = []
                for cards in hands:
                    tmp_cards = cards.copy()
                    if card_mapper["J"] in tmp_cards:
                        for i in range(2, 15):
                            new_card = tmp_cards.copy()
                            new_card[new_card.index(card_mapper["J"])] = i
                            new_hands.append(new_card)
                hands = new_hands

            scores = [self._score(h) for h in hands]
            return max(scores)
        else:
            return self._score(self.cards)

    def _score(self, cards):
        # five of a kind
        if len(set(cards)) == 1:
            return 1000 + self._sum()
        # four of a kind
        if len(set(cards)) == 2:
            if any([cards.count(c) == 4 for c in cards]):
                return 900 + self._sum()
        # full house
        if len(set(cards)) == 2:
            if any([cards.count(c) == 3 for c in cards]) and any([cards.count(c) == 2 for c in cards]):
                return 800 + self._sum()
        # three of a kind
        if len(set(cards)) == 3:
            if any([cards.count(c) == 3 for c in cards]):
                return 700 + self._sum()
        # two pairs
        if len(set(cards)) == 3:
            distinct_cards = set(cards)
            if sum([cards.count(c) == 2 for c in distinct_cards]) == 2:
                return 600 + self._sum()
        # one pair
        if len(set(cards)) == 4:
            distinct_cards = set(cards)
            if sum([cards.count(c) == 2 for c in distinct_cards]) == 1:
                return 500 + self._sum()
        # high card
        if len(set(cards)) == 5:
            return 400 + self._sum()
        raise Exception("Something went wrong")


def main():
    lines = loadfile("data/7.txt")
    hands = []
    for line in lines:
        cards, bid = line.split(" ")
        cards = [card_mapper[c] for c in cards]
        hands.append(Hand(bid, cards))

    sorted_hands = sorted(hands)

    for hand in sorted_hands:
        print(hand)

    total_score = [hand.bid * (i + 1) for i, hand in enumerate(sorted_hands)]
    print(sum(total_score))


if __name__ == "__main__":
    main()
