"""gendiff test modul."""
import os

import pytest

from gendiff.diff_finder import generate_diff


def get_fixture_path(file_name):
    """Get abs path to fixture file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def read(file_path):
    """Read the file."""
    with open(file_path, 'r') as f_file:
        f_result = f_file.read()
    return f_result


answers = read(get_fixture_path('expectation.txt')).rstrip().split('\n\n\n')
cases = list(range(4))


@pytest.mark.parametrize('case_index', cases)
def test_generate_diff(case_index):
    """Test generate_diff function."""
    f1 = get_fixture_path('test{cs}file1.json'.format(cs=case_index))
    f2 = get_fixture_path('test{cs}file2.json'.format(cs=case_index))
    expected = answers[case_index]
    assert generate_diff(f1, f2) == expected
