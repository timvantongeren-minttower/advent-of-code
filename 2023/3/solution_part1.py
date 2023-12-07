def is_number(char: str) -> bool:
    return char in [
        "0",
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


def is_end_of_line(char: str) -> bool:
    return char == "\n"


def is_symbol(char: str) -> bool:
    return not (is_number(char) or char == "." or is_end_of_line(char))


def main(test: bool = False):
    filename = "test_input.txt" if test else "real_input.txt"
    with open(filename, "r") as f:
        all_lines = f.readlines()

    total_sum = 0

    number_of_lines = len(all_lines)
    for line_index in range(number_of_lines):
        this_line = all_lines[line_index]
        number_of_chars = len(this_line)
        current_number = ""
        for char_index in range(number_of_chars):
            this_char = this_line[char_index]
            if is_number(this_char):
                current_number += this_char
            elif len(current_number) > 0:
                # for the search, so one extra on both sides
                start_char_index = max(char_index - len(current_number) - 1, 0)
                end_char_index = min(char_index, number_of_chars - 1)
                start_line_index = max(line_index - 1, 0)
                end_line_index = min(line_index + 1, number_of_lines - 1)

                include = False
                for search_line_index in range(start_line_index, end_line_index + 1):
                    search_line = all_lines[search_line_index]
                    for search_char_index in range(start_char_index, end_char_index + 1):
                        search_char = search_line[search_char_index]
                        if is_symbol(search_char):
                            include = True

                if include:
                    total_sum += int(current_number)
                current_number = ""

    print(total_sum)
    if test:
        assert total_sum == 4361


if __name__ == "__main__":
    main()
