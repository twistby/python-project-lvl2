"""Diff generator."""
from gendiff.diff_finder import find_diff
from gendiff.file_reader import read_file
from gendiff.formaters.jsonlish import jsonlish
from gendiff.formaters.plain import plain
from gendiff.formaters.stylish import stylish

STYLISH_FORMATER = 'stylish'
PLAIN_FORMATER = 'plain'
JSON_FORMATER = 'json'

formaters = [
    STYLISH_FORMATER,
    PLAIN_FORMATER,
    JSON_FORMATER,
]

DEFAULT_FORMATER = STYLISH_FORMATER


def generate_diff(
    first_file: str,
    second_file: str,
    formater: str = STYLISH_FORMATER,
) -> str:
    """Generate differences."""
    first_dict = read_file(first_file)
    second_dict = read_file(second_file)
    diff = find_diff(first_dict, second_dict)
    if formater == STYLISH_FORMATER:
        return stylish(diff)
    elif formater == PLAIN_FORMATER:
        return plain(diff)
    elif formater == JSON_FORMATER:
        return jsonlish(diff)
    raise ValueError('Incorrect format: {f}'.format(f=formater))
