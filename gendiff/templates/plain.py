"""Plain report template."""
from typing import Any

from gendiff.token import DIFF_TOKEN


def iscomplex(some_value: Any) -> bool:
    """Check is value is complex."""
    return (
        not isinstance(some_value, (str, int, float, complex, bool))
        and some_value is not None
    )


def format_value(some_value: Any) -> Any:
    """Format boolen to lowercase, None to null, remove control charachters."""
    if iscomplex(some_value):
        return '[complex value]'
    if isinstance(some_value, bool) or some_value in {'False', 'True'}:
        return '{v}'.format(v=str(some_value).lower())
    if isinstance(some_value, (int, float, complex)):
        return some_value
    string = str(some_value).rstrip('\n').rstrip('\r')
    if string in {'None', 'null'}:
        return 'null'
    return "'{v}'".format(v=string)


def make_diff_string(
    child: str,
    diff_kind: str,
    first_value: str,
    second_value: str = '',
) -> str:
    """Make formatted difference string."""
    if diff_kind == 'unchanged':
        return ''
    if diff_kind == 'added':
        tail = 'was added with value: {v}'.format(v=first_value)
    elif diff_kind == 'removed':
        tail = 'was removed'
    elif diff_kind == 'updated':
        tail = 'was updated. From {f} to {t}'.format(
            f=first_value,
            t=second_value,
        )
    return "Property '{c}' {t}\n".format(c=child, t=tail)


def to_plain(diff_dict: Any, parent: str = '') -> str:
    """Make default plain report."""
    if not isinstance(diff_dict, dict):
        return DIFF_TOKEN
    diff_string = ''
    key_list = list(set(diff_dict))
    key_list.sort()
    for key in key_list:
        child = parent + '.{c}'.format(c=key) if parent else key
        difference = diff_dict[key]
        if isinstance(difference, dict):
            if difference.get('token') == DIFF_TOKEN:
                substring = to_plain(difference['first_value'], child)
                if substring == DIFF_TOKEN:
                    diff_string += make_diff_string(
                        child,
                        difference['diff_kind'],
                        format_value(difference['first_value']),
                        format_value(difference['second_value']),
                    )
                else:
                    diff_string += substring
            else:
                return DIFF_TOKEN
        else:
            return DIFF_TOKEN
    return diff_string


def plain(diff_dict: Any) -> str:
    """Make report anfd strip last line break."""
    return to_plain(diff_dict).rstrip('\n')
