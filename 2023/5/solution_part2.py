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


class Mapper:
    def __init__(self, _from: str, ranges: list[MapRange]) -> None:
        self._from = _from
        self.ranges = ranges

    def get_input_ranges_of_output_range(
        self, output_range: Range, sort_ranges_by_asc_output: bool
    ) -> list[Range]:
        input_ranges_and_smallest_output: list[tuple[Range, int]] = []
        for map_range in self.ranges:
            map_range_destination_end = map_range.destination_start + map_range.len - 1

            has_before_part = output_range.start < map_range.destination_start
            if has_before_part:
                input_range = Range(
                    output_range.start,
                    min(
                        map_range.destination_start - output_range.start,
                        output_range.len,
                    ),
                )
                smallest_output = output_range.start
                input_ranges_and_smallest_output.append((input_range, smallest_output))

            has_mapped_part = not (
                output_range.end < map_range.destination_start
                or output_range.start > map_range_destination_end
            )
            if has_mapped_part:
                map_diff = map_range.source_start - map_range.destination_start
                valid_output_start = max(
                    output_range.start, map_range.destination_start
                )
                mapped_input_start = valid_output_start + map_diff
                valid_output_end = min(output_range.end, map_range_destination_end)
                valid_output_len = valid_output_end - valid_output_start + 1
                input_range = Range(mapped_input_start, valid_output_len)
                smallest_output = valid_output_start
                input_ranges_and_smallest_output.append((input_range, smallest_output))

            has_after_part = output_range.end > map_range_destination_end
            if has_after_part:
                input_range = Range(
                    map_range_destination_end,
                    min(
                        output_range.end - map_range_destination_end,
                        output_range.len,
                    ),
                )
                smallest_output = output_range.start
                input_ranges_and_smallest_output.append((input_range, smallest_output))

        if sort_ranges_by_asc_output:
            input_ranges_and_smallest_output = sorted(
                input_ranges_and_smallest_output, key=lambda t: t[1]
            )
        return [t[0] for t in input_ranges_and_smallest_output]

    def map_input(self, i: int) -> int:
        for map_range in self.ranges:
            if (
                i >= map_range.source_start
                and i < map_range.source_start + map_range.len
            ):
                return map_range.destination_start + (i - map_range.source_start)
        return i


def recursively_follow_maps_to_location(
    i: int, to: str, all_mappers: dict[str, Mapper]
) -> int:
    current_mapper = all_mappers[to]
    result = current_mapper.map_input(i)
    if to == "location":
        return result
    else:
        return recursively_follow_maps_to_location(
            result, current_mapper._from, all_mappers
        )


def recursively_follow_maps_to_seed_ranges(
    output_range: Range, to: str, all_mappers: dict[str, Mapper]
) -> list[Range]:
    current_mapper = all_mappers[to]
    result = current_mapper.get_input_ranges_of_output_range(
        output_range=output_range, sort_ranges_by_asc_output=True
    )
    if current_mapper._from == "seed":
        return result
    else:
        sorted_ranges: list[Range] = []
        for input_with_most_potential in result:
            sorted_ranges.extend(
                recursively_follow_maps_to_seed_ranges(
                    input_with_most_potential, current_mapper._from, all_mappers
                )
            )
        return sorted_ranges


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

    output_to_mapper_map: dict[str, Mapper] = {}

    for line_index, line in enumerate(map_lines):
        is_last = line_index == len(map_lines) - 1
        if line == "\n":
            # end of a map
            if _from is None or _to is None:
                raise ValueError("Expected from and to to be set")
            output_to_mapper_map[_to] = Mapper(_from=_from, ranges=ranges)
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
            output_to_mapper_map[_to] = Mapper(_from=_from, ranges=ranges)
            # Reset inputs
            _from, _to = None, None
            ranges: list[MapRange] = []

    location_mapper = output_to_mapper_map["location"]
    sorted_location_ranges = sorted(
        location_mapper.ranges, key=lambda t: t.destination_start
    )
    sorted_location_ranges = [
        Range(location_range.destination_start, location_range.len)
        for location_range in sorted_location_ranges
    ]
    non_mapped_location_ranges: list[Range] = []
    current_start = 1
    for mapped_location in sorted_location_ranges:
        non_mapped_location_ranges.append(
            Range(current_start, mapped_location.start - current_start)
        )
        current_start = mapped_location.end + 1
    all_locations = sorted(
        sorted_location_ranges + non_mapped_location_ranges, key=lambda t: t.start
    )

    print(all_locations)

    best_seed = None
    for location_range in all_locations:
        to = "location"
        resulting_seed_ranges = recursively_follow_maps_to_seed_ranges(
            output_range=location_range, to=to, all_mappers=output_to_mapper_map
        )
        for res in resulting_seed_ranges:
            for seed_range in seed_ranges:
                first_match = res.get_first_number_also_present_in(other=seed_range)
                if first_match is not None:
                    best_seed = first_match
                    break
            if best_seed is not None:
                break
        if best_seed is not None:
            break

    return recursively_follow_maps_to_location(
        best_seed, to="location", all_mappers=output_to_mapper_map
    )
