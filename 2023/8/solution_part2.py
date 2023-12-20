from dataclasses import dataclass
from enum import Enum
from itertools import combinations, permutations, product


class Instruction(str, Enum):
    left = "L"
    right = "R"


def parse_instructions(line: str) -> list[Instruction]:
    return [Instruction(char) for char in line if char != "\n"]


assert parse_instructions("LR\n") == [Instruction.left, Instruction.right]


def parse_map(line: str) -> tuple[str, str, str]:
    _in, out_part = line.split(" = ")
    left, right = out_part.replace("(", "").replace(")\n", "").split(", ")
    return (_in, left, right)


assert parse_map("FCG = (PLG, GXC)\n") == ("FCG", "PLG", "GXC")


class PathStepper:
    def __init__(
        self,
        starting_location: str,
        instructions: list[Instruction],
        mapping: dict[str, dict[Instruction, str]],
        instruction_starting_index: int = 0,
    ) -> None:
        self.steps = 0
        self.instruction_index = instruction_starting_index
        self.location = starting_location
        self.instructions = instructions
        self.mapping = mapping
        self.max_instruction_index = len(instructions) - 1

    def do_step(self) -> bool:
        # Returns True if spot it lands on ends with Z
        self.steps += 1
        instruction = self.instructions[self.instruction_index]
        if self.instruction_index == self.max_instruction_index:
            self.instruction_index = 0
        else:
            self.instruction_index += 1
        self.location = self.mapping[self.location][instruction]
        if self.location[-1] == "Z":
            return True
        return False


def find_loop_start_and_instruction_index(
    stepper: PathStepper, max_iter: int = 10_000_000
) -> tuple[str, int]:
    combinations_seen: set[tuple[str, int]] = set()
    for _ in range(max_iter):
        location = stepper.location
        instruction_index = stepper.instruction_index
        combi = (location, instruction_index)
        if combi in combinations_seen:
            return combi
        combinations_seen.add(combi)
        stepper.do_step()
    raise ValueError(
        f"No loop could be found for stepper {stepper} after {max_iter} iterations"
    )


def find_loop_length(
    starting_location: str,
    instruction_index: int,
    instructions: list[Instruction],
    mapping: dict[str, dict[Instruction, str]],
    max_iter: int = 100_000_000,
) -> int:
    stepper = PathStepper(
        starting_location=starting_location,
        instructions=instructions,
        mapping=mapping,
        instruction_starting_index=instruction_index,
    )
    for _ in range(max_iter):
        stepper.do_step()
        if (
            stepper.location == starting_location
            and stepper.instruction_index == instruction_index
        ):
            return stepper.steps
    raise ValueError(
        f"No loop could be found for stepper {stepper} after {max_iter} iterations"
    )


def find_z_indices_in_loop(
    starting_location: str,
    instruction_index: int,
    instructions: list[Instruction],
    mapping: dict[str, dict[Instruction, str]],
    max_iter: int = 100_000_000,
) -> list[int]:
    stepper = PathStepper(
        starting_location=starting_location,
        instructions=instructions,
        mapping=mapping,
        instruction_starting_index=instruction_index,
    )
    z_indices: list[int] = []
    for _ in range(max_iter):
        if stepper.location[-1] == "Z":
            z_indices.append(stepper.steps)
        stepper.do_step()
        if (
            stepper.location == starting_location
            and stepper.instruction_index == instruction_index
        ):
            return z_indices
    raise ValueError(
        f"No loop could be found for stepper {stepper} after {max_iter} iterations"
    )


def get_answer(all_lines: list[str]) -> int:
    instructions = parse_instructions(all_lines[0])

    mapping: dict[str, dict[Instruction, str]] = {}

    for map_line in all_lines[2:]:
        _in, left, right = parse_map(map_line)
        mapping[_in] = {Instruction.left: left, Instruction.right: right}

    starting_locations = list(set([k for k in mapping if k[-1] == "A"]))

    params: list[tuple[int, int, list[int]]] = []
    for starting_location in starting_locations:
        stepper = PathStepper(
            starting_location=starting_location,
            instructions=instructions,
            mapping=mapping,
        )
        loop_start, loop_instruction_index = find_loop_start_and_instruction_index(
            stepper
        )

        stepper = PathStepper(
            starting_location=starting_location,
            instructions=instructions,
            mapping=mapping,
        )
        while (stepper.location, stepper.instruction_index) != (
            loop_start,
            loop_instruction_index,
        ):
            stepper.do_step()
        length_before_loop = stepper.steps

        loop_length = find_loop_length(
            loop_start, loop_instruction_index, instructions, mapping
        )
        z_indices = find_z_indices_in_loop(
            loop_start, loop_instruction_index, instructions, mapping
        )

        params.append((length_before_loop, loop_length, z_indices))

    for a, b in combinations(params, 2):
        combination_ns: set[int] = []
        for z_a, z_b in product(a[2], b[2]):
            valid_n = ((b[0] + z_b) - (a[0] + z_a)) / (a[1] - b[1])
