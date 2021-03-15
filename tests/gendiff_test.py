"""gendiff test modul."""
from gendiff.diff_finder import generate_diff


def test_generate_diff():
    """Test generate_diff function."""
    assert generate_diff('file1.json', 'file2.json') == 5
