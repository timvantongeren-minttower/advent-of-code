def get_values_from_line(line: str) -> list[int]:
    data = line.split(":")[-1]
    return [int(t) for t in data.split()]


assert get_values_from_line("Time:      7  15   30") == [7, 15, 30]


def get_number_of_possible_wins(time: int, distance: int) -> int:
    wins = 0
    for seconds_to_hold_button in range(1, time):
        speed = seconds_to_hold_button
        time_to_travel = time - seconds_to_hold_button
        distance_travelled = speed * time_to_travel
        if distance_travelled > distance:
            wins += 1
    return wins


assert get_number_of_possible_wins(7, 9) == 4


def get_answer(all_lines: list[str]) -> int:
    # Time:      7  15   30
    # Distance:  9  40  200
    times = get_values_from_line(all_lines[0])
    distances = get_values_from_line(all_lines[1])

    total_product = 1
    for time, distance in zip(times, distances):
        possible_wins = get_number_of_possible_wins(time, distance)
        total_product *= possible_wins

    return total_product
