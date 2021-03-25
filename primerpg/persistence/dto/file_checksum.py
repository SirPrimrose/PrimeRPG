#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class FileChecksum:
    def __init__(self, file_name: str, md5_checksum: str):
        self.file_name = file_name
        self.md5_checksum = md5_checksum

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
