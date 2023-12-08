"""Advent of Code - Day 5."""
from __future__ import annotations
import argparse
from typing import Optional
from dataclasses import dataclass
import re
import sys


@dataclass
class Range:
    """Specifies an object that tracks the overlapping window and before/after windows."""

    within: tuple[int, int]
    before: Optional[tuple[int, int]] = None
    after: Optional[tuple[int, int]] = None


# pylint: disable=too-many-instance-attributes
@dataclass
class Almanac:
    """Tracks the Almanac as read from the data file."""

    seeds: list[tuple(int, int)]
    seed_to_soil: list[tuple[(int, int, int)]]
    soil_to_fertilizer: list[tuple[(int, int, int)]]
    fertilizer_to_water: list[tuple[(int, int, int)]]
    water_to_light: list[tuple[(int, int, int)]]
    light_to_temp: list[tuple[(int, int, int)]]
    temp_to_humidity: list[tuple[(int, int, int)]]
    humidity_to_location: list[tuple[(int, int, int)]]

    @classmethod
    def process_input(cls, path: str, seed_range: bool) -> Almanac:
        """Returns an Almanac object based on the datafile."""
        retval = Almanac(
            seeds=[],
            seed_to_soil=[],
            soil_to_fertilizer=[],
            fertilizer_to_water=[],
            water_to_light=[],
            light_to_temp=[],
            temp_to_humidity=[],
            humidity_to_location=[],
        )
        # pylint: disable=duplicate-code
        with open(path, encoding="utf-8") as f:
            data = f.read()

        lines = data.splitlines()

        seed_str = lines.pop(0)
        seed_matcher = re.finditer(r"\d+", seed_str)
        if seed_range:
            while True:
                try:
                    value = int(next(seed_matcher).group(0))
                    seed_range = int(next(seed_matcher).group(0))

                    retval.seeds.append((value, seed_range))
                except StopIteration:
                    break
        else:
            for match in seed_matcher:
                retval.seeds.append((int(match.group(0)), 1))

        mapping_map = {
            "seed-to-soil": "seed_to_soil",
            "soil-to-fertilizer": "soil_to_fertilizer",
            "fertilizer-to-water": "fertilizer_to_water",
            "water-to-light": "water_to_light",
            "light-to-temperature": "light_to_temp",
            "temperature-to-humidity": "temp_to_humidity",
            "humidity-to-location": "humidity_to_location",
        }

        for key, value in mapping_map.items():
            map_var = getattr(retval, value)  # dict[int:int]
            map_data = _process_map(lines.copy(), key)
            map_var.extend(map_data)

        return retval

    def closest_location(self) -> int:
        """Returns the closest location based on the Almanac values."""
        closest_location = sys.maxsize
        attr_order = [
            "seed_to_soil",
            "soil_to_fertilizer",
            "fertilizer_to_water",
            "water_to_light",
            "light_to_temp",
            "temp_to_humidity",
            "humidity_to_location",
        ]

        for seed_data in self.seeds:
            locations = [seed_data]
            for attr in attr_order:
                mapping = getattr(self, attr)
                locations = get_window_values(mapping, locations)

                for location in locations:
                    if location[1] < 0:
                        pass

            for location in locations:
                closest_location = min(closest_location, location[0])
        return closest_location


def _process_map(lines: str, key: str) -> list[tuple[(int, int, int)]]:
    # Find the desired map
    split_str = f"{key} map:"
    line = None
    while lines:
        line = lines.pop(0)
        if line.startswith(split_str):
            break

    retval = []
    # Now process all the entires until we run into the next map
    for line in lines:
        if data := re.match(r"(\d+)\s+(\d+)\s+(\d+)", line):
            dest = int(data.group(1))
            source = int(data.group(2))
            map_range = int(data.group(3))
            retval.append((source, dest, map_range))
        else:
            break

    return retval


def process_range(source: tuple(int, int), window: tuple(int, int)) -> Optional[Range]:
    """Returns whether there are any ranges that overlap (and any before/afters)."""
    source_start = source[0]
    source_range = source[1]
    source_end = source_start + source_range - 1

    window_start = window[0]
    window_range = window[1]
    window_end = window_start + window_range - 1

    if source_end <= window_start or source_start > window_end:
        return None

    before_range = None
    after_range = None
    if source_start < window_start:
        before_range = (source_start, window_start - source_start)
        within_start = window_start
        if source_end < window_end:
            within_range = source_end - window_start + 1
        else:
            within_range = window_end - window_start + 1
    else:
        within_start = source_start
        if source_end < window_end:
            within_range = source_end - source_start + 1
        else:
            within_range = window_end - source_start + 1

    if window_end < source_end:
        after_range = (window_end + 1, source_end - window_end)

    return Range(within=(within_start, within_range), before=before_range, after=after_range)


def get_window_values(windows: list[tuple(int, int, int)], values: list[tuple(int, int)]) -> list[tuple(int, int)]:
    """Returns a list of tuples with start/range values."""
    retval = []
    for value in values:
        seed_start = value[0]
        seed_range = value[1]

        for window in windows:
            window_start = window[0]
            dest = window[1]
            window_range = window[2]

            processed_range = process_range((seed_start, seed_range), (window_start, window_range))
            if processed_range:
                shift = abs(processed_range.within[0] - window_start)
                retval.append((dest + shift, processed_range.within[1]))
                if processed_range.before:
                    retval.extend(get_window_values(windows, [processed_range.before]))
                if processed_range.after:
                    retval.extend(get_window_values(windows, [processed_range.after]))
                break
        else:
            retval.append((seed_start, seed_range))

    return retval


def main(path: str):
    """Main entrypoint."""
    part1_almanac = Almanac.process_input(path, seed_range=False)
    part1_solution = part1_almanac.closest_location()
    print(f"Part1: {part1_solution}")

    part2_almanac = Almanac.process_input(path, seed_range=True)
    part2_solution = part2_almanac.closest_location()
    print(f"Part2: {part2_solution}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="day5")
    parser.add_argument("-f", "--filename", required=True)
    args = parser.parse_args()
    main(args.filename)
