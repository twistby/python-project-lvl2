"""Gendiff script."""
from typing import Callable

from gendiff.diff_finder import find_diff
from gendiff.parser import get_args
from gendiff.templates.jsonlish import jsonlish
from gendiff.templates.plain import plain
from gendiff.templates.stylish import stylish
from gendiff.transformator import transform_file_to_dict


def generate_diff(
    first_file: str,
    second_file: str,
    formater: Callable = stylish,
) -> str:
    """Generate differences."""
    first_dict = transform_file_to_dict(first_file)
    second_dict = transform_file_to_dict(second_file)
    differences = find_diff(first_dict, second_dict)
    return formater(differences)


def main():
    """Run main function."""
    args = get_args()
    if args.format == 'plain':
        formater = plain
    elif args.format == 'json':
        formater = jsonlish
    else:
        formater = stylish
    print(generate_diff(args.first_file, args.second_file, formater))


if __name__ == '__main__':
    main()
