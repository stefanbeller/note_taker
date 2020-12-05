#!/usr/bin/env python3


import argparse

from pytest import NoteTaking

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A CLI for note taking")
    parser.add_argument(
        "-l",
        "--list",
        action="store_const",
        dest="cmd",
        const="list",
        help="List all notes"
    )
    parser.add_argument(
        "-e",
        "--exit",
        action='store_const',
        dest="cmd",
        const="exit",
        help="Exit the whole thing"
    )
    args = parser.parse_args()
    print(args.cmd)
    if args.cmd == "list":
        NoteTaking().list_all_notes()