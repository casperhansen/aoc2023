import numpy as np


def loadfile(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        return lines


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
        # five of a kind
        if len(set(self.cards)) == 1:
            return 1000 + self._sum()
        # four of a kind
        if len(set(self.cards)) == 2:
            if any([self.cards.count(c) == 4 for c in self.cards]):
                return 900 + self._sum()
        # full house
        if len(set(self.cards)) == 2:
            if any([self.cards.count(c) == 3 for c in self.cards]) and any(
                [self.cards.count(c) == 2 for c in self.cards]
            ):
                return 800 + self._sum()
        # three of a kind
        if len(set(self.cards)) == 3:
            if any([self.cards.count(c) == 3 for c in self.cards]):
                return 700 + self._sum()
        # two pairs
        if len(set(self.cards)) == 3:
            distinct_cards = set(self.cards)
            if sum([self.cards.count(c) == 2 for c in distinct_cards]) == 2:
                return 600 + self._sum()
        # one pair
        if len(set(self.cards)) == 4:
            distinct_cards = set(self.cards)
            if sum([self.cards.count(c) == 2 for c in distinct_cards]) == 1:
                return 500 + self._sum()
        # high card
        if len(set(self.cards)) == 5:
            return 400 + self._sum()
        raise Exception("Something went wrong")


def main():
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
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

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
