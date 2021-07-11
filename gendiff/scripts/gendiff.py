"""Gendiff script."""
from gendiff.cli import get_args
from gendiff.constants import FORMATERS
from gendiff.diff_generator import generate_diff


def main():
    """Run main function."""
    args = get_args(list(FORMATERS))
    print(generate_diff(args.first_file, args.second_file, args.format))


if __name__ == '__main__':
    main()
