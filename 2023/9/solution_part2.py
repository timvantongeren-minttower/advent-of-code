def get_sequence_from_line(line: str) -> list[int]:
    return [int(i) for i in line.replace("\n", "").split()]


assert get_sequence_from_line("1 12 59 -99\n") == [1, 12, 59, -99]


def get_first_differences_of_sequence(sequence: list[int]) -> list[int]:
    return [last - first for first, last in zip(sequence[:-1], sequence[1:])]


assert get_first_differences_of_sequence([1, 2, 3, 4]) == [1, 1, 1]
assert get_first_differences_of_sequence([1, -1]) == [-2]


def has_zero_derivative(sequence: list[int]) -> bool:
    return all([s == 0 for s in sequence])


assert has_zero_derivative([0, 0]) == True
assert has_zero_derivative([1, 0]) == False


def get_next_number_in_sequence(sequence: list[int]) -> int:
    derivative_list: list[list[int]] = [sequence]
    while not has_zero_derivative(derivative_list[-1]):
        derivative_list.append(get_first_differences_of_sequence(derivative_list[-1]))

    if len(derivative_list) == 1:
        # original sequence already had 0 diffs
        return sequence[-1]

    for derivative_index in reversed(range(1, len(derivative_list))):
        this_derivative = derivative_list[derivative_index][-1]
        derivative_to_add_to = derivative_list[derivative_index - 1]
        number_to_add_to = derivative_to_add_to[-1]
        next_number = number_to_add_to + this_derivative
        derivative_to_add_to.append(next_number)

    return derivative_list[0][-1]


assert get_next_number_in_sequence([0, 3, 6]) == 9
assert get_next_number_in_sequence([1, 1]) == 1


def get_answer(all_lines: list[str]) -> int:
    next_number_sum = 0
    for line in all_lines:
        sequence = get_sequence_from_line(line)
        # Reverse the input
        sequence = list(reversed(sequence))
        next_number = get_next_number_in_sequence(sequence)
        next_number_sum += next_number
    return next_number_sum
