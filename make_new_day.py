from argparse import ArgumentParser
import os
import shutil


def handle_question(year: int, day: int):
    folder = os.path.join(".", str(year), str(day))
    if os.path.exists(folder):
        os.removedirs(folder)
    os.makedirs(folder)
    template_folder = os.path.join(".", "template")
    for file in os.listdir(template_folder):
        shutil.copy(os.path.join(template_folder, file), os.path.join(folder, file))


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
