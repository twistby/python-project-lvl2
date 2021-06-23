"""Plain report template."""
from typing import Any

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
        return '[complex value]'
    string = str(some_value).rstrip('\n').rstrip('\r')
    if string in {'False', 'True'}:
        return string.lower()
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
    return "\nProperty '{c}' {t}".format(c=child, t=tail)


def plain(diff_dict: Any, parent: str = '') -> str:
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
                substring = plain(difference['first_diff'], child)
                if substring == DIFF_TOKEN:
                    diff_string += make_diff_string(
                        child,
                        difference['diff_kind'],
                        format_value(difference['first_diff']),
                        format_value(difference['seconf_diff']),
                    )
                else:
                    diff_string += substring
            else:
                return DIFF_TOKEN
        else:
            return DIFF_TOKEN
    return diff_string
