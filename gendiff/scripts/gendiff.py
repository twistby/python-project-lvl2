"""Gendiff script."""
import argparse


def main():
    """Run main function."""
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    args = parser.parse_args()


if __name__ == '__main__':
    main()
