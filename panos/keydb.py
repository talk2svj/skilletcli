from pathlib import Path
import os
import json


class KeyDB:
    """
    Maintains a mapping of Device to Apikey in the users home directory.
    """
    def __init__(self, fn):
        self.filename = fn
        self.enabled = False
        self.keys = {}
        self.get_creds_file()

    def enable(self):
        self.enabled = True

    def get_creds_file(self):
        filename = self.filename

        home = str(Path.home())
        filepath = home + os.sep + filename
        self.path = filepath
        if not os.path.isfile(filepath):
            return False

        j = json.load(open(filepath))
        self.keys = j
        return j

    def lookup(self, device):
        if device in self.keys:
            return self.keys[device]

    def add_key(self, device, key):
        if not self.enabled:
            return
        self.keys[device] = key
        fh = open(self.path, "w")
        json.dump(self.keys, fh)
        fh.close()
        os.chmod(self.path, 0o400)

    def reinit(self):
        self.keys = {}
        fh = open(self.path, "w")
        json.dump(self.keys, fh)
        fh.close()
        os.chmod(self.path, 400)