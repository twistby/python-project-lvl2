"""Find differencies."""
from typing import Any

from gendiff.constants import DIFF_KINDS


def get_diff_node(
    diff_kind: str,
    first_value: Any,
    second_value: Any = None,
) -> dict:
    """Packs the difference in the dictionary."""
    return {
        'diff_kind': diff_kind,
        'first_value': first_value,
        'second_value': second_value,
    }


def find_diff(first_data: dict, second_data: dict) -> dict:
    """Create dict with differences between two dictionaries."""
    first_dict_keys = set(first_data)
    second_dict_keys = set(second_data)
    diff = {}
    for dict_key in first_dict_keys.union(second_dict_keys):
        first_value = first_data.get(dict_key)
        second_value = second_data.get(dict_key)
        if first_value == second_value:
            diff_node = get_diff_node(DIFF_KINDS[0], first_value)
        elif dict_key not in first_dict_keys:
            diff_node = get_diff_node(DIFF_KINDS[1], second_value)
        elif dict_key not in second_dict_keys:
            diff_node = get_diff_node(DIFF_KINDS[2], first_value)
        elif isinstance(first_value, dict) and isinstance(second_value, dict):
            diff_node = get_diff_node(
                DIFF_KINDS[0],
                find_diff(first_value, second_value),
            )
        else:
            diff_node = get_diff_node(
                DIFF_KINDS[3],
                first_value,
                second_value,
            )
        diff[dict_key] = diff_node
    return diff
