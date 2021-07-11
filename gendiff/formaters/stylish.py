"""Default differences report template."""
from typing import Any, Tuple

from gendiff.constants import DIFF_KINDS

signs = {
    DIFF_KINDS[0]: '  ',
    DIFF_KINDS[1]: '+ ',
    DIFF_KINDS[2]: '- ',
    DIFF_KINDS[3]: '- ',
}


def format_value(string: str) -> str:
    """Format boolen to lowercase, None to null, remove control charachters."""
    string = string.rstrip('\n').rstrip('\r')
    if string in {'False', 'True'}:
        string = string.lower()
    if string == 'None':
        string = 'null'
    return string


def format_diff(ident: str, sign: str, key: str, diff_value: str) -> str:
    """Make formatted difference string."""
    return '\n{i}{s}{k}: {v}'.format(
        i=ident,
        s=sign,
        k=key,
        v=diff_value,
    )


def get_value(difference: Any, depth: int) -> str:
    """Get difference value from dict."""
    if isinstance(difference, dict):
        return stylish(difference, depth + 1)
    return format_value(str(difference))


def get_diff_data(diff: dict) -> Tuple[Any, Any, str]:
    """Return values depending on whether it is a dict of differences or not."""
    if diff.get('diff_kind'):
        return diff['first_value'], diff['second_value'], diff['diff_kind']
    return diff, None, DIFF_KINDS[0]


def stylish(diff: dict, depth: int = 0) -> str:
    """Make default differences report."""
    indent = '    ' * depth
    if not diff:
        return '{s}\n{i}{v}'.format(s='{', i=indent, v='}')
    diff_strings = ['{']
    for key in sorted(diff.keys()):
        diff_node = diff[key]
        if isinstance(diff_node, dict):
            first_diff, second_diff, diff_kind = get_diff_data(diff_node)
            diff_strings.append(format_diff(
                indent,
                '  {s}'.format(s=signs[diff_kind]),
                key,
                get_value(first_diff, depth),
            ),
            )
            if diff_kind == DIFF_KINDS[3]:
                diff_strings.append(format_diff(
                    indent,
                    '  {s}'.format(s=signs[DIFF_KINDS[1]]),
                    key,
                    get_value(second_diff, depth),
                ),
                )
        else:
            diff_strings.append(
                format_diff(
                    indent,
                    '  {s}'.format(s=signs[DIFF_KINDS[0]]),
                    key,
                    diff_node,
                ),
            )
    diff_strings.append('\n{i}{v}'.format(i=indent, v='}'))
    return ''.join(diff_strings)
