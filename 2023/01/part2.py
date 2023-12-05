"""Advent of Code - Day 1 - Part 2"""

import math

name_to_value = {
    1: 1,
    "one": 1,
    2: 2,
    "two": 2,
    3: 3,
    "three": 3,
    4: 4,
    "four": 4,
    5: 5,
    "five": 5,
    6: 6,
    "six": 6,
    7: 7,
    "seven": 7,
    8: 8,
    "eight": 8,
    9: 9,
    "nine": 9,
}


def get_value(line: str) -> int:
    """Return the value extracted from the line."""
    name_to_index = dict.fromkeys(name_to_value.keys(), ())
    for name in name_to_value:
        fname = name
        if isinstance(name, int):
            fname = f"{name}"
        first = line.find(fname)
        last = line.rfind(fname)
        name_to_index[name] = (first, last)

    first_name = None
    lowest = math.inf
    last_name = None
    highest = -math.inf
    for name, data in name_to_index.items():
        if data[0] >= 0 and data[0] < lowest:
            first_name = name
            lowest = data[0]
        if data[1] >= 0 and data[1] > highest:
            last_name = name
            highest = data[1]

    first_num = name_to_value[first_name]
    last_num = name_to_value[last_name]
    return int(f"{first_num}{last_num}")


def get_sum(data: str) -> int:
    """Return the sum of all the values extracted from the lines."""
    # pylint: disable=duplicate-code
    total = 0
    for line in data.splitlines():
        total += get_value(line)
    return total


def main():
    """Main entrypoint."""
    # pylint: disable=duplicate-code
    with open("01/part2.txt", encoding="utf-8") as f:
        data = f.read()

    retval = get_sum(data)
    print(retval)


if __name__ == "__main__":
    main()
