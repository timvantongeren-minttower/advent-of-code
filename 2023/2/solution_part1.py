def main(test: bool = False):
    filename = "test_input.txt" if test else "real_input.txt"
    with open(filename, "r") as f:
        all_lines = f.readlines()

    bag = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    sum_of_possible_ids = 0

    for line in all_lines:
        line = line.replace("\n", "")
        game_part, draws_part = line.split(": ")
        game_number = int(game_part.split(" ")[-1])
        game_is_possible = True
        for draw in draws_part.split("; "):
            for color_draw in draw.split(", "):
                string_number, color = color_draw.split(" ")
                number = int(string_number)
                if not color in bag or number > bag[color]:
                    game_is_possible = False
                    break
            if not game_is_possible:
                break

        if game_is_possible:
            sum_of_possible_ids += game_number

    print(sum_of_possible_ids)
    if test:
        assert sum_of_possible_ids == 8


if __name__ == "__main__":
    main()
