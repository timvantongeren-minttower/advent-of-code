from argparse import ArgumentParser
import os
from importlib import import_module


def handle_question(year: int, day: int, test: bool, part: int):
    folder = os.path.join(".", str(year), str(day))
    filename = "test_input.txt" if test else "real_input.txt"
    with open(os.path.join(folder, filename), "r") as f:
        all_lines = f.readlines()

    get_answer = import_module(f"{year}.{day}.solution_part{part}").get_answer

    answer = get_answer(all_lines)
    print(answer)
    if test:
        with open(os.path.join(folder, f"test_answer{part}.txt"), "r") as f:
            test_answer = int(f.read().strip())
        assert answer == test_answer


def parse_arguments() -> tuple[int, int, bool, int]:
    parser = ArgumentParser()
    parser.add_argument(
        "--year",
        required=True,
        type=int,
        help="Year of advent",
    )
    parser.add_argument(
        "--day",
        required=True,
        type=int,
        help="Day of advent",
    )
    parser.add_argument(
        "--test",
        required=True,
        type=int,
        choices=[0, 1],
        help="Test mode",
    )
    parser.add_argument(
        "--part",
        required=True,
        type=int,
        choices=[1, 2],
        help="Part 1 or 2 of the question",
    )
    args = parser.parse_args()
    return (args.year, args.day, True if args.test else False, args.part)


if __name__ == "__main__":
    handle_question(*parse_arguments())
