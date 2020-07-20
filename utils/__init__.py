#! /usr/bin/env python
"""
utils/__init__.py

    Created: 7/18/2020, by Dan McGonigle

    Purpose: To provide utility functions for igit program
"""
import os
import re
import json
import click
from datetime import datetime
from subprocess import Popen, PIPE


def dtstamp():
    """ Return string datetime """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def dtfile():
    """ Return string datetime that can be used in filename """
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def get_logging_level(level):
    """ Return numeric logging level """
    return {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40}[level]


def debug(context, message):
    """ Print a debugging statement """
    if get_logging_level("DEBUG") >= get_logging_level(context.obj["level"]):
        click.echo(f"[DEBUG][{dtstamp()}] -- {message}")


def info(context, message):
    """ Print a debugging statement """
    if get_logging_level("INFO") >= get_logging_level(context.obj["level"]):
        click.echo(f"[INFO][{dtstamp()}] -- {message}")


def warning(context, message):
    """ Print a debugging statement """
    if get_logging_level("WARNING") >= get_logging_level(context.obj["level"]):
        click.echo(f"[WARNING][{dtstamp()}] -- {message}")


def error(context, message):
    """ Print a debugging statement """
    if get_logging_level("ERROR") >= get_logging_level(context.obj["level"]):
        click.echo(f"[ERROR][{dtstamp()}] -- {message}")


def base_dir():
    """ Return base directory for igit """
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def stash_path():
    """ Return the path of the stash file. """
    return os.path.join(base_dir(), "config", "stash.json")


def load_stash():
    """ Return the dictionary from the json stash file """
    if not os.path.exists(stash_path()):
        json.dump({}, open(stash_path(), "w"), indent=4)
    return json.load(open(stash_path(), "r"))


def save_stash(stash):
    """ Save the dictionary stash """
    json.dump(stash, open(stash_path(), "w"), indent=4)


def ask(question):
    """ Ask a yes/no question """
    answer = input(question)
    return answer.lower() in [
        "y",
        "yes",
        "yeah",
        "yep",
        "true",
        "t",
        "1",
    ]


def get_crontab():
    """ Returns crontab -l output and error """
    proc = Popen(["crontab", "-l"], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return out, err


def get_crontab_template():
    """ Returns crontab template """
    return open(os.path.join(base_dir(), "crons", "template.cron"), "r").readlines()


def get_crontab_filename():
    """ Returns crontab filename based on datetime """
    return os.path.join(base_dir(), "crons", f"{dtfile()}.cron")


def activate_crontab(filename):
    """ Activate crontab for a given file """
    proc = Popen(["crontab", filename], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return out, err


def verify_cronstring(cronstring, hours=0, minutes=0):
    """ Verify valid cron string """
    #   (mins, hrs, dom, mon, dow)
    cron_fields = cronstring.split()
    for field in cron_fields:
        #   Can be '*', '<number>' '*/<number>'
        if not re.search(r"^\*$|^[0-9]{1,2}$|^\*/[0-9]{1,2}$", field):
            return False
    return True

