class Mapper:
    def __init__(self, to: str, ranges: list[tuple[int, int, int]]) -> None:
        self.to = to
        self.ranges = ranges

    def map_input(self, i: int) -> int:
        for d, s, l in self.ranges:
            if i >= s and i < s + l:
                return d + (i - s)
        return i


def recursively_follow_maps_to_location(
    i: int, _from: str, all_mappers: dict[str, Mapper]
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
