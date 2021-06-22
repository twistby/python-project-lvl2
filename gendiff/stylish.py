"""Default differences report template."""
from typing import Any, Tuple

from gendiff.token import DIFF_TOKEN


def format_value(string: str) -> str:
    """Format boolen to lowercase, None to null, remove control charachters."""
    string = string.rstrip('\n').rstrip('\r')
    if string in {'False', 'True'}:
        string = string.lower()
    if string == 'None':
        string = 'null'
    return string


def make_diff_string(ident: str, sign: str, key: str, diff_value: str) -> str:
    """Make formatted difference string."""
    return '\n{i}{s}{k}: {v}'.format(
        i=ident,
        s=sign,
        k=key,
        v=diff_value,
    )


def get_sign(diff_kind: str) -> str:
    """Return difference sign."""
    signs = {
        'unchanged': '  ',
        'added': '+ ',
        'removed': '- ',
        'updated': '- ',
    }
    return signs[diff_kind]


def get_diff_value(difference: Any, indent_counter: int) -> str:
    """Get difference value from dict."""
    if isinstance(difference, dict):
        return stylish(difference, indent_counter + 1)
    return format_value(str(difference))


def get_differences(diff: dict) -> Tuple[Any, Any, str]:
    """Return values depending on whether it is a dict of differences or not."""
    if diff.get('token') == DIFF_TOKEN:
        return diff['first_diff'], diff['seconf_diff'], '  {s}'.format(
            s=get_sign(diff['diff_kind']),
        )
    return diff, None, '    '


def stylish(diff_dict: dict, indent_counter: int = 0) -> str:
    """Make default differences report."""
    indent = '    ' * indent_counter
    diff_string = '{'
    if not diff_dict:
        return diff_string + '\n{i}{v}'.format(i=indent, v='}')
    key_list = list(set(diff_dict))
    key_list.sort()
    for key in key_list:
        difference = diff_dict[key]
        if isinstance(difference, dict):
            first_diff, second_diff, sign = get_differences(difference)
            diff_string += make_diff_string(
                indent,
                sign,
                key,
                get_diff_value(first_diff, indent_counter),
            )
            if second_diff is not None:
                diff_string += make_diff_string(
                    indent,
                    '  + ',
                    key,
                    get_diff_value(second_diff, indent_counter),
                )
        else:
            diff_string += make_diff_string(indent, '    ', key, difference)
    diff_string += '\n{i}{v}'.format(i=indent, v='}')
    return diff_string
