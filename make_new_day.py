from argparse import ArgumentParser
import os
import shutil


def handle_question(year: int, day: int):
    folder = rf".\{year}\{day}"
    os.makedirs(folder)
    shutil.copy(r".\template\*", folder)


def parse_arguments() -> tuple[int, int]:
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
    args = parser.parse_args()
    return (args.year, args.day)


if __name__ == "__main__":
    handle_question(*parse_arguments())
