from dataclasses import dataclass


def is_number(char: str) -> bool:
    return char in [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    ]


def is_symbol(char: str) -> bool:
    return not (is_number(char) or char == ".")


@dataclass
class Coordinate:
    line_index: int
    char_index: int


def main(test: bool = True):
    filename = "test_input.txt" if test else "real_input.txt"
    with open(filename, "r") as f:
        all_lines = f.readlines()

    char_coords: list[Coordinate] = []

    for line_index in range(len(all_lines)):
        this_line = all_lines[line_index]
        for char_index in range(len(this_line)):
            this_char = this_line[char_index]
            if is_symbol(this_char):
                char_coords.append(Coordinate(line_index, char_index))

    print(char_coords)


if __name__ == "__main__":
    main()
