spelled_digits_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def get_first_number_in_line(line: str) -> int:
    for end_index in range(1, len(line) + 1):
        line_slice = line[:end_index]
        last_char = line_slice[-1]
        try:
            return int(last_char)
        except:
            for spelled_digit in spelled_digits_map:
                if spelled_digit in line_slice:
                    return spelled_digits_map[spelled_digit]
    raise ValueError(f"No number found in line {line}")


def get_last_number_in_line(line: str) -> int:
    for start_index in range(0, len(line))[::-1]:
        line_slice = line[start_index:]
        first_char = line_slice[0]
        try:
            return int(first_char)
        except:
            for spelled_digit in spelled_digits_map:
                if spelled_digit in line_slice:
                    return spelled_digits_map[spelled_digit]
    raise ValueError(f"No number found in line {line}")


def get_answer(all_lines: list[str]) -> int:
    total_sum = 0
    for line in all_lines:
        first_number = get_first_number_in_line(line)
        last_number = get_last_number_in_line(line)
        combined_digits = str(first_number) + str(last_number)
        total_sum += int(combined_digits)
    return total_sum
