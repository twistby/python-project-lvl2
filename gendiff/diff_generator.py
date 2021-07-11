"""Diff generator."""
from gendiff.constants import FORMATERS
from gendiff.diff_finder import find_diff
from gendiff.file_reader import read_file
from gendiff.formaters.jsonlish import jsonlish
from gendiff.formaters.plain import plain
from gendiff.formaters.stylish import stylish

DEFAULT_FORMATER = FORMATERS[0]


def generate_diff(
    first_file: str,
    second_file: str,
    formater: str = DEFAULT_FORMATER,
) -> str:
    """Generate differences."""
    first_dict = read_file(first_file)
    second_dict = read_file(second_file)
    diff = find_diff(first_dict, second_dict)
    if formater == FORMATERS[0]:
        return stylish(diff)
    elif formater == FORMATERS[1]:
        return plain(diff)
    elif formater == FORMATERS[2]:
        return jsonlish(diff)
    raise ValueError('Incorrect format: {f}'.format(f=formater))
