"""gendiff test modul."""
import os

import pytest

from gendiff.diff_finder import generate_diff


def get_fixture_path(file_name: str) -> str:
    """Get abs path to fixture file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def read(file_path: str) -> str:
    """Read the file."""
    with open(file_path, 'r') as f_file:
        f_result = f_file.read()
    return f_result


# expected data
json_data = read(get_fixture_path('expect_json.txt')).rstrip().split('\n\n\n')
yaml_data = read(get_fixture_path('expect_yaml.txt')).rstrip().split('\n\n\n')
cases_json = list(range(4))
cases_yaml = list(range(2))


@pytest.mark.parametrize('case_index', cases_json)
def test_generate_diff_json(case_index: int) -> None:
    """Test generate_diff function with json files."""
    f1 = get_fixture_path('test{cs}file1.json'.format(cs=case_index))
    f2 = get_fixture_path('test{cs}file2.json'.format(cs=case_index))
    expected = json_data[case_index]
    assert generate_diff(f1, f2) == expected


@pytest.mark.parametrize('case_index', cases_yaml)
def test_generate_diff_yaml(case_index: int) -> None:
    """Test generate_diff function with yaml files."""
    f1 = get_fixture_path('test{cs}file1.yml'.format(cs=case_index))
    f2 = get_fixture_path('test{cs}file2.yml'.format(cs=case_index))
    expected = yaml_data[case_index]
    assert generate_diff(f1, f2) == expected
