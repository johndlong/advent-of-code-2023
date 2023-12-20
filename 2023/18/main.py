"""--- Day 18: Lavaduct Lagoon ---"""

from __future__ import annotations
from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple, Optional
import re


class Direction(NamedTuple):
    """Defines the possible direction"""

    dx: int
    dy: int

    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)


NORTH = Direction(dx=0, dy=-1)
EAST = Direction(dx=1, dy=0)
SOUTH = Direction(dx=0, dy=1)
WEST = Direction(dx=-1, dy=0)

direction_map = {
    "R": EAST,
    "D": SOUTH,
    "L": WEST,
    "U": NORTH,
}


class State(Enum):
    """Defines the possible states"""

    LEVEL = "."
    DUG = "#"


@dataclass
class GridEntry:
    """Defines a grid entry"""

    state: State
    edge: bool = False
    color: Optional[str] = ""


class Field(NamedTuple):
    """Defines the space"""

    start: tuple[int, int]
    grid: list[list[GridEntry]]

    @classmethod
    def initialize(cls, start: tuple[int, int], columns: int, rows: int) -> Field:
        grid = []
        for _ in range(rows):
            grid.append([GridEntry(state=State.LEVEL) for _ in range(columns)])
        grid[start[1]][start[0]].state = State.DUG
        return Field(start=start, grid=grid)

    def dig(self, instructions: list[Instruction]):
        x = self.start[0]
        y = self.start[1]

        hit_x_0 = False
        hit_y_0 = False
        for inst in instructions:
            direction = direction_map[inst.direction]
            for _ in range(inst.count):
                x += 1 * direction.dx
                y += 1 * direction.dy

                if x == 0:
                    hit_x_0 = True
                if y == 0:
                    hit_y_0 = True

                self.grid[y][x].state = State.DUG
                self.grid[y][x].color = inst.color

        if not hit_x_0 or not hit_y_0:
            pass

    def mark_edges(self):
        for y, row in enumerate(self.grid):
            # Mark any Left -> Right edges on each row
            for ge in row:
                if ge.state == State.DUG:
                    break
                ge.edge = True

            # Mark any Left -> Right edges on each row
            for ge in row[::-1]:
                if ge.state == State.DUG:
                    break
                ge.edge = True

        # Mark North->South edges
        for x in range(len(self.grid[0])):
            for y in range(len(self.grid)):
                if self.grid[y][x].state == State.DUG:
                    break
                self.grid[y][x].edge = True

            for y in range(len(self.grid) - 1, -1, -1):
                if self.grid[y][x].state == State.DUG:
                    break
                self.grid[y][x].edge = True

    def fill(self):
        for row in self.grid:
            for pos in row:
                if pos.state == State.LEVEL and not pos.edge:
                    pos.state = State.DUG

    def count_fill(self):
        return len([x for y in self.grid for x in y if x.state == State.DUG])


class Instruction(NamedTuple):
    """Defines the set of instructions."""

    direction: str
    count: int
    color: str


def read_file(path: str) -> tuple[Field, list[Instruction]]:
    """Returns a Space given the file provided."""
    with open(path, encoding="utf-8") as f:
        data = f.read()

    inst_re = re.compile(r"(\w+)\s+(\d+)\s+\((.*)\)")
    instructions = []

    for line in data.splitlines():
        match = inst_re.match(line)
        instructions.append(Instruction(direction=match.group(1), count=int(match.group(2)), color=match.group(3)))

    min_row = 0
    max_row = 0
    min_column = 0
    max_column = 0

    pos = (0, 0)
    for inst in instructions:
        direction = direction_map[inst.direction]
        ny = pos[1] + direction.dy * inst.count
        nx = pos[0] + direction.dx * inst.count

        pos = (nx, ny)

        min_row = min(min_row, ny)
        max_row = max(max_row, ny)
        min_column = min(min_column, nx)
        max_column = max(max_column, nx)

    columns = max_column - min_column + 1
    rows = max_row - min_row + 1

    field = Field.initialize(start=(-min_column, -min_row), columns=columns, rows=rows)
    return (field, instructions)


def part1(field: Field, instructions: list[Instruction]) -> int:
    """Returns the part 1 answer"""
    field.dig(instructions)
    field.mark_edges()
    field.fill()
    return field.count_fill()


def main():
    """Main entrypoint."""
    parser = ArgumentParser(prog="day18")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    field, instructions = read_file(args.filename)
    p1 = part1(field, instructions)
    print(f"Part1: {p1}")


if __name__ == "__main__":
    main()
