"""Day 14: Parabolic Reflector Dish"""

from __future__ import annotations
from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum


class Item(Enum):
    """Defines the possible items"""

    ROUNDED_ROCK = "O"
    CUBE_ROCK = "#"
    EMPTY_SPACE = "."


class Direction(Enum):
    """Defines the possible direction"""

    NORTH = "N"


@dataclass
class Platform:
    """Defines the Platform"""

    positions: list[list[Item]]

    def slide(self, direction: Direction = Direction.NORTH) -> None:
        """Slides the platform in a specified direction (only N currently)"""
        if direction != Direction.NORTH:
            raise ValueError("slide direction not supported")

        # We'll keep performing one-row up changes until we have a pass through
        # where nothing changes.
        while True:
            complete = True
            for i, row in enumerate(self.positions[1:], 1):
                for j, entry in enumerate(row):
                    if entry == Item.ROUNDED_ROCK:
                        # If the above entry is empty space, move the rounded rock up
                        # a position and backfill with an empty space.
                        if self.positions[i - 1][j] == Item.EMPTY_SPACE:
                            self.positions[i - 1][j] = Item.ROUNDED_ROCK
                            self.positions[i][j] = Item.EMPTY_SPACE
                            complete = False
            if complete:
                break

    def total_load(self) -> int:
        """Returns the load on the platform given the current state"""
        retval = 0

        # Start from the bottom, count the number of round rocks and
        # increment the retval by i*N
        for i, row in enumerate(reversed(self.positions), 1):
            for entry in row:
                row_count = 0
                if entry == Item.ROUNDED_ROCK:
                    row_count += 1
                retval += i * row_count

        return retval


def read_file(path: str) -> Platform:
    """Returns a platform given the file provided."""
    with open(path, encoding="utf-8") as f:
        data = f.read()

    lines = data.splitlines()
    platform = []
    for line in lines:
        row = []
        for pos in line:
            row.append(Item(pos))
        platform.append(row)
    return Platform(positions=platform)


def part1(platform: Platform) -> int:
    """Returns the part 1 answer"""
    platform.slide()
    return platform.total_load()


def main():
    """Main entrypoint."""
    parser = ArgumentParser(prog="day14")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    platform = read_file(args.filename)
    p1 = part1(platform)
    print(f"Part1: {p1}")


if __name__ == "__main__":
    main()
