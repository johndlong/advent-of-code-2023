"""Day 17: Clumsy Crucible"""

from __future__ import annotations
import asyncio
from argparse import ArgumentParser
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import sys
import uuid


class Direction(Enum):
    """Defines the possible direction"""

    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)


@dataclass
class GridEntry:
    """Represents an entry in the grid."""

    value: int
    paths: list[Path]


@dataclass
class Path:
    """Represents a path entry when calculating distances."""

    uuid: uuid.UUID
    parent_uuid: Optional[uuid.UUID] = None
    value: list[int]
    travelled: list[tuple[int, int]]
    directions: list[Direction]


@dataclass
class Block:
    """Defines the city block"""

    grid: list[list[GridEntry]]


def read_file(path: str) -> Block:
    """Returns a Block given the file provided."""
    with open(path, encoding="utf-8") as f:
        data = f.read()

    lines = data.splitlines()
    grid = []
    for line in lines:
        row = []
        for pos in line:
            row.append(GridEntry(value=int(pos), paths=[]))
        grid.append(row)
    return Block(grid=grid)


async def part1(space: Block) -> int:
    """Returns the part 1 answer"""

    return await calculate_distances(space)


async def calculate_distances(block: Block) -> int:
    """Returns the minimal heat distance for the given block."""
    paths = [Path(uuid=uuid.uuid4(), value=[0], travelled=[(0, 0)], directions=[])]
    cycle = 1
    minimal = sys.maxsize
    while True:
        print(f"Beginning cycle: {cycle}: paths: {len(paths)}")

        if len(paths) == 0:
            break

        new_paths: list[Path] = []
        tasks = []

        async with asyncio.TaskGroup() as tg:
            tasks.extend([tg.create_task(process_path(p, block)) for p in paths])

        for task in tasks:
            result = task.result()
            if result[0]:
                minimal = min([minimal, min(result[0])])
            for np in result[1]:
                if np.value[-1] >= minimal:
                    continue
                new_paths.append(np)

        optimal_paths: list[Path] = []
        for np in new_paths:
            new_x = np.travelled[-1][0]
            new_y = np.travelled[-1][1]
            direction = np.directions[-1]
            if is_sub_optimal(new_x, new_y, direction, np, block.grid[new_y][new_x]):
                continue
            optimal_paths.append(np)

        paths = optimal_paths
        cycle += 1

    return minimal


async def process_path(path: Path, block: Block) -> tuple[list[int], list[Path]]:
    """Processes a single path instance, figuring out any new paths / final distances."""
    retval = []
    new_paths = []
    pos = path.travelled[-1]

    possible_directions = get_possible_directions(path, height=len(block.grid), width=len(block.grid[0]))
    for direction in possible_directions:
        new_x = pos[0] + direction.value[0]
        new_y = pos[1] + direction.value[1]

        # If we've hit the final position, mark the heat value and we're done.
        if new_x == len(block.grid) - 1 and new_y == len(block.grid[0]) - 1:
            retval.append(path.value[-1] + block.grid[new_y][new_x].value)
            block.grid[new_y][new_x].paths.append(path)
            continue

        # If other paths have hit this point and had a lower value at this point
        # there is no need to continue.  We'lldo a second check between cycles but
        # we can initially rule it out here.
        if is_sub_optimal(new_x, new_y, direction, path, block.grid[new_y][new_x]):
            continue

        np = deepcopy(path)
        np.parent_uuid = np.uuid
        np.uuid = uuid.uuid4()
        np.travelled.append((new_x, new_y))
        np.directions.append(direction)
        np.value.append(np.value[-1] + block.grid[new_y][new_x].value)
        block.grid[new_y][new_x].paths.append(np)

        new_paths.append(np)
    return retval, new_paths


def is_sub_optimal(new_x: int, new_y: int, direction: Direction, path: Path, ge: GridEntry) -> bool:
    """Determines if the path isn't optimal compared to other paths that have hit this position."""
    for other_path in ge.paths:
        if path.uuid[-1] != other_path.uuid[-1] and (new_x, new_y) in other_path.travelled:
            index = other_path.travelled.index((new_x, new_y))

            current_direction_count = 1
            for past_direction in path.directions[::-1]:
                if past_direction == direction:
                    current_direction_count += 1
                    if current_direction_count == 3:
                        break
                else:
                    break

            try:
                if set(other_path.directions[index - current_direction_count - 1 :]) == set([direction]):
                    continue
            except IndexError:
                pass

            if set(other_path.directions[index - current_direction_count :]) == set([direction]):
                if other_path.value[index] < path.value[-1]:
                    return True
    return False


def get_possible_directions(path: Path, height: int, width: int) -> list[Direction]:
    """Returns the possible directions of travel based on a given path."""
    retval = []

    pos = path.travelled[-1]
    for direction in Direction:
        new_x = pos[0] + direction.value[0]
        new_y = pos[1] + direction.value[1]

        # If you loop back on yourself, stop.
        if (new_x, new_y) in path.travelled:
            continue

        # If our current direction is the same as the last two, skip it.
        if len(path.directions) >= 3 and set(path.directions[-3:]) == set([direction]):
            continue

        # If the next position will roll off the grid, skip it.
        if new_x < 0 or new_x >= width or new_y < 0 or new_y >= height:
            continue
        retval.append(direction)
    return retval


async def main():
    """Main entrypoint."""
    parser = ArgumentParser(prog="day17")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    space = read_file(args.filename)
    p1 = await part1(space)
    print(f"Part1: {p1}")


if __name__ == "__main__":
    asyncio.run(main())
