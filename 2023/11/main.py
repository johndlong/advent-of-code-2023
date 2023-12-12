"""Day 11: Cosmic Expansion"""
from __future__ import annotations
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
import argparse


class CosmicEntity(Enum):
    """Defines the possible move directions"""

    EMPTY = "."
    GALAXY = "#"


NamedGalaxy = namedtuple("NamedGalaxy", ["num", "x", "y"])


@dataclass
class Universe:
    """Defines the universe"""

    positions: list[list[CosmicEntity]] = None

    def expand(self) -> Universe:
        """Returns an expanded copy of the universe"""
        # Expand any empty rows of the universe
        new_universe = []
        columns = 0
        expand_rows = []
        for y_pos, y in enumerate(self.positions):
            columns = len(y)
            new_universe.append(y)
            x_set = set(y)
            # if the row is entirely empty, add an additional empty row.
            if x_set == set([CosmicEntity.EMPTY]):
                expand_rows.append(y_pos)

        # Expand any empty columns
        expand_columns = []
        for x in range(columns):
            y_set = set()
            for y, _ in enumerate(self.positions):
                y_set.add(self.positions[y][x])
            # Add a new empty column if we have an entirely empty column
            if y_set == set([CosmicEntity.EMPTY]):
                expand_columns.append(x)

        # Perform expansion...
        for i, x in enumerate(expand_columns):
            for y in range(len(self.positions)):
                # As we expand the columns, we need to consider the additional ones added
                # by previous inserts (hence adding i)
                new_universe[y].insert(x + i, CosmicEntity.EMPTY)
        for i, y_expand in enumerate(expand_rows):
            new_universe.insert(y_expand + i, new_universe[y_expand + i])

        return Universe(new_universe)

    def shortest_pairs(self) -> int:
        """Returns the total of the shortest distance between every galaxy in the universe."""
        total = 0
        galaxies = []
        count = 1
        for y, row in enumerate(self.positions):
            for x, pos in enumerate(row):
                if pos == CosmicEntity.GALAXY:
                    galaxies.append(NamedGalaxy(count, x, y))
                    count += 1

        for i, galaxy1 in enumerate(galaxies, 1):
            for galaxy2 in galaxies[i:]:
                total += distance(galaxy1, galaxy2)

        return total


def distance(g1: NamedGalaxy, g2: NamedGalaxy) -> int:
    """Returns the manahattan distance of two galaxies"""
    total = sum(abs(val1 - val2) for val1, val2 in zip([g1.x, g1.y], [g2.x, g2.y]))
    return total


def read_file(path: str) -> Universe:
    """Returns a universe given the file provided."""
    with open(path, encoding="utf-8") as f:
        data = f.read()

    universe = []
    lines = data.splitlines()
    y_len = len(lines)
    x_len = len(lines[0])
    for y in range(y_len):
        row = []
        for x in range(x_len):
            row.append(CosmicEntity.EMPTY)
        universe.append(row)
    for y, line in enumerate(lines):
        for x, pos in enumerate(line):
            universe[y][x] = CosmicEntity(pos)

    return Universe(positions=universe)


def part1(universe: Universe) -> int:
    """Returns the part1 answer."""
    expanded = universe.expand()
    return expanded.shortest_pairs()


def main():
    """Main entrypoint."""
    parser = argparse.ArgumentParser(prog="day11")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    universe = read_file(args.filename)
    p1 = part1(universe)
    print(f"Part 1: {p1}")


if __name__ == "__main__":
    main()
