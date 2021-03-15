"""Gendiff script."""
from gendiff.diff_finder import generate_diff
from gendiff.parser import get_args


def main():
    """Run main function."""
    args = get_args()
    print(generate_diff(args.first_file, args.second_file))


if __name__ == '__main__':
    main()
