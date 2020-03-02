#!/usr/bin/env python3

from time import time, sleep
import argparse
import sys
from os import getenv
import subprocess
import re

GRACE_TIME = 5


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


def notify(message="", title="Discipline"):
    subprocess.run(
        ["osascript", "-e", f'display notification "{message}" with title "{title}"']
    )


def is_block_active(whoami):
    start_time = subprocess.run(
        [
            "sudo",
            "-u",
            whoami,
            "defaults",
            "read",
            "org.eyebeam.SelfControl",
            "BlockStartedDate",
        ],
        capture_output=True,
        text=True,
    )
    if start_time.returncode != 0:
        notify(message="Could not get block starting date!", title="Error!")
        exit(1)
    return start_time.stdout != "4001-01-01 00:00:00 +0000\n"


def is_current_SSID_within(list_SSIDs):
    airport_out = subprocess.run(
        [
            "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport",
            "-I",
        ],
        capture_output=True,
        text=True,
    )

    current_SSID = re.findall(" SSID: (.*)", airport_out.stdout)[0]

    for SSID in list_SSIDs:
        if current_SSID == SSID:
            return True
    return False


def compute_block_duration(block_end):
    return 2


def set_block_duration(whoami, minutes):
    result = subprocess.run(
        [
            "sudo",
            "-u",
            whoami,
            "defaults",
            "write",
            "org.eyebeam.SelfControl",
            "BlockDuration",
            "-int",
            str(minutes),
        ]
    )
    if result.returncode != 0:
        notify(message="Could not set block duration!", title="Error!")
        exit(1)


def start_block(whoami):
    my_id = subprocess.run(["id", "-u", whoami], capture_output=True, text=True).stdout[
        :-1
    ]
    result = subprocess.run(
        [
            "sudo",
            "/Applications/SelfControl.app/Contents/MacOS/org.eyebeam.SelfControl",
            my_id,
            "--install",
        ]
    )
    if result.returncode != 0:
        notify(message="Could not start block!", title="Error!")
        exit(1)


if __name__ == "__main__":
    args = parse_args()
    block_end = args.time[0]

    # check for root
    whoami = getenv("USER")
    if whoami is None:
        notify(message="This script must be run as root", title="Error!")
        exit(0)

    # check for block already running
    if is_block_active(whoami):
        notify(message="Block already running!", title="Discipline active")
        exit(0)

    # check SSID condition
    if args.SSID is not None and not is_current_SSID_within(args.SSID):
        exit(0)  # quit silently

    # get duration and check on duration
    minutes = compute_block_duration(block_end)
    if minutes <= 0 or minutes > 12 * 60:
        exit(0)  # quit silently

    # start block
    notify(
        message=f"Start working in {GRACE_TIME} seconds!",
        title=f"Discipline until {block_end}",
    )
    sleep(GRACE_TIME)

    set_block_duration(whoami, minutes)
    start_block(whoami)


# # write down starting time

# # write down end time
