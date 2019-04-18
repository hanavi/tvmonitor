#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup as bs
import re
import pprint
import json
from datetime import datetime
from localshows import check_local


def download_data(showid):

    base_url = "https://www.episodate.com/api"
    cmd = base_url + f"/show-details?q={showid}"

    req = requests.get(cmd)
    if req.status_code == 200:
        return req.json()


def load_data(fname):

    with open(fname) as fd:
        show_data = fd.read()

    show_data = json.loads(show_data)
    return show_data


def save_data(fname, show_data):

    with open(fname, 'w') as fd:
        fd.write(json.dumps(show_data))


def get_last_episode(show_dir, show_file):

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

    fname = 'shows.json'
    with open(fname) as fd:
        data = fd.read()
    show_info = json.loads(data)

    for show, local_info in show_info.items():

        show_id = local_info['id']
        show_dir = local_info['localdir']
        show_file = local_info['json_file']
        show_name = local_info['name']

        print()
        print("-"*79)
        print(f"Checking {show_name}")
        get_last_episode(show_dir, show_file)
        print("-"*79)
        print()

def main():
    check_shows()

    # update_shows()


if __name__ == "__main__":
    main()

