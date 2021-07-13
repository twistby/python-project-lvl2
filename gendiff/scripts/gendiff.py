"""Gendiff script."""
from gendiff.cli import get_args
from gendiff.diff_generator import DEFAULT_FORMATER, formaters, generate_diff


def main():
    """Run main function."""
    args = get_args(formaters, DEFAULT_FORMATER)
    print(generate_diff(args.first_file, args.second_file, args.format))


if __name__ == '__main__':
    main()
