from __future__ import annotations
from dataclasses import dataclass
from re import M
from typing import Optional


@dataclass
class Range:
    start: int
    len: int

    @property
    def end(self) -> int:
        # inclusive
        return self.start + self.len - 1

    def get_first_number_also_present_in(self, other: Range) -> Optional[int]:
        if self.start > other.end:
            return None
        if other.start > self.end:
            return None
        return max(self.start, other.start)


@dataclass
class MapRange:
    source_start: int
    destination_start: int
    len: int


def get_answer(all_lines: list[str]) -> int:
    # seeds: 79 14 55 13
    seed_line = all_lines[0]
    seeds_part = seed_line.split(": ")[-1]
    seeds = [int(s) for s in seeds_part.split(" ")]

    # They're ranges now
    seed_ranges: list[Range] = []
    s, l = None, None
    for seed in seeds:
        if s is None:
            s = seed
        else:
            l = seed
            seed_ranges.append(Range(s, l))
            s, l = None, None

    map_lines = all_lines[2:]

    # seed-to-soil map:
    # 50 98 2
    # 52 50 48

    _from, _to = None, None
    ranges: list[MapRange] = []

    maps: list[list[MapRange]] = []

    for line_index, line in enumerate(map_lines):
        is_last = line_index == len(map_lines) - 1
        if line == "\n":
            # end of a map
            if _from is None or _to is None:
                raise ValueError("Expected from and to to be set")
            maps.append(ranges)
            # Reset inputs
            _from, _to = None, None
            ranges: list[MapRange] = []
        elif ":" in line:
            # seed-to-soil map:
            _from, _, _to = line.split(" ")[0].split("-")[:3]
        else:
            # 52 50 48
            d, s, l = line.split(" ")
            destination_start = int(d)
            source_start = int(s)
            range_length = int(l)
            ranges.append(
                MapRange(
                    destination_start=destination_start,
                    source_start=source_start,
                    len=range_length,
                )
            )
        if is_last:
            # end of a map
            if _from is None or _to is None:
                raise ValueError("Expected from and to to be set")
            maps.append(ranges)
            # Reset inputs
            _from, _to = None, None
            ranges: list[MapRange] = []

    splitted_seed_ranges_and_current_mapped: list[tuple[Range, Range]] = [(s,s) for s in seed_ranges]
    next_level: list[tuple[Range, Range]] = []
    for m in maps:
        for current_map in m:
            for seed_range, mapped_range in splitted_seed_ranges_and_current_mapped:
                has_before_part = mapped_range.start < current_map.destination_start
                if has_before_part:
                    