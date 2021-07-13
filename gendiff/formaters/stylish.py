"""Default differences report template."""
from typing import Any

from gendiff.diff_finder import ADDED, NESTED, REMOVED, UNCHANGED, UPDATED

signs = {
    UNCHANGED: '  ',
    ADDED: '+ ',
    REMOVED: '- ',
    UPDATED: '- ',
}
IDENT_STRING = '    '
DIFF_KIND_STRING = '  {s}'
LF_STRING = '\n'


def compile_diff(dif_value, depth):
    """Make formated diff from list."""
    return '{{{v}{e}{i}}}'.format(
        v=''.join(dif_value),
        e=LF_STRING,
        i=IDENT_STRING * depth,
    )


def format_value(some_value: Any, depth: int) -> str:
    """Format boolen to lowercase, None to null, remove control charachters."""
    if isinstance(some_value, dict):
        formated_value = []
        for dict_key, dict_value in some_value.items():
            formated_value.append(format_diff(
                depth,
                UNCHANGED,
                dict_key,
                format_value(dict_value, depth),
            ),
            )
        return compile_diff(formated_value, depth)
    if some_value in {False, True}:
        return str(some_value).lower()
    if some_value is None:
        return 'null'
    return str(some_value).rstrip('\n').rstrip('\r')


def format_diff(depth: int, diff_kind: str, key: str, diff_value: str) -> str:
    """Make formatted difference string."""
    return '{i}{s}{k}: {v}'.format(
        i='{l}{i}'.format(l=LF_STRING, i=IDENT_STRING * depth),
        s=DIFF_KIND_STRING.format(s=signs[diff_kind]),
        k=key,
        v=diff_value,
    )


def stylish(diff: dict, depth: int = 0) -> str:
    """Make default differences report."""
    formated_diff = []
    for key in sorted(diff.keys()):
        first_diff, second_diff, diff_kind = diff[key]
        if diff_kind == NESTED:
            formated_diff.append(format_diff(
                depth,
                UNCHANGED,
                key,
                stylish(first_diff, depth + 1),
            ),
            )
        else:
            formated_diff.append(format_diff(
                depth,
                diff_kind,
                key,
                format_value(first_diff, depth),
            ),
            )
            if diff_kind == UPDATED:
                formated_diff.append(format_diff(
                    depth,
                    ADDED,
                    key,
                    format_value(second_diff, depth),
                ),
                )
    return compile_diff(formated_diff, depth)
