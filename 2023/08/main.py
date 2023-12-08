""" Day 8: Haunted Wasteland """
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import argparse
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


def traverse_part1(nodes: dict[str, Node], sequence: list[Movement]) -> int:
    """Traverse the nodes given the sequence, returning the number of steps."""
    current_node = nodes["AAA"]
    steps = 0
    while True:
        for movement in sequence:
            steps += 1
            if movement == Movement.LEFT:
                current_node = nodes[current_node.left]
            else:
                current_node = nodes[current_node.right]
        if current_node.value == "ZZZ":
            return steps


def main():
    """Main entrypoint."""
    parser = argparse.ArgumentParser(prog="day8")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    nodes, sequence = read_file(args.filename)
    steps = traverse_part1(nodes, sequence)
    print(f"Part 1: {steps}")


if __name__ == "__main__":
    main()
