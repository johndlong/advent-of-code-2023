"""Day 12: Hot Springs"""

from __future__ import annotations
import argparse
import copy
from dataclasses import dataclass
from enum import Enum
import re

from bitmap import BitMap


class State(Enum):
    """Defines the Spring states"""

    OPERATIONAL = "."
    DAMAGED = "#"
    UNKNOWN = "?"


@dataclass
class Spring:
    """Defines a spring"""

    entries: list[State]
    records: list[int]
    final: bool = False


def read_file(path: str) -> list[Spring]:
    """Returns a set of springs given the file provided."""
    with open(path, encoding="utf-8") as f:
        data = f.read()

    springs = []

    entries_re = re.compile(r"([\.\#\?])")
    records_re = re.compile(r"(\d+)")
    lines = data.splitlines()
    for row in lines:
        spring = Spring(entries=[], records=[])
        for match in re.finditer(entries_re, row):
            spring.entries.append(State(match.group(1)))
        for match in re.finditer(records_re, row):
            spring.records.append(int(match.group(1)))
        springs.append(spring)

    return springs


def different_arrangements(spring: Spring) -> int:
    """Return all the different possible arrangement for a given spring"""
    retval = 0

    total_unknown = len([x for x in spring.entries if x == State.UNKNOWN])
    replicas = []
    for _ in range(2**total_unknown):
        replica = Spring(entries=copy.copy(spring.entries), records=spring.records)
        replicas.append(replica)

    for j, replica in enumerate(replicas):
        bm = BitMap.fromstring(format(j, "#0100b").lstrip("0b"))
        unknown_count = 0
        for k, entry in enumerate(replica.entries):
            if entry == State.UNKNOWN:
                try:
                    if bm.test(unknown_count):
                        replica.entries[k] = State.DAMAGED
                    else:
                        replica.entries[k] = State.OPERATIONAL
                except IndexError:
                    replica.entries[k] = State.OPERATIONAL
                unknown_count += 1
    for replica in replicas:
        if is_valid(replica.entries, spring.records):
            retval += 1

    return retval


def is_valid(states: list[State], records: list[int]) -> bool:
    """Determines if a provided spring is valid."""
    contiguous_damaged = []
    total = len(states)
    i = 0
    while True:
        if i >= total:
            break
        if states[i] == State.DAMAGED:
            count = 1
            while True:
                if i + count >= total or states[i + count] != State.DAMAGED:
                    contiguous_damaged.append(count)
                    i = i + count
                    break
                count += 1
        else:
            i += 1

    if contiguous_damaged == records:
        return True
    return False


def part1(springs: list[Spring]) -> int:
    """Returns the part 1 answer"""
    return sum(different_arrangements(spring) for spring in springs)


def main():
    """Main entrypoint."""
    parser = argparse.ArgumentParser(prog="day12")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    springs = read_file(args.filename)
    p1 = part1(springs)
    print(f"Part1: {p1}")


if __name__ == "__main__":
    main()
