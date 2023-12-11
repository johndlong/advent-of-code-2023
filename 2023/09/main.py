"""Day 9: Mirage Maintenance """
from __future__ import annotations
import argparse
import re


def read_file(path: str) -> list[list[int]]:
    """Returns a list of list of values that are the basis for predictions."""
    with open(path, encoding="utf-8") as f:
        data = f.read()

    lines = data.splitlines()

    sequence = []
    sequence_regex = re.compile(r"([-]?\d+)")

    for line in lines:
        values = []
        for sequence_match in sequence_regex.finditer(line):
            values.append(int(sequence_match.group(0)))
        sequence.append(values)

    return sequence


def part1_prediction(values: list[int]) -> int:
    """Returns the prediction value given the set of values."""
    diffs = []
    if len(values) == 0:
        return 0
    i = values[0]
    for j in values[1:]:
        diffs.append(j - i)
        i = j

    if set(diffs) == set([0]):
        return values[-1:][0]

    return values[-1:][0] + part1_prediction(diffs)


def part2_prediction(values: list[int]) -> int:
    """Returns the left-side prediction value given the set of values."""
    diffs = []
    if len(values) == 0:
        return 0
    i = values[0]
    for j in values[1:]:
        diffs.append(j - i)
        i = j

    if set(diffs) == set([0]):
        return values[0]

    return values[0] - part2_prediction(diffs)


def part1(sequences: list[list[int]]) -> int:
    """Returns the sum of predictions given a sequence of values."""
    total = 0
    for seq in sequences:
        total += part1_prediction(seq)
    return total


def part2(sequences: list[list[int]]) -> int:
    """Returns the sum of predictions given a sequence of values."""
    total = 0
    for seq in sequences:
        total += part2_prediction(seq)
    return total


def main():
    """Main entrypoint."""
    parser = argparse.ArgumentParser(prog="day9")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    sequences = read_file(args.filename)
    p1 = part1(sequences)
    print(f"Part 1: {p1}")

    p2 = part2(sequences)
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
