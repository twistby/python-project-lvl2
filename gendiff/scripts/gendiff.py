"""Gendiff script."""
import argparse
import json


def generate_diff(first_path, second_path):
    """Generate difference between two files."""
    with open(first_path) as first_file:
        first_dict = dict(json.load(first_file))
    with open(second_path) as second_file:
        second_dict = dict(json.load(second_file))
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
    return '{op}\n{st}{cl}'.format(
        op='{',
        st='\n'.join(list(map(get_dif, key_list))),
        cl='\n}',
    )


def main():
    """Run main function."""
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file))


if __name__ == '__main__':
    main()
