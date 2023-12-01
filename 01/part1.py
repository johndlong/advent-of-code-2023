import re


def get_value(line: str) -> int:
    if result := re.match(r"^.*?(\d).*(\d)", line):
        groups = result.groups()
        assert len(groups) == 2
        first_num = groups[0]
        last_num = groups[1]
        return int(f"{first_num}{last_num}")
    else:
        match = re.match(r"^.*(\d+)", line)
        assert match is not None
        groups = match.groups()
        first_num = groups[0]
        return int(f"{first_num}{first_num}")


def get_sum(data: str) -> int:
    total = 0
    for line in data.splitlines():
        total += get_value(line)
    return total


def main():
    with open("01/part1.txt") as f:
        data = f.read()
    sum = get_sum(data)
    print(sum)


if __name__ == "__main__":
    main()
