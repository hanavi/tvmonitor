#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import requests
from collections import namedtuple
import pexpect
from subprocess import run
from bs4 import BeautifulSoup as bs
import re
import datetime
import pathlib
import json


def run_search(query):
    """Run search on TPB and return the first page."""


    # Use Tor to keep things private
    url = "http://uj3wazyk5u4hnvtk.onion/search/{}/0/99/0".format(query)
    proxies = { 'http': "socks5h://10.1.0.11:9100",
                'https': "socks5h://10.1.0.11:9100" }

    try:
        page = requests.get(url, proxies=proxies)
    except requests.exceptions.ConnectionError:
        sys.exit("Failed to connect to TPB...")

    # Need to do some more error handling
    if page.status_code == 200:
        return page.content


def parse_search_results(html=None):
    """Parse the PB search results page."""

    if html is None:
        html = sys.stdin.read()

    soup = bs(html, "html.parser")
    lines = soup.find_all("tr")

    Magnet = namedtuple("Magnet", "id description url")

    i = 0
    magnets = []
    for line in lines:
        links = line.find_all('a')
        if len(links) > 3:
            description = links[2].text
            url = links[3].get('href')
            if url[:6] == "magnet":
                i += 1
                magnets.append(Magnet(i, description, url))
    return magnets


def choose_magnets(magnets):
    """Print the list of returned magnet links for selection."""

    choice = None
    while choice != 'q':

        print()
        print("="*79)
        print("Select a torrent to download")
        print("-"*79)

        for magnet in magnets:
            print("{id:2d}. {description}".format(**(magnet._asdict())))

        print("-"*79)

        choice = input("Select a file to download: ")

        try:
            # Process our selection
            if choice != 'q':

                choice = int(choice)
                for magnet in magnets:

                    if magnet.id == choice:

                        print("Sending: {}".format(magnet.description))
                        send_to_deluge(magnet.url)

            print("="*79)
            print()

        except ValueError:

            print("Please Try Again")


def get_running_torrents():
    output = run(["ssh", "deluge", "deluge-console", "info"],
                 capture_output=True)

    output = output.stdout.decode()
    torrent_list = output.split("\n \n")
    torrent_info = parse_torrent_info(torrent_list)

    return torrent_info


def parse_torrent_info(torrent_list):

    torrent_info = []
    TorrentData = namedtuple("TorrentData", ['name', 'id', 'state'])


    for torrent in torrent_list:
        for line in torrent.split("\n"):
            if re.match("Name", line):
                name = line.split(":")[1].strip()
            if re.match("ID", line):
                torrent_id = line.split(":")[1].strip()
            if re.match("State", line):
                state = line.split(":")[1].strip()
        torrent_info.append(torrent_id)

    return torrent_info


def auto_download(show="Young Sheldon", episode="S02E19"):

    m = re.compile(episode)

    search = show + " " + episode
    page = run_search(search)
    magnets = parse_search_results(page)

    for magnet in magnets:
        description = magnet.description
        url = magnet.url
        if m.search(description):
            start_torrent_info = get_running_torrents()
            print(f"Found Match: {description}")
            send_to_deluge(url)
            end_torrent_info = get_running_torrents()
            break

    date = datetime.datetime.now()
    date = date.strftime("%Y_%m_%d")
    for torrent in end_torrent_info:
        if not torrent in start_torrent_info:
            fname = f"downloading/{date}.json"
            output = {"show": show, "episode": episode, "id": torrent }
            if pathlib.Path(fname).is_file():
                # Load the existing data first
                with open(fname, "r") as fd:
                    data  = json.loads(fd.read())

                # Output new data
                data.append(output)
                with open(fname, "w") as fd:
                    fd.write(json.dumps(data))
            else:
                with open(fname, "w") as fd:
                    fd.write(json.dumps([output], indent=4))



def send_to_deluge(magnet):
    """Log into the Deluge server and send the magnet link."""

    # This is so we can log in to the server
    if 'SSH_AUTH_SOCK' not in os.environ:

        print("Please start SSH agent first")
        sys.exit()

    else:

        server = "deluge"
        child = pexpect.spawn("/usr/bin/ssh", [server])
        child.expect("james@torrent:~\$ ")
        child.sendline("deluge-console add '{}'\r".format(magnet))
        child.expect("james@torrent:~\$ ")
        child.close()


def main():
    """Run a search on TPB and send links for download."""

    auto_download()
    # Make sure we actually have a search term
    # if len(sys.argv) > 1:

    #     search = " ".join(sys.argv[1:])
    #     page = run_search(search)
    #     magnets = parse_search_results(page)
    #     choose_magnets(magnets)


if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
        print()
