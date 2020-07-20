#! /usr/bin/env python
"""
commands/stash.py

    Created: 7/18/2020, by Dan McGonigle

    Purpose: To provide stash click group commands for igit program
        These commands will interface with config/stash.json for saving files into the git repository
"""
import os
import json
import click
from utils import debug, info, warning, error, load_stash, save_stash, ask


@click.command("create")
@click.pass_context
@click.argument("machine", required=True)
def stash_create(context, machine):
    """
    Add machine to config/stash.json
    
    ARGS:\n
    machine             <str> Name of machine to add to stash
    """
    info(context, f"Adding {machine} to config/stash.json")
    stash = load_stash()
    if machine not in stash.keys():
        stash[machine] = {}
        save_stash(stash)
    else:
        warning(context, f"Machine {machine} already exists in stash.")


@click.command("add")
@click.pass_context
@click.argument("machine", required=True)
@click.argument("filenames", type=click.Path(exists=True), nargs=-1, required=True)
@click.option("--force", is_flag=True)
@click.option("--files-only", is_flag=True)
@click.option("--dest", type=str, default="")
def stash_add(context, machine, filenames, force, files_only, dest):
    """
    Add filenames to config/stash.json
    
    ARGS:\n
    machine             <str> Name of machine to add to\n
    filenames           <str> Filename(s) to add (space-separated)\n
    OPTIONS:\n
    --force             <boolean flag> Force adding file if size (>1MB) or directory\n
    --files-only        <boolean flag> Only add files
    --dest              <str> Destination within git file structure
    """
    info(
        context,
        f"Adding {filenames} to {machine} config/stash.json with force={force}, files_only {files_only}, and dest={dest}",
    )
    stash = load_stash()
    if machine.lower() not in stash.keys():
        error(context, f"Machine {machine.lower()} not in stash.keys() {stash.keys()}")
        exit(1)
    for filename in filenames:
        filepath = os.path.abspath(filename)
        if filepath in stash[machine.lower()]:
            warning(context, f"File {filepath} already in stash")
        else:
            filesize = os.stat(filepath).st_size / 2 ** 20
            if os.path.isdir(filepath):
                if files_only:
                    debug(context, f"Not adding directory {filepath}; files_only")
                    continue
                elif force:
                    debug(context, f"Force adding directory {filepath}")
                elif not ask(f"{filepath} is a directory;  Add anyways? (y/yes) "):
                    debug(context, f"Not adding directory {filepath}")
                    continue
            elif filesize > 1.0:  # 1MB
                if force:
                    debug(context, f"Force adding {filepath}, size {filesize:.3f} MB")
                elif not ask(
                    f"File size for {filepath} : {filesize} MB; Add anyways? (y/yes) "
                ):
                    debug(context, f"Not adding {filepath}")
                    continue
            stash[machine.lower()][filepath] = dest
            debug(context, f"Added {filepath} to stash, with dest {dest}")

    debug(context, f"Saving changes to stash")
    save_stash(stash)


@click.command("list")
@click.pass_context
@click.argument("machine", default="all")
def stash_list(context, machine):
    """
    List files from config/stash.json
    
    ARGS:\n
    machine             <str> Name of machine to list, or 'all'
    """
    info(context, f"Listing files from config/stash.json for machine: {machine}")
    stash = load_stash()
    if machine.lower() == "all":
        info(context, json.dumps(stash, indent=4))
    elif machine.lower() in stash.keys():
        info(context, json.dumps(stash[machine.lower()], indent=4))
    else:
        error(context, f"Machine {machine} not found in stash.keys(): {stash.keys()}")
        exit(1)


@click.command("clear")
@click.pass_context
@click.argument("machine", required=True)
def stash_clear(context, machine):
    """
    Clear files from config/stash.json
    
    ARGS:\n
    machine             <str> Name of machine to list, or 'all'
    """
    info(context, f"Clearing files from config/stash.json for machine: {machine}")
    stash = load_stash()
    if machine.lower() == "all":
        save_stash({})
    elif machine.lower() in stash.keys():
        stash[machine.lower()] = {}
        save_stash(stash)
    else:
        error(context, f"Machine {machine} not found in stash.keys(): {stash.keys()}")
        exit(1)


@click.command("remove")
@click.pass_context
@click.argument("machine", required=True)
@click.argument("filenames", type=click.Path(exists=True), nargs=-1, required=True)
def stash_clear(context, machine, filenames):
    """
    Remove specific files from config/stash.json
    
    ARGS:\n
    machine             <str> Name of machine to list\n
    filenames           <str> Filename(s) to add (space-separated)
    """
    info(
        context,
        f"Removing files {filenames} from config/stash.json for machine: {machine}",
    )
    stash = load_stash()
    if machine.lower() not in stash.keys():
        error(context, f"Machine {machine} not found in stash.keys(): {stash.keys()}")
        exit(1)

    for filename in filenames:
        filepath = os.path.abspath(filename)
        if filepath in stash[machine.lower()]:
            del stash[machine.lower()][filepath]
            debug(context, f"Deleted {filepath} from {machine.lower()}")
        else:
            warning(context, f"File {filepath} not in {machine.lower()}")

    debug(context, f"Saving changes to stash")
    save_stash(stash)

