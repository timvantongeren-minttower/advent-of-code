def get_first_number_in_line(line: str) -> int:
    for char in line:
        try:
            return int(char)
        except:
            continue
    raise ValueError(f"No number found in line {line}")


def get_answer(all_lines: list[str]) -> int:
    total_sum = 0
    for line in all_lines:
        first_number = get_first_number_in_line(line)
        last_number = get_first_number_in_line(line[::-1])
        combined_digits = str(first_number) + str(last_number)
        total_sum += int(combined_digits)
    return total_sum
