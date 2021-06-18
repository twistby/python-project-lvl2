"""Transform files to dictionaries."""
import json
import pathlib

import yaml


def transform_file_to_dict(file_path: str) -> dict:
    """Open file and transform to dict."""
    with open(file_path) as dict_file:
        file_extansion = pathlib.Path(file_path).suffix
        if file_extansion == '.json':
            dict_from_file = dict(json.load(dict_file))
            return {} if dict_from_file is None else dict_from_file
        elif file_extansion in {'.yml', '.yaml'}:
            dict_from_file = yaml.safe_load(dict_file)
            return {} if dict_from_file is None else dict_from_file
        raise ValueError('Incorrect data file: '.join(file_path))
