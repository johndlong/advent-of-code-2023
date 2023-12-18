"""Day 16: The Floor Will Be Lava"""

from __future__ import annotations
from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    """Defines the possible direction"""

    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)


class Item(Enum):
    """Defines the possible items"""

    LEFT_90_MIRROR = "/"
    RIGHT_90_MIRROR = "\\"
    VERTICAL_SPLITTER = "|"
    HORIZONTAL_SPLITTER = "-"
    EMPTY_SPACE = "."


reflection_movements = {
    Item.EMPTY_SPACE: {
        Direction.NORTH: [Direction.NORTH],
        Direction.EAST: [Direction.EAST],
        Direction.SOUTH: [Direction.SOUTH],
        Direction.WEST: [Direction.WEST],
    },
    Item.LEFT_90_MIRROR: {  # /
        Direction.NORTH: [Direction.EAST],
        Direction.EAST: [Direction.NORTH],
        Direction.SOUTH: [Direction.WEST],
        Direction.WEST: [Direction.SOUTH],
    },
    Item.RIGHT_90_MIRROR: {  # \
        Direction.NORTH: [Direction.WEST],
        Direction.EAST: [Direction.SOUTH],
        Direction.SOUTH: [Direction.EAST],
        Direction.WEST: [Direction.NORTH],
    },
    Item.VERTICAL_SPLITTER: {  # |
        Direction.NORTH: [Direction.NORTH],
        Direction.EAST: [Direction.NORTH, Direction.SOUTH],
        Direction.SOUTH: [Direction.SOUTH],
        Direction.WEST: [Direction.NORTH, Direction.SOUTH],
    },
    Item.HORIZONTAL_SPLITTER: {  # -
        Direction.NORTH: [Direction.EAST, Direction.WEST],
        Direction.EAST: [Direction.EAST],
        Direction.SOUTH: [Direction.EAST, Direction.WEST],
        Direction.WEST: [Direction.WEST],
    },
}


@dataclass
class GridEntry:
    """Represents an entry in the grid."""

    value: Item
    energized: list[Direction]


@dataclass
class Space:
    """Defines the space"""

    grid: list[list[GridEntry]]

    def energized_count(self) -> int:
        """Returns the energized count within the grid."""
        return len([x for row in self.grid for x in row if x.energized])

    def light_beam(self):
        """Kicks off a light beam and traverses the grid until all options are exhausted."""
        positions = [
            (
                0,
                0,
                Direction.EAST,
            )
        ]
        while True:
            complete = True
            next_positions = []
            for x, y, direction in positions:
                self.grid[y][x].energized.append(direction)
                nps = self._get_next_positions(x, y, direction)
                if len(nps) > 2:
                    pass
                next_positions.extend([np for np in nps if np not in next_positions])

            if len(next_positions) > 0:
                complete = False

            if complete:
                break

            positions = next_positions
            if len(positions) > 3:
                pass

    def _get_next_positions(self, x, y, direction) -> tuple(int, int, Direction):
        next_positions = []
        next_directions = reflection_movements[self.grid[y][x].value][direction]

        for nd in next_directions:
            next_x = x + nd.value[0]
            next_y = y + nd.value[1]

            if next_x < 0 or next_x >= len(self.grid[0]) or next_y < 0 or next_y >= len(self.grid):
                continue

            if nd in self.grid[next_y][next_x].energized:
                continue

            next_positions.append((next_x, next_y, nd))
        return next_positions


def read_file(path: str) -> Space:
    """Returns a Space given the file provided."""
    with open(path, encoding="utf-8") as f:
        data = f.read()

    lines = data.splitlines()
    grid = []
    for line in lines:
        row = []
        for pos in line:
            row.append(GridEntry(value=Item(pos), energized=[]))
        grid.append(row)
    return Space(grid=grid)


def part1(space: Space) -> int:
    """Returns the part 1 answer"""
    space.light_beam()
    return space.energized_count()


def main():
    """Main entrypoint."""
    parser = ArgumentParser(prog="day16")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    space = read_file(args.filename)
    p1 = part1(space)
    print(f"Part1: {p1}")


if __name__ == "__main__":
    main()
