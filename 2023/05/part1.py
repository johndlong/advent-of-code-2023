from __future__ import annotations
from dataclasses import dataclass
import logging
import re
import sys


@dataclass
class Almanac:
    seeds: list[int]
    seed_to_soil: list[tuple[(int, int, int)]]
    soil_to_fertilizer: list[tuple[(int, int, int)]]
    fertilizer_to_water: list[tuple[(int, int, int)]]
    water_to_light: list[tuple[(int, int, int)]]
    light_to_temp: list[tuple[(int, int, int)]]
    temp_to_humidity: list[tuple[(int, int, int)]]
    humidity_to_location: list[tuple[(int, int, int)]]

    @classmethod
    def process_input(cls, path: str) -> Almanac:
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
        with open(path) as f:
            data = f.read()

        lines = data.splitlines()

        seed_str = lines.pop(0)
        seed_matcher = re.finditer(r"\d+", seed_str)
        for match in seed_matcher:
            retval.seeds.append(int(match.group(0)))

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
        for seed in self.seeds:
            location = seed
            for attr in attr_order:
                mapping = getattr(self, attr)
                location = get_map_value(mapping, location)

            logging.debug(f"Seed {seed}: Location: {location}")
            closest_location = min(closest_location, location)
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


def get_map_value(map: list[tuple(int, int, int)], value: int) -> int:
    for window in map:
        source = window[0]
        dest = window[1]
        range = window[2]
        if value >= source and value <= source + range:
            return dest + (value - source)
    return value


def main(path: str):
    almanac = Almanac.process_input(path)
    solution = almanac.closest_location()
    print(solution)


if __name__ == "__main__":
    main("2023/05/part1.txt")
