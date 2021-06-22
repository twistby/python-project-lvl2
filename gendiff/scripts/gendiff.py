"""Gendiff script."""
from gendiff.diff_finder import generate_diff
from gendiff.parser import get_args
from gendiff.templates.plain import plain
from gendiff.templates.stylish import stylish


def main():
    """Run main function."""
    args = get_args()
    if args.format == 'plain':
        formater = plain
    else:
        formater = stylish
    print(generate_diff(args.first_file, args.second_file, formater))


if __name__ == '__main__':
    main()
