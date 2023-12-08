def get_answer(all_lines: list[str]) -> int:
    number_of_cards_extra: dict[int, int] = {}
    for line in all_lines:
        # some parsing cleanup
        line = line.replace("\n", "").replace("  ", " ")
        # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        card_part, game_part = line.split(": ")
        card_number = int(card_part.split(" ")[-1])
        number_of_times_to_play = 1 + number_of_cards_extra.get(card_number, 0)
        my_numbers_part, winning_number_part = game_part.split(" | ")
        my_numbers = [int(partial) for partial in my_numbers_part.split(" ")]
        winning_numbers = [int(partial) for partial in winning_number_part.split(" ")]
        number_of_winners = sum([n in winning_numbers for n in my_numbers])
        if number_of_winners > 0:
            for index_to_add in range(1, number_of_winners + 1):
                game_to_add_to = card_number + index_to_add
                if not game_to_add_to in number_of_cards_extra:
                    number_of_cards_extra[game_to_add_to] = number_of_times_to_play
                else:
                    number_of_cards_extra[game_to_add_to] += number_of_times_to_play

    original_cards = len(all_lines)
    extra_cards = sum(number_of_cards_extra.values())
    return original_cards + extra_cards
