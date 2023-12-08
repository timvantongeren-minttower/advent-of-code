def get_answer(all_lines: list[str]) -> int:
    total_sum = 0
    for line in all_lines:
        # some parsing cleanup
        line = line.replace("\n", "").replace("  ", " ")
        # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        card_part, game_part = line.split(": ")
        card_number = int(card_part.split(" ")[-1])
        my_numbers_part, winning_number_part = game_part.split(" | ")
        my_numbers = [int(partial) for partial in my_numbers_part.split(" ")]
        winning_numbers = [int(partial) for partial in winning_number_part.split(" ")]
        number_of_winners = sum([n in winning_numbers for n in my_numbers])
        if number_of_winners > 0:
            points_for_this_game = 2 ** (number_of_winners - 1)
        else:
            points_for_this_game = 0
        total_sum += points_for_this_game
    return total_sum
