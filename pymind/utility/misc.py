"""!
@file misc.py

@module This module exposes miscellaneous functions.
"""

from pathlib import Path


##======================================================================================================================
#
def recursiveDelete(directory: Path):
    """!
    @brief Recursively delete files from the starting point `directory`

    @param directory Path to the directory to recursively delete
    """
    for path in directory.rglob("*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            recursiveDelete(path)
            path.rmdir()

    return
