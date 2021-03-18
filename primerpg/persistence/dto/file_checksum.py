#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class FileChecksum:
    def __init__(self, file_name: str, md5_checksum: str):
        self.file_name = file_name
        self.md5_checksum = md5_checksum
