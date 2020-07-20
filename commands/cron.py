#! /usr/bin/env python
"""
commands/cron.py

    Created: 7/18/2020, by Dan McGonigle

    Purpose: To provide cron click group commands for igit program
        These commands will interface with the local machine's cron for saving files in config/stash.json to the git repo
"""
import os
import json
import click
from utils import (
    debug,
    info,
    warning,
    error,
    get_crontab,
    get_crontab_template,
    get_crontab_filename,
    verify_cronstring,
    activate_crontab,
    base_dir,
)


@click.command("edit")
@click.pass_context
@click.argument("machine", required=True)
@click.argument("copycron", required=True)
@click.argument("gitcron", required=True)
@click.option("--save", is_flag=True)
def cron_edit(context, machine, copycron, gitcron, save):
    """
    Edit the current crontab
    
    ARGS:\n
    machine             <str> Name of machine to list\n
    copycron            <str> Cron string for copymachine.py\n
    gitcron             <str> Cron string for gitactions.py\n
    OPTIONS:\n
    --save              <boolean flag> Save a copy of the old crontab in crons
    """
    info(
        context,
        f"Editing {machine} cronfile timing for saving files with cron strings {copycron} and {gitcron}, and --save={save}",
    )
    if not verify_cronstring(copycron):
        error(context, f"Unable to parse cron string {copycron} for copymachine.py")
    if not verify_cronstring(gitcron):
        error(context, f"Unable to parse cron string {copycron} for gitactions.py")

    filename = get_crontab_filename()
    copylog = os.path.join(base_dir(), "copymachine.log")
    gitlog = os.path.join(base_dir(), "gitactions.log")
    new_lines = [
        "#  NOTE: Cron will use python version in /usr/bin or similar, so you may need to install click or other modules with something like 'sudo /usr/bin/python3 -m pip install click'",
        f"{copycron} python3 {os.path.join(base_dir(), 'copymachine.py')} --machine {machine.lower()} >> {copylog} 2>&1",
        f"{gitcron} python3 {os.path.join(base_dir(), 'gitactions.py')} >> {gitlog} 2>&1",
    ]

    out, err = get_crontab()
    if err:
        warning(context, f"Unable to get crontab : {err}")

        #   Unable to pull up crontab; default to template
        cron_lines = get_crontab_template()
        cron_lines += new_lines

        info(context, f"Added line:{line}")

        with open(filename, "w") as cronfile:
            for line in cron_lines:
                cronfile.write(line)
        debug(f"Saved cronfile to {filename}")

    elif out:
        out = out.decode("utf-8")
        if save:
            with open(f"{filename}.old", "w") as oldcronfile:
                oldcronfile.write(out)
            debug(context, f"Saved old cronfile to {filename}.old")

        lines = out.split("\n")

        replace_indexes = []
        for index, line in enumerate(lines):
            if any(
                [
                    "copymachine.py" in line,
                    "gitactions.py" in line,
                    "NOTE: Cron will use python" in line,
                    line == "",
                ]
            ):
                replace_indexes.append(index)

        #   Need to iterate through the indexes backwards since popping the front of the list will affect downstream indexes
        for replace_index in replace_indexes[::-1]:
            debug(context, f"Removing the following line:\n{lines[replace_index]}")
            lines.pop(replace_index)

        lines += new_lines
        info(context, f"Added line:{line}")

        with open(filename, "w") as cronfile:
            for line in lines:
                cronfile.write(line + "\n")
        debug(context, f"Saved cronfile to {filename}")

    #   Activate crontab
    out, err = activate_crontab(filename)
    if out:
        info(context, f"CRONTAB ACTIVATION OUTPUT: {out}")
    if err:
        warning(
            context,
            f"CRONTAB ACTIVATION ERROR: {err}; Activate manually with 'crontab filename'",
        )

