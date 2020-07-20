#! /usr/bin/env python
"""
copymachine.py

    Created: 7/18/2020, by Dan McGonigle

    Purpose: To copy the files in config/stash.json into the appropriate save directory
"""
import os
import shutil
import argparse
import traceback
from utils import load_stash, dtstamp, base_dir

parser = argparse.ArgumentParser()
parser.add_argument(
    "--machine",
    required=True,
    type=str,
    help="Name of machine; should be a key in config/stash.json",
)
args = parser.parse_args()

print(f"STARTING copymachine.py at {dtstamp()}")
stash = load_stash()
assert (
    args.machine.lower() in stash.keys()
), f"{args.machine.lower()} not in stash.keys() {stash.keys()}"

os.makedirs(os.path.join(base_dir(), args.machine.lower()), exist_ok=True)

for filename, dest in stash[args.machine.lower()].items():
    try:
        os.makedirs(os.path.join(base_dir(), args.machine.lower(), dest), exist_ok=True)
        if os.path.isdir(filename):
            dest = os.path.join(
                base_dir(), args.machine.lower(), dest, os.path.basename(filename)
            )
            # print(f"Copying from {filename} to {dest}")
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(filename, dest)
        elif os.path.isfile(filename):
            dest = os.path.join(
                base_dir(), args.machine.lower(), dest, os.path.basename(filename)
            )
            # print(f"Copying from {filename} to {dest}")
            shutil.copy2(filename, dest)
        else:
            print(f"WARNING: {filename} is neither a file or a directory")
    except Exception as err:
        print(
            f"ERROR: Unable to copy {filename} to {os.path.join(base_dir(), args.machine.lower(), dest, os.path.basename(filename))} : {err}"
        )
        print(f"FULL TRACEBACK : {traceback.format_exc()}")
