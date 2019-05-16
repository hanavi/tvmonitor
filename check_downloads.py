#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import json
from subprocess import run
import re

def check_torrent_status(torrentid):

    cmd = ["ssh", "deluge", "deluge-console", "info", torrentid]
    output = run(cmd, capture_output=True)
    output = output.stdout.decode()
    output = output.split("\n")
    for line in output:
        if re.match("State: Seeding", line):
            return True
    return False

def remove_torrent(torrentid):

    cmd = ["ssh", "deluge", "deluge-console", "rm", torrentid]
    run(cmd)

def move_torrent(torrent_info):
    print("Not working yet")


def main():

    p = pathlib.Path("downloading")
    for fname in p.glob("*.json"):

        with open(fname, "r") as fd:
            data = json.loads(fd.read())

        for line in data:
            if(check_torrent_status(line['id'])):

                remove_torrent(line['id'])
                move_torrent(line)


if __name__ == "__main__":
    main()

