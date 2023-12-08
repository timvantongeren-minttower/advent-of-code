def get_answer(all_lines: list[str]) -> int:
    sum_of_powers = 0

    for line in all_lines:
        bag = {}

        line = line.replace("\n", "")
        _, draws_part = line.split(": ")
        for draw in draws_part.split("; "):
            for color_draw in draw.split(", "):
                string_number, color = color_draw.split(" ")
                number = int(string_number)
                if not color in bag or number > bag[color]:
                    bag[color] = number

        this_power = bag["red"] * bag["green"] * bag["blue"]
        sum_of_powers += this_power

    return sum_of_powers
