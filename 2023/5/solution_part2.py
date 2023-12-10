from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


class MapNode:
    def __init__(
        self, name: str, input_start: int, output_start: int, range_len: int
    ) -> None:
        self.name = name
        self.input_start = input_start
        self.output_start = output_start
        self.range_len = range_len
        self.children: list[MapNode] = []

    def add_mapped_range(
        self, input_start: int, mapped_start: int, range_len: int, mapped_name: str
    ):
        self.children.append(
            MapNode(
                name=mapped_name,
                input_start=input_start,
                output_start=mapped_start,
                range_len=range_len,
            )
        )


class Mapper:
    def __init__(self, to: str, ranges: list[tuple[int, int, int]]) -> None:
        self.to = to
        self.ranges = ranges

    def map_input(self, seed_range: tuple[int, int]) -> list[MapResult]:
        range_start, range_length = seed_range
        # range end is inclusive
        range_end = range_start + range_length - 1

        new_ranges: list[MapResult] = []
        for dest_start, map_start, map_len in self.ranges:
            # map end is inclusive
            map_end = map_start + map_len - 1
            # At most we get 3 ranges
            has_before_part = range_start < map_start
            if has_before_part:
                before_start = range_start
                before_len = min(range_length, map_start - before_start)
                new_ranges.append(
                    MapResult(
                        input_range=(before_start, before_len),
                        output_range=(before_start, before_len),
                    )
                )

            has_mapped_part = not (range_end < map_start or range_start > map_end)
            if has_mapped_part:
                to_be_mapped_start = max(range_start, map_start)
                # End is inclusive here, so length is 1 more
                to_be_mapped_end = min(map_start + map_len, range_start + range_length)
                to_be_mapped_len = to_be_mapped_end - to_be_mapped_start + 1
                mapped_start = dest_start + (to_be_mapped_start - map_start)
                mapped_len = to_be_mapped_len
                new_ranges.append(
                    MapResult(
                        input_range=(to_be_mapped_start, to_be_mapped_len),
                        output_range=(mapped_start, mapped_len),
                    )
                )

            has_after_part = range_end > map_end
            if has_after_part:
                after_start = max(range_start, map_end + 1)
                after_end = range_end
                # end inclusive so + 1
                after_len = after_end - after_start + 1
                new_ranges.append(
                    MapResult(
                        input_range=(after_start, after_len),
                        output_range=(after_start, after_len),
                    )
                )

        if new_ranges:
            return new_ranges
        else:
            return [MapResult(input_range=seed_range, output_range=seed_range)]


def recursively_follow_maps_to_location(
    i: tuple[int, int], _from: str, all_mappers: dict[str, Mapper]
) -> int:
    current_mapper = all_mappers[_from]
    result = current_mapper.map_input(i)
    if current_mapper.to == "location":
        return result
    else:
        return recursively_follow_maps_to_location(
            result, current_mapper.to, all_mappers
        )


def get_answer(all_lines: list[str]) -> int:
    # seeds: 79 14 55 13
    seed_line = all_lines[0]
    seeds_part = seed_line.split(": ")[-1]
    seeds = [int(s) for s in seeds_part.split(" ")]

    # They're ranges now
    seed_ranges: list[tuple[int, int]] = []
    s, l = None, None
    for seed in seeds:
        if s is None:
            s = seed
        else:
            l = seed
            seed_ranges.append((s, l))
            s, l = None, None

    map_lines = all_lines[2:]

    # seed-to-soil map:
    # 50 98 2
    # 52 50 48

    _from, _to = None, None
    ranges: list[tuple[int, int, int]] = []

    input_to_mapper_map: dict[str, Mapper] = {}

    for line_index, line in enumerate(map_lines):
        is_last = line_index == len(map_lines) - 1
        if line == "\n" or is_last:
            # end of a map
            if _from is None or _to is None:
                raise ValueError("Expected from and to to be set")
            input_to_mapper_map[_from] = Mapper(to=_to, ranges=ranges)
            # Reset inputs
            _from, _to = None, None
            ranges: list[tuple[int, int, int]] = []
        elif ":" in line:
            # seed-to-soil map:
            _from, _, _to = line.split(" ")[0].split("-")[:3]
        else:
            # 52 50 48
            d, s, l = line.split(" ")
            destination_start = int(d)
            source_start = int(s)
            range_length = int(l)
            ranges.append((destination_start, source_start, range_length))

    seed_to_location: list[tuple[int, int]] = []

    for seed in seeds:
        location = recursively_follow_maps_to_location(
            seed, "seed", input_to_mapper_map
        )
        seed_to_location.append((seed, location))

    sorted_ascending_by_location = sorted(
        seed_to_location, key=lambda t: t[1], reverse=False
    )
    closest_location = sorted_ascending_by_location[0][1]
    return closest_location
