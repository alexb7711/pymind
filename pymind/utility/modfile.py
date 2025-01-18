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
    logger.debug(f"FILE: Replacing {key} with {text}")
    with open(file, "r+") as f:
        # Retrieve the current content of the file
        file_content = f.read()

        # Replace the text
        file_content = file_content.replace(key, text)

        # Write the text back into the file
        f.seek(0)
        f.write(file_content)
        f.truncate()

    return

##======================================================================================================================
#
def multipleStrReplace(s: str, replacements: dict):
    """!
    @brief Perform multiple text replacements in a string.

    @param s Original text string
    @param replacements Dictionary of current and new sub-strings

    @return
    Updated string where the current sub-strings have been replaced with the new sub-strings
    """
    for old, new in replacements.items():
        s = s.replace(old, new)

    return s

##======================================================================================================================
#
def removeLinesMatchingRegex(filename: Path, pattern: str):
    import re

    # Compile the regex pattern
    compiled_pattern = re.compile(pattern)

    # Open the file for reading and a new file for writing
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Filter out lines that match the regex pattern
    filtered_lines = [line for line in lines if not compiled_pattern.search(line)]

    # Write the filtered lines back to the file
    with open(filename, 'w') as file:
        file.writelines(filtered_lines)

    return
