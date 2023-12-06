def main(test: bool = False):
    filename = "test_input.txt" if test else "real_input.txt"
    with open(filename, "r") as f:
        all_lines = f.readlines()

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

    print(sum_of_powers)
    if test:
        assert sum_of_powers == 2286


if __name__ == "__main__":
    main()
