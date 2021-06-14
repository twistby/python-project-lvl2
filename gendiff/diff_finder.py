"""Find differencies."""
import json
import pathlib

import yaml


def get_dict_from_file(file_path: str) -> dict:
    """Open file and transform to dict."""
    with open(file_path) as dict_file:
        file_extansion = pathlib.Path(file_path).suffix
        if file_extansion == '.json':
            dict_from_file = dict(json.load(dict_file))
            return {} if dict_from_file is None else dict_from_file
        elif file_extansion in {'.yml', '.yaml'}:
            dict_from_file = yaml.safe_load(dict_file)
            return {} if dict_from_file is None else dict_from_file
        raise ValueError('Incorrect data file.')


def formatting_value(string: str) -> str:
    """Format boolen to lowercase, None to null, remove control charachters."""
    string = string.rstrip('\n').rstrip('\r')
    if string in {'False', 'True'}:
        string = string.lower()
    if string == 'None':
        string = 'null'
    return string


def generate_dict_diff(first_dict: dict, second_dict: dict) -> str:
    """Get difference between two dictionaries."""
    key_list = list(set(first_dict).union(set(second_dict)))
    key_list.sort()

    def get_dif(dict_key: str) -> str:
        """Get difference between two values of dictionaries."""
        first_value = first_dict.get(dict_key)
        second_value = second_dict.get(dict_key)
        if first_value is None:
            return '+ {k}: {v}'.format(
                k=dict_key,
                v=formatting_value(str(second_value)),
            )
        elif second_value is None:
            return '- {k}: {v}'.format(
                k=dict_key,
                v=formatting_value(str(first_value)),
            )
        elif first_value == second_value:
            return '  {k}: {v}'.format(
                k=dict_key,
                v=formatting_value(str(first_value)),
            )
        return '- {k}: {v}\n+ {k}: {v2}'.format(
            k=dict_key,
            v=formatting_value(str(first_value)),
            v2=formatting_value(str(second_value)),
        )
    return '{start}\n{body}{end}'.format(
        start='{',
        body='\n'.join(list(map(get_dif, key_list))),
        end='\n}' if key_list else '}',
    )


def generate_diff(first_path: str, second_path: str) -> str:
    """Generate difference between two files."""
    first_dict = get_dict_from_file(first_path)
    second_dict = get_dict_from_file(second_path)
    return generate_dict_diff(first_dict, second_dict)
