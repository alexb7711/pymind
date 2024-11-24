"""!
@file modfile.py

@module This module exposes various utility functions to make modifying files easier.
"""

import logging
from pathlib import Path

logger = logging.getLogger("PYMIND")


##======================================================================================================================
#
def appendFile(file: Path, text: str):
    """!@brief Write text to the end of a file.

    @param file Path to the file
    @param text Text to append to the file
    """
    logger.debug(f"FILE: Appending {file} with text")
    with open(file, "r+") as f:
        # Retrieve the current content of the file
        file_content = f.read()

    with open(file, "a") as f:
        # Append text to the file
        f.write(text)

    return


##======================================================================================================================
#
def prependFile(file: Path, text: str):
    """!@brief Write text to the beginning of a file.

    @param file Path to the file
    @param text Text to prepend to the file
    """
    logger.debug(f"FILE: Prepending {file} with text")
    with open(file, "r+") as f:
        # Retrieve the current content of the file
        file_content = f.read()

        # Prepend text to the file
        f.seek(0)
        f.write(text + file_content)


##======================================================================================================================
#
def replaceText(file: Path, key: str, text: str):
    """!@brief Search and replace text within a file

    @param file Path to the file
    @param key Text to search for in the file
    @param text Text to replace `key` in the file
    """
    logger.debug(f"FILE: Prepending {file} with text")
    with open(file, "r+") as f:
        # Retrieve the current content of the file
        file_content = f.read()

        # Replace the text
        file_content = file_content.replace(key, text)

        # Write the text back into the file
        f.seek(0)
        f.write(file_content)

    return
