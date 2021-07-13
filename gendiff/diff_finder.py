"""Find differencies."""
from typing import Any, Tuple

ADDED = 'added'
REMOVED = 'removed'
NESTED = 'nested'
UNCHANGED = 'unchanged'
UPDATED = 'updated'


def get_diff_node(
    diff_kind: str,
    first_value: Any,
    second_value: Any = None,
) -> Tuple:
    """Packs the difference in the dictionary."""
    return (
        first_value,
        second_value,
        diff_kind,
    )


def find_diff(first_data: dict, second_data: dict) -> dict:
    """Create dict with differences between two dictionaries."""
    first_dict_keys = set(first_data)
    second_dict_keys = set(second_data)
    diff = {}
    for dict_key in first_dict_keys.union(second_dict_keys):
        first_value = first_data.get(dict_key)
        second_value = second_data.get(dict_key)
        if first_value == second_value:
            diff_node = get_diff_node(UNCHANGED, first_value)
        elif dict_key not in first_dict_keys:
            diff_node = get_diff_node(ADDED, second_value)
        elif dict_key not in second_dict_keys:
            diff_node = get_diff_node(REMOVED, first_value)
        elif isinstance(first_value, dict) and isinstance(second_value, dict):
            diff_node = get_diff_node(
                NESTED,
                find_diff(first_value, second_value),
            )
        else:
            diff_node = get_diff_node(
                UPDATED,
                first_value,
                second_value,
            )
        diff[dict_key] = diff_node
    return diff
