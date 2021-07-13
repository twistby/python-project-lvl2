"""JSON formater."""
import json
from typing import Any

from gendiff.diff_finder import ADDED, NESTED, REMOVED, UNCHANGED, UPDATED


def format_value(some_value: Any) -> Any:
    """Format value.

    boolen to lowercase.
    None to null.
    Remove control charachters.
    """
    if isinstance(some_value, bool):
        return '{v}'.format(v=str(some_value).lower())
    if some_value is None:
        return 'null'
    if isinstance(some_value, str):
        '{v}'.format(v=some_value.rstrip('\n').rstrip('\r'))
    return some_value


def format_diff(
    diff_kind: str,
    first_value: Any,
    second_value: Any = '',
) -> dict:
    """Make diff dict."""
    if diff_kind == UNCHANGED:
        return {'diffKind': UNCHANGED, 'value': first_value}
    if diff_kind == ADDED:
        return {'diffKind': ADDED, 'value': first_value}
    elif diff_kind == REMOVED:
        return {'diffKind': REMOVED}
    return {'diffKind': UPDATED, 'from': first_value, 'to': second_value}


def to_json(diff: dict) -> dict:
    """Prepare diff dict for transformation to JSON."""
    result_dict = {}
    for key in sorted(diff.keys()):
        first_diff, second_diff, diff_kind = diff[key]
        if diff_kind == NESTED:
            result_dict[key] = to_json(first_diff)
        else:
            result_dict[key] = format_diff(
                diff_kind,
                format_value(first_diff),
                format_value(second_diff),
            )
    return result_dict


def jsonlish(diff: dict) -> str:
    """Make JSON report."""
    return json.dumps(to_json(diff))
