"""Find differencies."""
import json


def get_dict_from_file(file_path):
    """Open file and transform to dict."""
    with open(file_path) as dict_file:
        return dict(json.load(dict_file))


def generate_diff(first_path, second_path):
    """Generate difference between two files."""
    first_dict = get_dict_from_file(first_path)
    second_dict = get_dict_from_file(second_path)
    key_list = list(set(first_dict).union(set(second_dict)))
    key_list.sort()

    def get_dif(dict_key):
        """Get difference between two values of dictionaries."""
        first_value = first_dict.get(dict_key)
        second_value = second_dict.get(dict_key)
        if first_value is None:
            return '+ {k}: {v}'.format(k=dict_key, v=second_value)
        elif second_value is None:
            return '- {k}: {v}'.format(k=dict_key, v=first_value)
        elif first_value == second_value:
            return '  {k}: {v}'.format(k=dict_key, v=first_value)
        return '- {k}: {v}\n+ {k}: {v2}'.format(
            k=dict_key,
            v=first_value,
            v2=second_value,
        )
    return '{start}\n{body}{end}'.format(
        start='{',
        body='\n'.join(list(map(get_dif, key_list))),
        end='\n}',
    )
