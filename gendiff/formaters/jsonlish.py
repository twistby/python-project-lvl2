"""JSON formater."""
import json
from typing import Any, Tuple

from gendiff.constants import DIFF_KINDS


def iscomplex(some_value: Any) -> bool:
    """Check value is complex."""
    return isinstance(some_value, (dict, list))


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
    if diff_kind == DIFF_KINDS[0]:
        return {'diffKind': DIFF_KINDS[0], 'value': first_value}
    if diff_kind == DIFF_KINDS[1]:
        return {'diffKind': DIFF_KINDS[1], 'value': first_value}
    elif diff_kind == DIFF_KINDS[2]:
        return {'diffKind': DIFF_KINDS[2]}
    return {'diffKind': DIFF_KINDS[3], 'from': first_value, 'to': second_value}


def get_diff_data(node: dict) -> Tuple[Any, Any, str]:
    """Return values  of diff."""
    return node['first_value'], node['second_value'], node['diff_kind']


def to_json(diff: dict) -> dict:
    """Prepare diff dict for transformation to JSON."""
    result_dict = {}
    for key in sorted(diff.keys()):
        diff_node = diff[key]
        first_diff, second_diff, diff_kind = get_diff_data(diff_node)
        if diff_kind == DIFF_KINDS[0]:
            if isinstance(first_diff, dict):
                result_dict[key] = to_json(first_diff)
            else:
                result_dict[key] = format_diff(
                    diff_kind,
                    format_value(first_diff),
                    format_value(second_diff),
                )
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
