class TorrentInfo():
    """Class to hold torrent info from torrent server."""

    def __init__(self, input_string):

        # Set some defaults
        self.id = None
        self.name = None
        self.state = None

        # Parse the string to set the actual values
        self.parse_input(input_string)


    def parse_input(self, input_string):
        """Parse the input string and pull out the data we are interested in.
        """
        for line in input_string.split("\n"):
            if line[:4] == 'Name':
                self.name = line[6:]
            elif line[:2] == 'ID':
                self.id = line[4:]
            elif line[:5] == 'State':
                self.state = line.split(" ")[1]


    def __repr__(self):

        output = f"id: {self.id}\n"
        output += f"name: {self.name}\n"
        output += f"state: {self.state}"

        return output
