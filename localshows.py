#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pathlib
import re


def check_local(showid, show_dir):

    local_shows = get_shows(show_dir)
    if showid.upper() in local_shows:
        return True

    return False


def get_shows(show_dir):

    localdir = "/mnt/raid/media/Shows"

    p = pathlib.Path(localdir)
    path = p / show_dir

    if not path.exists():
        return []

    shows = []
    season_fmt = re.compile("season[0-9][0-9]")
    episode_fmt = re.compile(".*([sS][0-9]+[eE][0-9]+).*")

    for fname in path.glob("**/*"):
        matches = episode_fmt.match(str(fname))
        if matches is not None:
            shows.append(matches.group(1).upper())
    return shows


def main():
    check_local()


if __name__ == "__main__":
    main()

