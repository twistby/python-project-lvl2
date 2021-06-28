"""Default differences report template."""
from typing import Any, Tuple


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
    if diff.get('is_differense'):
        return diff['first_value'], diff['second_value'], diff['diff_kind']
    return diff, None, 'unchanged'


def stylish(diff_dict: dict, indent_counter: int = 0) -> str:
    """Make default differences report."""
    indent = '    ' * indent_counter
    if not diff_dict:
        return '{s}\n{i}{v}'.format(s='{', i=indent, v='}')
    diff_list = ['{']
    for key in sorted(diff_dict.keys()):
        difference = diff_dict[key]
        if isinstance(difference, dict):
            first_diff, second_diff, diff_kind = get_differences(difference)
            diff_list.append(make_diff_string(
                indent,
                '  {s}'.format(s=get_sign(diff_kind)),
                key,
                get_diff_value(first_diff, indent_counter),
            ),
            )
            if diff_kind == 'updated':
                diff_list.append(make_diff_string(
                    indent,
                    '  + ',
                    key,
                    get_diff_value(second_diff, indent_counter),
                ),
                )
        else:
            diff_list.append(make_diff_string(indent, '    ', key, difference))
    diff_list.append('\n{i}{v}'.format(i=indent, v='}'))
    return ''.join(diff_list)
