"""Plain formater."""
from typing import Any, Tuple

from gendiff.constants import DIFF_KINDS


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
    child: str,
    diff_kind: str,
    first_value: Any,
    second_value: Any = '',
) -> str:
    """Make formatted difference string."""
    if diff_kind == DIFF_KINDS[0]:
        return ''
    if diff_kind == DIFF_KINDS[1]:
        tail = 'was added with value: {v}'.format(v=first_value)
    elif diff_kind == DIFF_KINDS[2]:
        tail = 'was removed'
    elif diff_kind == DIFF_KINDS[3]:
        tail = 'was updated. From {f} to {t}'.format(
            f=first_value,
            t=second_value,
        )
    return "Property '{c}' {t}\n".format(c=child, t=tail)


def get_diff_data(diff: dict) -> Tuple[Any, Any, str]:
    """Return values of diff."""
    return diff['first_value'], diff['second_value'], diff['diff_kind']


def to_plain(diff: dict, parent: str = '') -> str:
    """Make plain report."""
    diff_strings = []
    for key in sorted(diff.keys()):
        current_parent = '{p}.{c}'.format(p=parent, c=key) if parent else key
        diff_node = diff[key]
        first_diff, second_diff, diff_kind = get_diff_data(diff_node)
        if diff_kind == DIFF_KINDS[0]:
            if isinstance(first_diff, dict):
                diff_strings.append(to_plain(first_diff, current_parent))
            else:
                diff_strings.append(format_diff(
                    current_parent,
                    diff_kind,
                    format_value(first_diff),
                    format_value(second_diff),
                ),
                )
        else:
            diff_strings.append(format_diff(
                current_parent,
                diff_kind,
                format_value(first_diff),
                format_value(second_diff),
            ),
            )
    return ''.join(diff_strings)


def plain(diff: Any) -> str:
    """Make report and cut off last line break."""
    return to_plain(diff).rstrip('\n')
