"""Find differencies."""
from typing import Any, Callable

from gendiff.stylish import stylish
from gendiff.token import DIFF_TOKEN
from gendiff.transformator import transform_file_to_dict


def none_to_null(none_value):
    """Convert None to string null."""
    if str(none_value) == 'None':
        return 'null'
    return none_value


def pack_diff_to_dict(
    diff_kind: str,
    first_value: Any,
    second_value: Any = None,
) -> dict:
    """Packs the difference in the dictionary."""
    return {
        'token': DIFF_TOKEN,
        'diff_kind': diff_kind,
        'first_diff': first_value,
        'seconf_diff': second_value,
    }


def find_diff(first_data: dict, second_data: dict) -> dict:
    """Create dict with differences between two dictionaries."""
    first_dict_keys = set(first_data)
    second_dict_keys = set(second_data)
    key_list = list(first_dict_keys.union(second_dict_keys))
    differences = {}
    for dict_key in key_list:
        first_value = first_data.get(dict_key)
        second_value = second_data.get(dict_key)
        if first_value == second_value:
            difference = pack_diff_to_dict('unchanged', first_value)
        elif dict_key not in first_dict_keys:
            difference = pack_diff_to_dict('added', second_value)
        elif dict_key not in second_dict_keys:
            difference = pack_diff_to_dict('removed', first_value)
        elif isinstance(first_value, dict) and isinstance(second_value, dict):
            difference = pack_diff_to_dict(
                'unchanged',
                find_diff(first_value, second_value),
            )
        else:
            difference = pack_diff_to_dict(
                'updated',
                first_value,
                none_to_null(second_value),
            )
        differences[dict_key] = difference
    return differences


def generate_diff(first_path: str, second_path: str, formater: Callable = stylish) -> str:
    """Generate difference between two files."""
    first_dict = transform_file_to_dict(first_path)
    second_dict = transform_file_to_dict(second_path)
    differences = find_diff(first_dict, second_dict)
    return formater(differences)
