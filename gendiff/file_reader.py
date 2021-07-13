"""Transform files to dictionaries."""
import json
import pathlib

import yaml

JSON_SUFIX = '.json'
YAML_SUFIXES = ('.yml', '.yaml')


def read_file(file_path: str) -> dict:
    """Open file and transform to dict."""
    with open(file_path) as dict_file:
        file_extansion = pathlib.Path(file_path).suffix.lower()
        if file_extansion == JSON_SUFIX:
            dict_from_file = dict(json.load(dict_file))
            return dict_from_file if isinstance(dict_from_file, dict) else {}
        elif file_extansion in YAML_SUFIXES:
            dict_from_file = yaml.safe_load(dict_file)
            return dict_from_file if isinstance(dict_from_file, dict) else {}
        raise ValueError('Incorrect data file: {f}'.format(f=file_path))
