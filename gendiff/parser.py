"""Making parser and return arguments."""
import argparse


def make_parser(first_formater, second_formater, third_formater):
    """Make argparse parser."""
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f',
        '--format',
        help='set format of output',
        choices=[first_formater, second_formater, third_formater],
    )
    return parser


def get_args(first_formater, second_formater, third_formater):
    """Return arguments."""
    parser = make_parser(first_formater, second_formater, third_formater)
    return parser.parse_args()
