"""Making parser and return arguments."""
import argparse


def make_parser(formaters: list):
    """Make argparse parser."""
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f',
        '--format',
        help='set format of output',
        choices=formaters,
        default=formaters[0],
    )
    return parser


def get_args(formaters: list):
    """Return arguments."""
    parser = make_parser(formaters)
    return parser.parse_args()
