"""Day 13: Point of Incidence"""

from __future__ import annotations
from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Item(Enum):
    """Defines the possible items"""

    ASH = "."
    ROCK = "#"


@dataclass
class Land:
    """Defines the Land"""

    num: int = 0
    positions: list[list[Item]] = None
    vertical: bool = True

    def horizontal_mirror(self) -> Optional[int]:
        """Returns the horizontal mirror position"""
        return horizontal_mirror(self.positions)

    def veritical_mirror(self) -> Optional[int]:
        """Returns the vertical mirror position"""
        vertical = [[self.positions[j][i] for j in range(len(self.positions))] for i in range(len(self.positions[0]))]
        return horizontal_mirror(vertical)


def horizontal_mirror(positions: list[list[Item]]) -> Optional[int]:
    """Calculates the horizontal mirror position for the provided list."""
    for idx in range(len(positions)):
        if idx == 0:
            continue

        if all(l == r for l, r in zip(reversed(positions[:idx]), positions[idx:])):
            return idx

    return None


def read_file(path: str) -> Land:
    """Returns a group of Lands given the file provided."""
    with open(path, encoding="utf-8") as f:
        data = f.read()

    lands = []
    groups = data.split("\n\n")
    for i, group in enumerate(groups):
        lines = group.splitlines()
        land = []
        for line in lines:
            row = []
            for pos in line:
                row.append(Item(pos))
            land.append(row)
        lands.append(Land(num=i + 1, positions=land))

    return lands


def part1(lands: list[Land]) -> int:
    """Returns the part 1 answer"""
    retval = 0
    for land in lands:
        horizontal_result = land.horizontal_mirror()
        vertical_result = land.veritical_mirror()

        if horizontal_result and vertical_result:
            pass

        if horizontal_result:
            retval += horizontal_result * 100
        elif vertical_result:
            retval += vertical_result

    return retval


def main():
    """Main entrypoint."""
    parser = ArgumentParser(prog="day13")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    lands = read_file(args.filename)
    p1 = part1(lands)
    print(f"Part1: {p1}")


if __name__ == "__main__":
    main()
