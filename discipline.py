#!/usr/bin/env python3

import argparse
import sys

def parse_args():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "-u",
        "--until",
        dest="time",
        action="store",
        help="Block end time [hh:mm]",
        nargs=1,
    )
    arg_parser.add_argument(
        "-n",
        "--network",
        dest="SSID",
        action="append",
        help="List of applicable WiFi SSIDs",
    )

    if len(sys.argv) == 1:
        arg_parser.print_help(sys.stderr)
        sys.exit(1)

    return arg_parser.parse_args()


if __name__ == "__main__":
    args = parse_args()


# # write down end time
