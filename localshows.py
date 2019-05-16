# -*- coding: utf-8 -*-

import pathlib
import re


def check_local(showid, show_dir):
    """Check to see if a show already exists."""

    local_shows = get_shows(show_dir)
    if showid.upper() in local_shows:
        return True

    return False


def get_shows(show_dir):
    """Get local show list."""

    localdir = "/mnt/raid/media/Shows"

    p = pathlib.Path(localdir)
    path = p / show_dir

    if not path.exists():
        return []

    shows = []
    episode_fmt = re.compile(".*([sS][0-9]+[eE][0-9]+).*", flags=re.IGNORECASE)

    for fname in path.glob("**/*"):
        matches = episode_fmt.match(str(fname))
        if matches is not None:
            shows.append(matches.group(1).upper())
    return shows
