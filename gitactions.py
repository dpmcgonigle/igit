#! /usr/bin/env python
"""
gitactions.py

    Created: 7/18/2020, by Dan McGonigle

    Purpose: To add, commit, and push everything in the repo
"""
import os
import traceback
from subprocess import Popen, PIPE
from utils import dtstamp, base_dir

print(f"STARTING gitactions.py at {dtstamp()}")

os.chdir(base_dir())

#   Add files
call = "git add ."
proc = Popen(call.split(), stdout=PIPE, stderr=PIPE)
out, err = proc.communicate()

if err:
    print(f"ERROR FROM: '{call}' ; {err}")
    print(
        f"NOTE: Check git version to see if '{call}' behavior is expected, and change if necessary"
    )
if out:
    print(f"CALL: {call}; OUTPUT: {out}")

#   Commit files
call = "git commit"
args = ["-m", f"{dtstamp()} gitactions.py add/commit"]
proc = Popen(call.split() + args, stdout=PIPE, stderr=PIPE)
out, err = proc.communicate()

if err:
    print(f"ERROR FROM: '{call}' ; {err}")
    print(
        f"NOTE: Check git version to see if '{call}' behavior is expected, and change if necessary"
    )
if out:
    print(f"CALL: {call}; OUTPUT: {out}")

#   Push files
call = f"git push"
proc = Popen(call.split(), stdout=PIPE, stderr=PIPE)
out, err = proc.communicate()

if err:
    print(f"ERROR FROM: '{call}' ; {err}")
    print(
        f"NOTE: Check git version to see if '{call}' behavior is expected, and change if necessary"
    )
if out:
    print(f"CALL: {call}; OUTPUT: {out}")
