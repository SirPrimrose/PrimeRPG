#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import hashlib
from pathlib import Path
from typing import List

from primerpg.persistence.dto.file_checksum import FileChecksum
from primerpg.persistence.file_checksum_persistence import get_file_checksum, update_file_checksum, insert_file_checksum

checksums_to_update: List[FileChecksum] = []


def update_checksums():
    for checksum in checksums_to_update:
        if get_file_checksum(checksum.file_name):
            update_file_checksum(checksum)
        else:
            insert_file_checksum(checksum)
    checksums_to_update.clear()


def has_file_changed(file_paths: List[Path]) -> bool:
    """Checks if a file (or it's dependencies) has changed or been created since the last saved check.

    :param file_paths: All file paths to check for changes
    :return: True if the file is new or changed
    """
    for file in file_paths:
        if compare_checksums(file):
            return True
    return False


def compare_checksums(file_path: Path):
    global checksums_to_update
    checksum = get_file_checksum(file_path.name)
    md5 = get_md5(file_path)
    if not checksum:
        checksums_to_update.append(FileChecksum(file_path.name, md5))
        return True
    if checksum.md5_checksum != md5:
        checksum.md5_checksum = md5
        checksums_to_update.append(checksum)
        return True
    return False


def get_md5(file_path: Path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
