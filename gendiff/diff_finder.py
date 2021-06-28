"""Find differencies."""
from typing import Any


def pack_diff_to_dict(
    diff_kind: str,
    first_value: Any,
    second_value: Any = None,
) -> dict:
    """Packs the difference in the dictionary."""
    return {
        'is_differense': True,
        'diff_kind': diff_kind,
        'first_value': first_value,
        'second_value': second_value,
    }


def find_diff(first_data: dict, second_data: dict) -> dict:
    """Create dict with differences between two dictionaries."""
    first_dict_keys = set(first_data)
    second_dict_keys = set(second_data)
    differences = {}
    for dict_key in first_dict_keys.union(second_dict_keys):
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
                second_value,
            )
        differences[dict_key] = difference
    return differences
