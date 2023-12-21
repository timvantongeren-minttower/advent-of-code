from dataclasses import dataclass, field
from enum import Enum, auto
from math import ceil
from typing import Literal


class Direction(Enum):
    north = auto()
    east = auto()
    south = auto()
    west = auto()


def get_inverse_direction(direction: Direction) -> Direction:
    match direction:
        case Direction.north:
            return Direction.south
        case Direction.east:
            return Direction.west
        case Direction.south:
            return Direction.north
        case Direction.west:
            return Direction.east


@dataclass
class Pipe:
    connection1: Direction
    connection2: Direction

    def is_connected(self, direction: Direction) -> bool:
        return direction == self.connection1 or direction == self.connection2

    def way_out(self, way_in: Direction) -> Direction:
        if way_in == self.connection1:
            return self.connection2
        if way_in == self.connection2:
            return self.connection1
        raise ValueError(
            f"Pipe ({self.connection1}, {self.connection2}) isn't connected to {way_in}"
        )


@dataclass
class LocationTracker:
    map: list[list[Pipe | None | Literal["S"]]]
    current_point: tuple[int, int] = field(default=None)  # type: ignore

    def initialize_in_starting_point(self):
        for i in range(len(self.map)):
            this_row = self.map[i]
            for j in range(len(this_row)):
                element = this_row[j]
                if element == "S":
                    self.current_point = (i, j)
                    return

    def is_valid_point(self, point: tuple[int, int]) -> bool:
        try:
            self.map[point[0]][point[1]]
            return True
        except KeyError:
            return False

    def step_to(self, direction: Direction) -> Pipe | None | Literal["S"]:
        current_i, current_j = self.current_point
        match direction:
            case Direction.north:
                next_point = (current_i - 1, current_j)
            case Direction.east:
                next_point = (current_i, current_j + 1)
            case Direction.south:
                next_point = (current_i + 1, current_j)
            case Direction.west:
                next_point = (current_i, current_j - 1)
        if not self.is_valid_point(next_point):
            raise ValueError("You jumped of the map you fool")
        self.current_point = next_point
        point_we_land_on = self.map[self.current_point[0]][self.current_point[1]]
        return point_we_land_on

    def find_connected_directions(self) -> list[Direction]:
        connections: list[Direction] = []
        for d in Direction:
            back_d = get_inverse_direction(d)
            landing_spot = self.step_to(d)
            if isinstance(landing_spot, Pipe) and landing_spot.is_connected(back_d):
                connections.append(d)
            self.step_to(back_d)
        return connections


def parse_char(char: str) -> Pipe | None | Literal["S"]:
    match char:
        case "S":
            return "S"
        case ".":
            return None
        case "|":
            return Pipe(Direction.north, Direction.south)
        case "L":
            return Pipe(Direction.north, Direction.east)
        case "J":
            return Pipe(Direction.north, Direction.west)
        case "F":
            return Pipe(Direction.south, Direction.east)
        case "7":
            return Pipe(Direction.south, Direction.west)
        case "-":
            return Pipe(Direction.east, Direction.west)


def parse_map_line(line: str) -> list[Pipe | None | Literal["S"]]:
    parsed_line: list[Pipe | None | Literal["S"]] = []
    for char in line:
        parsed_line.append(parse_char(char))
    return parsed_line


def parse_map(lines: list[str]) -> list[list[Pipe | None | Literal["S"]]]:
    return [parse_map_line(line.replace("\n", "")) for line in lines]


assert parse_map(["FS7\n", "LJ.\n"]) == [
    [Pipe(Direction.south, Direction.east), "S", Pipe(Direction.south, Direction.west)],
    [
        Pipe(Direction.north, Direction.east),
        Pipe(Direction.north, Direction.west),
        None,
    ],
]


class LoopState(Enum):
    outside = auto()
    inside = auto()
    require_south_to_open = auto()
    require_north_to_open = auto()
    require_south_to_close = auto()
    require_north_to_close = auto()


