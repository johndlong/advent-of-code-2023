""" Day 8: Haunted Wasteland """
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import argparse
import asyncio
import re


class Movement(Enum):
    """Defines movement options."""

    LEFT = "L"
    RIGHT = "R"


@dataclass
class Node:
    """Defines a specific node."""

    value: str
    left: str
    right: str


def read_file(path: str) -> tuple[dict[str, Node], list[Movement]]:
    """Returns the root node and movement sequence after reading the provided file."""
    with open(path, encoding="utf-8") as f:
        data = f.read()

    lines = data.splitlines()

    sequence = []
    sequence_regex = re.compile(r"^[LR]+$")

    for sequence_match in sequence_regex.finditer(lines.pop(0)):
        for s in sequence_match.group(0):
            sequence.append(Movement(s))

    nodes = {}
    node_regex = re.compile(r"^(.*)\s+=\s+\((.*),\s+(.*)\)$")
    for line in data.splitlines():
        if result := node_regex.match(line):
            groups = result.groups()
            assert len(groups) == 3
            node = Node(value=groups[0], left=groups[1], right=groups[2])
            nodes[groups[0]] = node
        else:
            # Ignore non-compliant lines
            continue

    return (nodes, sequence)


async def traverse_part1(nodes: dict[str, Node], sequence: list[Movement]) -> int:
    """Traverse the nodes given the sequence, returning the number of steps."""
    current_node = nodes["AAA"]
    return await get_steps(current_node, nodes, sequence)


async def get_steps(n: Node, nodes: dict[str, Node], sequence: list[Movement], ghost: bool = False) -> Node:
    """Returns the number of steps required for a given start point and sequence."""
    steps = 0
    current_node = n
    endswith = "ZZZ"
    if ghost:
        endswith = "Z"

    while True:
        for movement in sequence:
            steps += 1
            if movement == Movement.LEFT:
                current_node = nodes[current_node.left]
            else:
                current_node = nodes[current_node.right]

            if current_node.value.endswith(endswith):
                return steps


def find_lcm(num1, num2):
    """Finds the least common multiple of the two numbers."""
    if num1 > num2:
        num = num1
        den = num2
    else:
        num = num2
        den = num1
    rem = num % den
    while rem != 0:
        num = den
        den = rem
        rem = num % den
    gcd = den
    lcm = int(int(num1 * num2) / int(gcd))
    return lcm


async def traverse_part2(nodes: dict[str, Node], sequence: list[Movement]) -> int:
    """Traverse the nodes using the part 2 spec given the sequence, returning the number of steps."""
    current_nodes = [nodes[n] for n in nodes.keys() if n.endswith("A")]
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(get_steps(n, nodes, sequence, ghost=True)) for n in current_nodes]

    # Instead of brute forcing, if we get the individual steps of
    # each path, the result is the least common multiple of those steps
    z_lengths = [t.result() for t in tasks]
    lcm = z_lengths[0]
    for num in z_lengths[1:]:
        lcm = find_lcm(lcm, num)

    return lcm


async def main():
    """Main entrypoint."""
    parser = argparse.ArgumentParser(prog="day8")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    nodes, sequence = read_file(args.filename)
    part1_steps = await traverse_part1(nodes, sequence)
    print(f"Part 1: {part1_steps}")

    part2_steps = await traverse_part2(nodes, sequence)
    print(f"Part 2: {part2_steps}")


if __name__ == "__main__":
    asyncio.run(main())
