#!/usr/bin/env python
# coding: utf-8

import requests
import json
from datetime import datetime
from localshows import check_local
import structlog
from structlog.stdlib import LoggerFactory
import logging
import click

structlog.configure(logger_factory=LoggerFactory())
log = structlog.get_logger()

debug = log.debug
info = log.info
warn = log.warn


def download_data(show_id):
    """Download show information from website."""

    base_url = "https://www.episodate.com/api"
    cmd = base_url + f"/show-details?q={show_id}"

    req = requests.get(cmd)
    if req.status_code == 200:
        return req.json()

    return {}


def load_data(fname):
    """Load local show info from file."""

    with open(fname) as fd:
        show_data = fd.read()

    show_data = json.loads(show_data)
    return show_data


def save_data(fname, show_data):
    """Save show information."""

    with open(fname, 'w') as fd:
        fd.write(json.dumps(show_data))


def get_last_episode(show_dir, show_file):
    """Print out the last episode information for a given show."""


    show_data = load_data(show_file)

    episodes = show_data['tvShow']['episodes']

    lastshow = ''
    now = datetime.now()
    for epi in episodes:
        show_date = epi['air_date']
        show_date = datetime.fromisoformat(show_date)
        show_id = f"S{epi['season']:02}E{epi['episode']}"

        nextshow = (f"{show_date} {show_id}   {epi['name']}")

        if show_date > now:
            break

        lastshow = nextshow
        lastshow_id = show_id

    if nextshow != lastshow:

        nextshow = "[ ] " + nextshow

        if check_local(lastshow_id, show_dir):
            lastshow = "[x] " + lastshow
        else:
            lastshow = "[ ] " + lastshow

        print("last: ", lastshow)
        print("next: ", nextshow)

    else:
        if check_local(lastshow_id, show_dir):
            lastshow = "[x] " + lastshow
        else:
            lastshow = "[ ] " + lastshow

        print("last: ", lastshow)


def update_shows():
    """Update the information for all of the shows."""

    fname = 'shows.json'
    with open(fname) as fd:
        data = fd.read()

    data = json.loads(data)

    for show, show_info in data.items():
        print(f"updating {show}")
        showid = show_info['id']
        jsonfile = show_info['json_file']
        show_data = download_data(showid)
        save_data(jsonfile, show_data)


def check_shows():
    """Check all of our shows for recent episodes."""

    fname = 'shows.json'
    with open(fname) as fd:
        data = fd.read()
    show_info = json.loads(data)

    for show, local_info in show_info.items():

        show_dir = local_info['localdir']
        show_file = local_info['json_file']
        show_name = local_info['name']

        print()
        print("-"*79)
        print(f"Checking {show_name}")
        get_last_episode(show_dir, show_file)
        print("-"*79)
        print()


@click.command()
@click.option("-d", "--debug", "dbg", is_flag=True, default=False,
              help="Show debugging info")
def main(dbg):

    if dbg is True:
        logging.basicConfig(level=logging.DEBUG)

    else:
        logging.basicConfig(level=logging.WARNING)

    check_shows()

    # update_shows()


if __name__ == "__main__":
    main()
