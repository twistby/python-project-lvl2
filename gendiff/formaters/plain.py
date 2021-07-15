"""Plain formater."""
from typing import Any

from gendiff.diff_finder import ADDED, NESTED, REMOVED, UNCHANGED, UPDATED


def iscomplex(some_value: Any) -> bool:
    """Check is value is complex."""
    return isinstance(some_value, (dict, list))


def format_value(some_value: Any) -> Any:
    """Format value.

    dict and list to string [complex value].
    boolen to lowercase string.
    None to string null.
    Remove control charachters.
    """
    if iscomplex(some_value):
        return '[complex value]'
    if isinstance(some_value, bool):
        return '{v}'.format(v=str(some_value).lower())
    if some_value is None:
        return 'null'
    if isinstance(some_value, str):
        return "'{v}'".format(v=some_value.rstrip('\n').rstrip('\r'))
    return some_value


def format_diff(
    parent: str,
    diff_kind: str,
    first_value: Any,
    second_value: Any = '',
) -> str:
    """Make formatted difference string."""
    if diff_kind == UNCHANGED:
        return ''
    if diff_kind == ADDED:
        return "Property '{p}' was added with value: {v}\n".format(
            p=parent,
            v=first_value,
        )
    elif diff_kind == REMOVED:
        return "Property '{p}' was removed\n".format(p=parent)
    elif diff_kind == UPDATED:
        return "Property '{p}' was updated. From {f} to {t}\n".format(
            p=parent,
            f=first_value,
            t=second_value,
        )


def to_plain(diff: dict, parent: str = '') -> str:
    """Make plain report."""
    diff_strings = []
    for key in sorted(diff.keys()):
        current_parent = '{p}.{c}'.format(p=parent, c=key) if parent else key
        first_diff, second_diff, diff_kind = diff[key]
        if diff_kind == NESTED:
            diff_strings.append(to_plain(first_diff, current_parent))
        else:
            diff_strings.append(format_diff(
                current_parent,
                diff_kind,
                format_value(first_diff),
                format_value(second_diff),
            ),
            )
    return ''.join(diff_strings)


def plain(diff: dict) -> str:
    """Make report and cut off last line break."""
    return to_plain(diff).rstrip('\n')
