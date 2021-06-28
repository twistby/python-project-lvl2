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


# expected data
json_data = read(get_path('expect_json.txt')).rstrip().split('\n\n\n')
yaml_data = read(get_path('expect_yaml.txt')).rstrip().split('\n\n\n')
json_data_default = read(get_path('expect_json_default.txt')).rstrip().split(
    '\n\n\n',
)
json_data_plain = read(get_path('expect_plain.txt')).rstrip().split('\n\n\n')
json_data_jsonlish = read(get_path('expect_jsonlish.txt')).rstrip().split(
    '\n\n\n',
)

cases_json = list(range(3))
cases_yaml = list(range(3))
cases_plain = list(range(2))
cases_jsonlish = list(range(1))


@pytest.mark.parametrize('case_index', cases_json)
def test_generate_diff_json_yaml(case_index: int) -> None:
    """Test generate_diff function with json files."""
    f1 = get_path('test{cs}file1.json'.format(cs=case_index))
    f2 = get_path('test{cs}file2.json'.format(cs=case_index))
    expected = json_data[case_index]
    assert generate_diff(f1, f2) == expected
    f1 = get_path('test{cs}file1.yml'.format(cs=case_index))
    f2 = get_path('test{cs}file2.yml'.format(cs=case_index))
    expected = yaml_data[case_index]
    assert generate_diff(f1, f2) == expected


@pytest.mark.parametrize('case_index', cases_plain)
def test_generate_diff_plain(case_index: int) -> None:
    """Test generate_diff function with plain template."""
    f1 = get_path('testplain{cs}file1.json'.format(cs=case_index))
    f2 = get_path('testplain{cs}file2.json'.format(cs=case_index))
    expected = json_data_plain[case_index]
    assert generate_diff(f1, f2, 'plain') == expected


@pytest.mark.parametrize('case_index', cases_jsonlish)
def test_generate_diff_jsonlish(case_index: int) -> None:
    """Test generate_diff function with jsonlish template."""
    f1 = get_path('testjsonlish{cs}file1.json'.format(cs=case_index))
    f2 = get_path('testjsonlish{cs}file2.json'.format(cs=case_index))
    expected = json.loads(json_data_jsonlish[0])
    assert json.loads(generate_diff(f1, f2, 'json')) == expected
