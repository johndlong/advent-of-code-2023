"""Day 15: Lens Library"""

from __future__ import annotations
from argparse import ArgumentParser
from collections import defaultdict, OrderedDict
from dataclasses import dataclass
from enum import Enum
import re
from typing import Optional


class Operation(Enum):
    """Defines the types of operations"""

    REMOVE = "-"
    ADD = "="


@dataclass
class Label:
    """Defines a label"""

    name: str
    number: Optional[int] = 0


@dataclass
class LabelEntry:
    """Defines a label entry"""

    label: Label
    operation: Operation


def read_file(path: str, label: bool = False) -> list[str] | list[Operation]:
    """Returns a data set given the file provided."""
    with open(path, encoding="utf-8") as f:
        data = f.read()

    data = data.replace("\n", "")

    if not label:
        return data.split(",")

    retval = []
    data_re = re.compile(r"(\w+)([-=])(\d+)?")
    for d in data.split(","):
        result = data_re.match(d)
        if not result:
            raise ValueError(f"failed parsing data: {d}")
        label = Label(name=result.group(1))
        if result.group(3):
            label.number = int(result.group(3))
        retval.append(LabelEntry(label=label, operation=Operation(result.group(2))))
    return retval


def calculate_hash(s: str) -> int:
    """Returns the hash value of a given string"""
    retval = 0
    for c in s:
        ascii_val = ord(c)
        retval = ((retval + ascii_val) * 17) % 256
    return retval


def part1(data: list[str]) -> int:
    """Returns the part 1 answer"""
    results = [calculate_hash(d) for d in data]
    return sum(results)


def part2(data: list[LabelEntry]) -> int:
    """Returns the part 2 answer"""
    buckets = defaultdict(OrderedDict)
    for d in data:
        hash_val = calculate_hash(d.label.name)
        bucket = buckets[hash_val]
        if d.operation == Operation.REMOVE:
            if d.label.name in bucket:
                del bucket[d.label.name]
        else:
            bucket[d.label.name] = d.label

    retval = 0
    for i in range(0, 256):
        if i not in buckets or len(buckets[i]) == 0:
            continue
        bucket = buckets[i]
        for j, slot in enumerate(list(bucket.keys()), 1):
            retval += (i + 1) * (j * bucket[slot].number)
    return retval


def main():
    """Main entrypoint."""
    parser = ArgumentParser(prog="day15")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    data = read_file(args.filename)
    p1 = part1(data)
    print(f"Part1: {p1}")

    d2 = read_file(args.filename, label=True)
    p2 = part2(d2)
    print(f"Part2: {p2}")


if __name__ == "__main__":
    main()
