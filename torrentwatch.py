#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pexpect
from subprocess import run, PIPE
from torrentinfo import TorrentInfo


def load_data():
    """Load the data from the torrent server."""

    check_cmd = ['ssh', 'deluge', 'deluge-console', 'info']
    data = run(check_cmd, stdout=PIPE).stdout.decode()

    # with open("output.txt") as fd:
    #     data = fd.read()

    for torrent_string in data.split("\n \n"):
        torrent_info = TorrentInfo(torrent_string)
        if torrent_info.state == "Seeding":
            finish_torrent(torrent_info)


def finish_torrent(torrent):
    """Run the final steps for the torrent."""

    print(torrent)
    print("cleaning up torrent")

    # check_cmd = ['ssh', 'deluge', 'deluge-console', 'info']
    # data = run(check_cmd, stdout=PIPE).stdout.decode()


def main():
    load_data()


if __name__ == "__main__":
    main()

