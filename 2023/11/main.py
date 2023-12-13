"""Day 11: Cosmic Expansion"""
from __future__ import annotations
import argparse
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from progressbar import ProgressBar


class CosmicEntity(Enum):
    """Defines the possible move directions"""

    EMPTY = "."
    GALAXY = "#"


NamedGalaxy = namedtuple("NamedGalaxy", ["num", "x", "y"])


@dataclass
class Position:
    """Defines a Position in the Galaxy"""

    val: CosmicEntity
    x: int
    y: int


@dataclass
class Universe:
    """Defines the universe"""

    positions: list[list[Position]] = None

    def expand(self, expansion_number: int = 1) -> Universe:
        """Returns an expanded copy of the universe"""
        # Expand any empty rows of the universe
        new_universe = []
        columns = 0
        expand_rows = []
        for y_pos, y in enumerate(self.positions):
            columns = len(y)
            new_universe.append(y)
            x_set = set([x.val for x in y])
            # if the row is entirely empty, add an additional empty row.
            if x_set == set([CosmicEntity.EMPTY]):
                expand_rows.append(y_pos)

        # Expand any empty columns
        expand_columns = []
        for x in range(columns):
            y_set = set()
            for y, _ in enumerate(self.positions):
                y_set.add(self.positions[y][x].val)
            # Add a new empty column if we have an entirely empty column
            if y_set == set([CosmicEntity.EMPTY]):
                expand_columns.append(x)

        print("Starting Expansion.")
        expands = max(1, expansion_number - 1)

        # Perform expansion...
        progress = ProgressBar(maxval=len(expand_columns) + len(expand_rows)).start()
        count = 0
        for i, x in enumerate(expand_columns, 1):
            progress.update(count + 1)
            count += 1
            for n in range(x, len(self.positions[0])):
                for y in range(len(self.positions)):
                    # # As we expand the columns, we need to consider the additional ones added
                    # # by previous inserts (hence adding i)
                    new_universe[y][n].x += expands * i
                    # new_universe[y] = new_universe[y][:x] + [Position(CosmicEntity.EMPTY] * expands + new_universe[y][x:]
        for i, y_expand in enumerate(expand_rows, 1):
            progress.update(count + 1)
            count += 1
            for x, _ in enumerate(new_universe[y_expand]):
                new_universe[y_expand][x].y += expands * i

        progress.finish()

        return Universe(new_universe)

    def shortest_pairs(self) -> int:
        """Returns the total of the shortest distance between every galaxy in the universe."""
        total = 0
        galaxies = []
        count = 1
        print("Finding galaxies.")
        row_len = len(self.positions[0])
        progress = ProgressBar(maxval=(len(self.positions) + 1) * (row_len + 1) + 1).start()
        p_count = 0
        for row in self.positions:
            for pos in row:
                if pos.val == CosmicEntity.GALAXY:
                    galaxies.append(NamedGalaxy(count, pos.x, pos.y))
                p_count += 1
                progress.update(p_count + 1)
        progress.finish()

        print("Starting Calculating Shortest Pairs.")
        progress = ProgressBar(maxval=len(galaxies)).start()
        for i, galaxy1 in enumerate(galaxies, 1):
            for galaxy2 in galaxies[i:]:
                total += distance(galaxy1, galaxy2)
                progress.update(i + 1)
        progress.finish()

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
    for y, y_row in enumerate(lines):
        row = []
        for x, pos in enumerate(y_row):
            row.append(Position(val=CosmicEntity(pos), x=x, y=y))
        universe.append(row)

    return Universe(positions=universe)


def part1(universe: Universe) -> int:
    """Returns the part1 answer."""
    expanded = universe.expand()
    return expanded.shortest_pairs()


def part2(universe: Universe) -> int:
    """Returns the part2 answer."""
    expanded = universe.expand(expansion_number=1000000)
    return expanded.shortest_pairs()


def main():
    """Main entrypoint."""
    parser = argparse.ArgumentParser(prog="day11")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    universe = read_file(args.filename)
    p1 = part1(universe)
    print(f"Part 1: {p1}")

    universe = read_file(args.filename)
    p2 = part2(universe)
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
