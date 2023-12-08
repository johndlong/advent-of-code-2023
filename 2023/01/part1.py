"""Advent of Code - Day 1 - Part 1"""
import argparse
import re


def get_value(line: str) -> int:
    """Return the value extracted from the line."""
    if result := re.match(r"^.*?(\d).*(\d)", line):
        groups = result.groups()
        assert len(groups) == 2
        first_num = groups[0]
        last_num = groups[1]
        return int(f"{first_num}{last_num}")
    match = re.match(r"^.*(\d+)", line)
    assert match is not None
    groups = match.groups()
    first_num = groups[0]
    return int(f"{first_num}{first_num}")


def get_sum(data: str) -> int:
    """Return the sum of all the values extracted from the lines."""
    total = 0
    for line in data.splitlines():
        total += get_value(line)
    return total


def main():
    """Main entrypoint."""
    # pylint: disable=duplicate-code
    parser = argparse.ArgumentParser(prog="day1_part1")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    with open(args.filename, encoding="utf-8") as f:
        data = f.read()
    retval = get_sum(data)
    print(retval)


if __name__ == "__main__":
    main()
