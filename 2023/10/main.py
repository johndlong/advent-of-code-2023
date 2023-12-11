"""Day 10: Pipe Maze"""
from __future__ import annotations
import sys
from dataclasses import dataclass
from enum import Enum
import argparse


class Move(Enum):
    """Defines the possible move directions"""

    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)


class Pipe(Enum):
    """Defines the types of pipes"""

    VERTICAL = "|"
    HORIZONTAL = "-"
    N_E_BEND = "L"
    N_W_BEND = "J"
    S_W_BEND = "7"
    S_E_BEND = "F"
    GROUND = "."
    STARTING = "S"


move_map = {
    Move.N: [Pipe.VERTICAL, Pipe.S_E_BEND, Pipe.S_W_BEND],
    Move.E: [Pipe.HORIZONTAL, Pipe.N_W_BEND, Pipe.S_W_BEND],
    Move.S: [Pipe.VERTICAL, Pipe.N_E_BEND, Pipe.N_W_BEND],
    Move.W: [Pipe.HORIZONTAL, Pipe.N_E_BEND, Pipe.S_E_BEND],
}


@dataclass
class Position:
    """Defines a grid position"""

    pipe: Pipe
    distance: int = 0


@dataclass
class Grid:
    """Defines the grid"""

    positions: list[list[Position]] = None

    def find_starting(self) -> tuple(int, int):
        """Returns the start point within the grid."""
        for y, y_list in enumerate(self.positions):
            for x, pos in enumerate(y_list):
                if pos.pipe == Pipe.STARTING:
                    return (x, y)
        raise ValueError("didn't find starting position")

    def travel_distance(self, positions: tuple[int, int], distance: int = 1):
        """Traverses the grid, setting distances as it moves"""
        next_moves = []
        for position in positions:
            for move in [Move.N, Move.E, Move.S, Move.W]:
                next_x = position[0] + move.value[0]
                next_y = position[1] + move.value[1]

                try:
                    next_pos = self.positions[next_y][next_x]
                    if next_pos.pipe in move_map[move] and next_pos.distance == 0:
                        next_moves.append((next_x, next_y))
                        next_pos.distance = distance
                except IndexError:
                    continue
        if len(next_moves) == 0:
            return

        self.travel_distance(next_moves, distance + 1)

    def max_distance(self) -> int:
        """Returns the max distance after moving from the starting point."""
        start_x, start_y = self.find_starting()
        self.travel_distance([(start_x, start_y)])
        max_distance = 0
        for y, y_row in enumerate(self.positions):
            for x, _ in enumerate(y_row):
                if self.positions[y][x].distance > max_distance:
                    max_distance = self.positions[y][x].distance
        return max_distance


def read_file(path: str) -> Grid:
    """Returns a grid given the file provided."""
    with open(path, encoding="utf-8") as f:
        data = f.read()

    grid = []
    lines = data.splitlines()
    y_len = len(lines)
    x_len = len(lines[0])
    for y in range(y_len):
        row = []
        for x in range(x_len):
            row.append(Position(Pipe(Pipe.GROUND)))
        grid.append(row)
    for y, line in enumerate(lines):
        for x, pos in enumerate(line):
            grid[y][x] = Position(Pipe(pos))

    return Grid(positions=grid)


def main():
    """Main entrypoint."""
    sys.setrecursionlimit(10000)
    parser = argparse.ArgumentParser(prog="day10")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    grid = read_file(args.filename)
    distance = grid.max_distance()
    print(f"Part 1: {distance}")


if __name__ == "__main__":
    main()
