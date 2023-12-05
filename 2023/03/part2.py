# pylint: skip-file
import re


def gear_ratios(current_line: str, above_line: str, below_line: str) -> list[int]:
    retval = []
    if matches := re.finditer(r"\*", current_line):
        for match in matches:
            start = match.start()
            end = match.end()

            if start - 1 < 0:
                start = 0
            else:
                start = start - 1

            if end + 1 > len(current_line) + 1:
                end = len(current_line) + 1
            else:
                end = end + 1

            gears = []
            for line in [current_line, above_line, below_line]:
                if num_matches := re.finditer(r"\d+", line):
                    for num_match in num_matches:
                        num_positions = range(num_match.start(), num_match.end())
                        for pos in num_positions:
                            if pos in range(start, end):
                                gears.append(int(num_match.group(0)))
                                break
            if len(gears) > 1:
                ratio = 1
                for gear in gears:
                    ratio = ratio * gear
                retval.append(ratio)

    return retval


def main():
    above = ""
    current = ""
    below = None

    total = 0
    with open("03/part2.txt", encoding="utf-8") as f:
        data = f.read()

    lines = data.splitlines()

    while True:
        if below is None:
            current = lines.pop(0)

        if len(lines) > 0:
            below = lines.pop(0)

        if current == "":
            break

        ratios = gear_ratios(current, above, below)
        for part in ratios:
            total += part

        above = current
        current = below

        if len(lines) == 0:
            below = ""

    print(f"Total: {total}")


if __name__ == "__main__":
    main()
