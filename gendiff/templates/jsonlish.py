"""JSON report template."""
import json
from typing import Any, Dict

from gendiff.token import DIFF_TOKEN


def iscomplex(some_value: Any) -> bool:
    """Check is value is complex."""
    return (
        not isinstance(some_value, (str, int, float, complex, bool)) and
        some_value is not None
    )


def format_value(some_value: Any) -> str:
    """Format boolen to lowercase, None to null, remove control charachters."""
    if iscomplex(some_value):
        return some_value
    string = str(some_value).rstrip('\n').rstrip('\r')
    if string in {'False', 'True'}:
        return string.lower()
    if string in {'None', 'null'}:
        return 'null'
    return '{v}'.format(v=string)


def make_diff_dict(
    diff_kind: str,
    first_value: Any,
    second_value: Any = '',
) -> dict:
    """Make difference dict."""
    if diff_kind == 'unchanged':
        return {'diffKind': 'unchanged', 'value': first_value}
    if diff_kind == 'added':
        return {'diffKind': 'added', 'value': first_value}
    elif diff_kind == 'removed':
        return {'diffKind': 'removed'}
    return {'diffKind': 'updated', 'from': first_value, 'to': second_value}


def to_json(diff_dict: Any) -> Any:
    """Prepare diff dict for transformation to JSON."""
    if not isinstance(diff_dict, dict):
        return DIFF_TOKEN
    result_dict = {}
    key_list = list(set(diff_dict))
    key_list.sort()
    for key in key_list:
        difference = diff_dict[key]
        if isinstance(difference, dict):
            if difference.get('token') == DIFF_TOKEN:
                subdict = to_json(difference['first_value'])
                if subdict == DIFF_TOKEN:
                    result_dict[key] = make_diff_dict(
                        difference['diff_kind'],
                        format_value(difference['first_value']),
                        format_value(difference['second_value']),
                    )
                else:
                    result_dict[key] = subdict
            else:
                return DIFF_TOKEN
        else:
            return DIFF_TOKEN
    return result_dict


def jsonlish(diff_dict: dict) -> Dict[Any, Dict[Any, Any]]:
    """Make JSON report."""
    return json.loads(json.dumps(to_json(diff_dict)))
