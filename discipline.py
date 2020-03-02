#!/usr/bin/env python3

import time
from datetime import datetime
import argparse
import os, sys
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
    raise NotImplementedError("notification do not work at the moment")
    # subprocess.run(
    #     [
    #         "sudo",
    #         "-u#501", # 501 should be the user id of the default user
    #         "reattach-to-user-namespace",
    #         "osascript",
    #         "-e",
    #         f'display notification "{message}" with title "{title}"',
    #     ]
    # )


def is_block_active():
    start_time = subprocess.run(
        [
            "sudo",
            "-u#501",  # 501 should be the user id of the default user
            "defaults",
            "read",
            "org.eyebeam.SelfControl",
            "BlockStartedDate",
        ],
        capture_output=True,
        text=True,
    )
    if start_time.returncode != 0:
        # notify(message="Could not get block starting date!", title="Error!")
        sys.exit(1)

    if start_time.stdout == "4001-01-01 00:00:00 +0000\n":
        return False
    else:
        return True


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
    assert len(block_end) == 5, "Time should be in hh:mm format"
    assert block_end[2] == ":", "Time should be in hh:mm format"

    h = int(block_end.split(":")[0])
    m = int(block_end.split(":")[1])
    assert 0 <= h <= 23
    assert 0 <= m <= 59

    time_end = h * 60 + m
    time_now = datetime.now().hour * 60 + datetime.now().minute

    duration = time_end - time_now

    if duration < 0:
        duration += 24 * 60

    return duration


def set_block_duration(minutes):
    result = subprocess.run(
        [
            "sudo",
            "-u#501",  # 501 should be the user id of the default user
            "defaults",
            "write",
            "org.eyebeam.SelfControl",
            "BlockDuration",
            "-int",
            str(minutes),
        ]
    )
    if result.returncode != 0:
        # notify(message="Could not set block duration!", title="Error!")
        exit(1)


def start_block():
    # user_id = subprocess.run(
    #     ["id", "-u", USER_NAME], capture_output=True, text=True
    # ).stdout[:-1]
    user_id = 501

    result = subprocess.run(
        [
            "/Applications/SelfControl.app/Contents/MacOS/org.eyebeam.SelfControl",
            user_id,
            "--install",
        ]
    )
    if result.returncode != 0:
        # notify(message="Could not start block!", title="Error!")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()
    block_end = args.time[0]

    # check for root
    if os.geteuid() != 0:
        # notify(message="This script must be run as root", title="Error!")
        sys.exit(1)

    # check for block already running
    if is_block_active():
        # notify(message="Block already running!", title="Discipline active")
        sys.exit(0)

    # check SSID condition
    if args.SSID is not None and not is_current_SSID_within(args.SSID):
        sys.exit(0)  # quit silently

    # get duration and check on duration
    minutes = compute_block_duration(block_end)
    if minutes > 12 * 60:
        sys.exit(0)  # quit silently

    # start block
    # notify(
    #     message=f"Start working in {GRACE_TIME} seconds!",
    #     title=f"Discipline until {block_end}",
    # )
    # time.sleep(GRACE_TIME)

    set_block_duration(minutes)
    start_block()
