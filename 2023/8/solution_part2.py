from enum import Enum


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


def get_answer(all_lines: list[str]) -> int:
    instructions = parse_instructions(all_lines[0])
    max_instruction_index = len(instructions) - 1

    mapping: dict[str, dict[Instruction, str]] = {}

    for map_line in all_lines[2:]:
        _in, left, right = parse_map(map_line)
        mapping[_in] = {Instruction.left: left, Instruction.right: right}

    steps = 0
    instruction_index = 0
    locations = [k for k in mapping if k[-1] == "A"]
    while True:
        steps += 1
        instruction = instructions[instruction_index]
        if instruction_index == max_instruction_index:
            instruction_index = 0
        else:
            instruction_index += 1
        locations = [mapping[l][instruction] for l in locations]
        if all([l[-1] == "Z" for l in locations]):
            break

    return steps