def get_answer(all_lines: list[str]) -> int:
    parsed_map = parse_map(all_lines)

    location_tracker = LocationTracker(parsed_map)
    location_tracker.initialize_in_starting_point()

    directions_connected_to_starting_point = (
        location_tracker.find_connected_directions()
    )
    # puzzle assumption
    assert len(directions_connected_to_starting_point) == 2

    # we just pick a way around
    direction_to_go = directions_connected_to_starting_point[0]
    coordinates_of_all_loop_parts: set[tuple[int, int]] = set()
    while True:
        landing_spot = location_tracker.step_to(direction_to_go)
        coordinates_of_all_loop_parts.add(location_tracker.current_point)
        if landing_spot == "S":
            break
        if not isinstance(landing_spot, Pipe):
            raise ValueError("Puzzle assumption violation, didn't jump on pipe")
        came_in_from = get_inverse_direction(direction_to_go)
        direction_to_go = landing_spot.way_out(came_in_from)

    # Replace S with a pipe as we need to treat it like one below
    location_tracker.initialize_in_starting_point()
    i, j = location_tracker.current_point
    parsed_map[i][j] = Pipe(*directions_connected_to_starting_point)

    inside_squares = 0
    for line_index in range(len(parsed_map)):
        loop_state = LoopState.outside
        map_line = parsed_map[line_index]
        for location_index in range(len(map_line)):
            this_square = parsed_map[line_index][location_index]
            this_coord = (line_index, location_index)
            this_is_part_of_loop = this_coord in coordinates_of_all_loop_parts
            match loop_state:
                case LoopState.outside:
                    if not this_is_part_of_loop:
                        continue
                    else:
                        if this_square.is_connected(
                            Direction.north
                        ) and this_square.is_connected(Direction.south):
                            loop_state = LoopState.inside
                        elif this_square.is_connected(
                            Direction.north
                        ) and this_square.is_connected(Direction.east):
                            loop_state = LoopState.require_south_to_open
                        elif this_square.is_connected(
                            Direction.south
                        ) and this_square.is_connected(Direction.east):
                            loop_state = LoopState.require_north_to_open

                case LoopState.inside:
                    if not this_is_part_of_loop:
                        inside_squares += 1
                    else:
                        if this_square.is_connected(
                            Direction.north
                        ) and this_square.is_connected(Direction.south):
                            loop_state = LoopState.outside
                        elif this_square.is_connected(
                            Direction.north
                        ) and this_square.is_connected(Direction.east):
                            loop_state = LoopState.require_south_to_close
                        elif this_square.is_connected(
                            Direction.south
                        ) and this_square.is_connected(Direction.east):
                            loop_state = LoopState.require_north_to_close

                case LoopState.require_north_to_close:
                    if this_is_part_of_loop and this_square.is_connected(
                        Direction.north
                    ):
                        loop_state = LoopState.outside
                    elif this_is_part_of_loop and this_square.is_connected(
                        Direction.south
                    ):
                        loop_state = LoopState.inside

                case LoopState.require_south_to_close:
                    if this_is_part_of_loop and this_square.is_connected(
                        Direction.south
                    ):
                        loop_state = LoopState.outside
                    elif this_is_part_of_loop and this_square.is_connected(
                        Direction.north
                    ):
                        loop_state = LoopState.inside

                case LoopState.require_north_to_open:
                    if this_is_part_of_loop and this_square.is_connected(
                        Direction.north
                    ):
                        loop_state = LoopState.inside
                    elif this_is_part_of_loop and this_square.is_connected(
                        Direction.south
                    ):
                        loop_state = LoopState.outside

                case LoopState.require_south_to_open:
                    if this_is_part_of_loop and this_square.is_connected(
                        Direction.south
                    ):
                        loop_state = LoopState.inside
                    elif this_is_part_of_loop and this_square.is_connected(
                        Direction.north
                    ):
                        loop_state = LoopState.outside

    return inside_squares
