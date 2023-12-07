""" Day 7: Camel Cards s"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
import re


class FaceCard(IntEnum):
    """Defines the values of Face Cards."""

    A = 14
    K = 13
    Q = 12
    JACK = 11
    T = 10
    JOKER = 1


face_card_names = {x.name for x in FaceCard}


class HandRank(IntEnum):
    """Defines the values of Hand Rankings"""

    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


@dataclass
class Card:
    """Defines a specific card."""

    value: int

    @classmethod
    def to_card(cls, data: str, joker: bool = False) -> Card:
        """Returns a Card object based on the string."""
        if data == "J":
            if joker:
                return Card(value=FaceCard.JOKER)
            return Card(value=FaceCard.JACK)

        if data in face_card_names:
            return Card(value=FaceCard[data])
        return Card(value=int(data))


@dataclass
class Hand:
    """Defines a Hand"""

    cards: list[Card]
    bid: int = 0

    # pylint: disable=too-many-return-statements
    def rank(self) -> HandRank:
        """Calculates the rank of the provided hand based with support for jokers."""
        hand_set = Counter([x.value for x in self.cards])

        if num_jokers := hand_set[FaceCard.JOKER]:
            del hand_set[FaceCard.JOKER]
            # If you have 5 jokers, then convert them to all Aces.
            if num_jokers == 5:
                hand_set[FaceCard.A] = num_jokers
            # Otherwise, add the number of jokers to the current most common card
            # to maximize the hand rank
            else:
                most_common = hand_set.most_common(1)[0]
                hand_set[most_common[0]] += num_jokers

        return self.legacy_rank(hand_set)

    # pylint: disable=too-many-return-statements
    def legacy_rank(self, hand_set: Counter) -> HandRank:
        """Calculates the rank of the provided hand based on non-joker support."""
        length = len(hand_set)
        if length == 1:
            return HandRank.FIVE_OF_A_KIND
        if length == 2:
            if hand_set.most_common(1)[0][1] == 4:
                return HandRank.FOUR_OF_A_KIND
            return HandRank.FULL_HOUSE
        if length == 3:
            most_common = hand_set.most_common(2)
            if most_common[0][1] == 3:
                return HandRank.THREE_OF_A_KIND
            return HandRank.TWO_PAIR
        if length == 4:
            return HandRank.ONE_PAIR
        return HandRank.HIGH_CARD

    def __eq__(self, other: Hand) -> bool:
        """Evaulate whether two hands are equal."""
        return self.cards == other.cards

    def __lt__(self, other: Hand) -> bool:
        """Evaluate whether a hand is lt another based on rank/card order."""
        if self.rank() == other.rank():
            for i, val in enumerate(self.cards):
                if val == other.cards[i]:
                    continue
                return val.value < other.cards[i].value
        return self.rank() < other.rank()

    @classmethod
    def read_file(cls, path: str, joker: bool = False) -> list[Hand]:
        """Returns a list of hands after reading the provided file"""
        with open(path, encoding="utf-8") as f:
            data = f.read()

        retval = []
        regex = re.compile(r"^(.*)\s+(\d+)$")
        for line in data.splitlines():
            if result := regex.match(line):
                hand = Hand(cards=[Card.to_card(c, joker=joker) for c in result.group(1)], bid=int(result.group(2)))
                retval.append(hand)
            else:
                raise ValueError(f"failed reading line: {line}")

        return retval


def winning_total(hands: list[Hand]) -> int:
    """Part 1 calculator."""
    ranked_hands = sorted(hands)
    retval = 0
    for i, hand in enumerate(ranked_hands, 1):
        retval += i * hand.bid
    return retval


def main():
    """Main entrypoint."""
    part1 = winning_total(Hand.read_file("2023/07/data.txt"))
    print(f"Part1: {part1}")

    part2 = winning_total(Hand.read_file("2023/07/data.txt", joker=True))
    print(f"Part2: {part2}")


if __name__ == "__main__":
    main()
