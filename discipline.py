#!/usr/bin/env python3

import argparse
import sys
import subprocess


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
        help="List of disciplined WiFi SSIDs",
    )

    if len(sys.argv) == 1:
        arg_parser.print_help(sys.stderr)
        sys.exit(1)

    return arg_parser.parse_args()


def notify(message, title):
    subprocess.run(
        ["osascript", "-e", f'display notification "{message}" with title "{title}"']
    )

def is_block_active():
    start_time = subprocess.run(
        ["defaults", "read", "org.eyebeam.SelfControl", "BlockStartedDate"],
        capture_output=True,
        text=True,
    )
    return start_time.stdout != "4001-01-01 00:00:00 +0000\n"


    )

if __name__ == "__main__":
    args = parse_args()

    if is_block_active():
        notify(message="Block already running!", title="Discipline active")
        exit(0)

# # write down starting time

# # write down end time
