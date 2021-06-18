"""Find differencies."""
from typing import Any, Callable

from gendiff.stylish import stylish
from gendiff.transformator import transform_file_to_dict


def none_to_null(none_value):
    """Convert None to string null."""
    if str(none_value) == 'None':
        return 'null'
    return none_value


def pack_diff_to_dict(
    sign: str,
    first_value: Any,
    second_value: Any = None,
) -> dict:
    """Packs the difference in the dictionary."""
    return {'sign': sign, 'first_diff': first_value, 'seconf_diff': second_value}


def find_diff(first_dict: dict, second_dict: dict) -> dict:
    """Create dict with differences between two dictionaries."""
    first_dict_keys = set(first_dict)
    second_dict_keys = set(second_dict)
    key_list = list(first_dict_keys.union(second_dict_keys))
    differences = {}
    for dict_key in key_list:
        first_value = first_dict.get(dict_key)
        second_value = second_dict.get(dict_key)
        if first_value == second_value:
            difference = pack_diff_to_dict('  ', first_value)
        elif dict_key not in first_dict_keys:
            difference = pack_diff_to_dict('+ ', second_value)
        elif dict_key not in second_dict_keys:
            difference = pack_diff_to_dict('- ', first_value)
        elif isinstance(first_value, dict) and isinstance(second_value, dict):
            difference = pack_diff_to_dict('  ', find_diff(first_value, second_value))
        else:
            difference = pack_diff_to_dict('- ', first_value, none_to_null(second_value))
        differences[dict_key] = difference
    return differences


def generate_diff(first_path: str, second_path: str, formater: Callable = stylish) -> str:
    """Generate difference between two files."""
    first_dict = transform_file_to_dict(first_path)
    second_dict = transform_file_to_dict(second_path)
    differences = find_diff(first_dict, second_dict)
    return formater(differences)
