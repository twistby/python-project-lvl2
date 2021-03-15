"""Making parser and return arguments."""
import argparse


def make_parser():
    """Make argparse parser."""
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    return parser


def get_args():
    """Return arguments."""
    parser = make_parser()
    return parser.parse_args()
