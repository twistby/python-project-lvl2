"""gendiff test modul."""
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


cases = list(range(3))


@pytest.mark.parametrize('case_index', cases)
def test_generate_diff(case_index: int) -> None:
    """Test generate_diff function."""
    f1 = get_path('test{cs}file1.json'.format(cs=case_index))
    f2 = get_path('test{cs}file2.json'.format(cs=case_index))
    expected = read(get_path('expect_json{cs}.txt'.format(cs=case_index)))
    assert generate_diff(f1, f2) == expected
    f1 = get_path('test{cs}file1.yml'.format(cs=case_index))
    f2 = get_path('test{cs}file2.yml'.format(cs=case_index))
    expected = read(get_path('expect_yaml{cs}.txt'.format(cs=case_index)))
    assert generate_diff(f1, f2) == expected
    if case_index < 2:
        f1 = get_path('testplain{cs}file1.json'.format(cs=case_index))
        f2 = get_path('testplain{cs}file2.json'.format(cs=case_index))
        expected = read(get_path('expect_plain{cs}.txt'.format(cs=case_index)))
        assert generate_diff(f1, f2, 'plain') == expected
    if case_index == 0:
        f1 = get_path('testjsonlish{cs}file1.json'.format(cs=case_index))
        f2 = get_path('testjsonlish{cs}file2.json'.format(cs=case_index))
        expected = json.loads(
            read(get_path('expect_jsonlish{cs}.txt'.format(cs=case_index))),
        )
        assert json.loads(generate_diff(f1, f2, 'json')) == expected
