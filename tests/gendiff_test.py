"""Gendiff test modul."""
import json
import os

import pytest

from gendiff.scripts.gendiff import generate_diff


def get_path(file_name: str) -> str:
    """Get abs path to fixture file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def read(file_path: str) -> str:
    """Read the file."""
    with open(file_path, 'r') as f_file:
        f_result = f_file.read()
    return f_result


first_files = [
    'test0file1.json',
    'test1file1.json',
    'test2file1.json',
    'test0file1.yml',
    'test1file1.yml',
    'test2file1.yml',
    'testplain0file1.json',
    'testplain1file1.json',
    'testjsonlish0file1.json',
]

second_files = [
    'test0file2.json',
    'test1file2.json',
    'test2file2.json',
    'test0file2.yml',
    'test1file2.yml',
    'test2file2.yml',
    'testplain0file2.json',
    'testplain1file2.json',
    'testjsonlish0file2.json',
]

expected_files = [
    'expect_json0.txt',
    'expect_json1.txt',
    'expect_json2.txt',
    'expect_yaml0.txt',
    'expect_yaml1.txt',
    'expect_yaml2.txt',
    'expect_plain0.txt',
    'expect_plain1.txt',
    'expect_jsonlish0.txt',
]

formaters = [
    'stylish',
    'stylish',
    'stylish',
    'stylish',
    'stylish',
    'stylish',
    'plain',
    'plain',
    'json',
]

cases = list(range(9))


@pytest.mark.parametrize('case_index', cases)
def test_generate_diff(case_index: int) -> None:
    """Test generate_diff function."""
    f1 = get_path(first_files[case_index])
    f2 = get_path(second_files[case_index])
    expected = read(get_path(expected_files[case_index]))
    formater = formaters[case_index]
    if case_index == 8:
        assert json.loads(generate_diff(f1, f2, formater)) == json.loads(
            expected,
        )
    else:
        assert generate_diff(f1, f2, formater) == expected


if __name__ == '__main__':
    test_generate_diff(5)
