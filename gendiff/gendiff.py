"""Gendiff script."""
from gendiff.diff_finder import find_diff
from gendiff.parser import get_args
from gendiff.templates.jsonlish import jsonlish
from gendiff.templates.plain import plain
from gendiff.templates.stylish import stylish
from gendiff.transformator import transform_file_to_dict

STYLISH_FORMATER = 'stylish'
PLAIN_FORMATER = 'plain'
JSONLISH_FORMATER = 'json'


def generate_diff(
    first_file: str,
    second_file: str,
    formater_string: str = STYLISH_FORMATER,
) -> str:
    """Generate differences."""
    first_dict = transform_file_to_dict(first_file)
    second_dict = transform_file_to_dict(second_file)
    differences = find_diff(first_dict, second_dict)
    if formater_string == PLAIN_FORMATER:
        return plain(differences)
    elif formater_string == JSONLISH_FORMATER:
        return jsonlish(differences)
    elif formater_string in {STYLISH_FORMATER, None}:
        return stylish(differences)


def main():
    """Run main function."""
    args = get_args(STYLISH_FORMATER, PLAIN_FORMATER, JSONLISH_FORMATER)
    print(generate_diff(args.first_file, args.second_file, args.format))


if __name__ == '__main__':
    main()
