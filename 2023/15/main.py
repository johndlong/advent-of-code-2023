"""Day 15: Lens Library"""

from __future__ import annotations
from argparse import ArgumentParser


def read_file(path: str) -> list[str]:
    """Returns a data set given the file provided."""
    with open(path, encoding="utf-8") as f:
        data = f.read()

    data = data.replace("\n", "")
    return data.split(",")


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


def main():
    """Main entrypoint."""
    parser = ArgumentParser(prog="day15")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    data = read_file(args.filename)
    p1 = part1(data)
    print(f"Part1: {p1}")


if __name__ == "__main__":
    main()
