def main(test: bool = False):
    filename = "test_input.txt" if test else "real_input.txt"
    with open(filename, "r") as f:
        all_lines = f.readlines()


if __name__ == "__main__":
    main()
