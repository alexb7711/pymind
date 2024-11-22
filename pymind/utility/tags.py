"""!
@file tags.py

@module This module is used to expose the functionality for finding tags.
"""

import re
import logging
from pathlib import Path

logger = logging.getLogger("PYMIND")

##======================================================================================================================
#
def getTags(files: list[str]) -> dict:
    """!
    @brief Retrieve tags from the files

    @param bf List of files to search

    @return A dictionary where the key is the tag found and the item is a list of files where the tag was found.
    """
    tags = {}

    # For each file in the 'build files' list
    logger.debug("TAGS: Searching for tags in files list.")
    for f in files:
        ## Open the build file
        with open(f, "r") as txt:
            ### For each row in the build file
            for l in txt:
                #### Search for tags in the file
                matches = re.findall(r"^<!--\s*:?(.*?):\s*-->", l)

                #### If tags were found
                if matches:
                    #### Create a list of the tags
                    matches = matches[0].split(":")

                    ##### Add the tag to the table of tags
                    tags = __updateTags(f, tags, matches)

                    ##### Continue looking for tags in other files
                    continue

    return tags


##======================================================================================================================
#
def __updateTags(fn: str, tags: dict, matches: list) -> dict:
    """!
    @brief Updates `tags` with the data found in `matches` for the provided `file`

    @param fn Name of the parse file
    @param tags Dictionary of found tags associated with a list of the files in which that tag was found
    @param matches List of tags that were found in a file

    @return Update dictionary of tag => [list of files with tag]
    """
    # Loop through each matched tag found in `fn`
    logger.debug("TAGS: Updating dictionary of tags")
    for m in matches:
        ## If the tag already exists
        if tags.get(m):
            ### Append the tag
            tags[m].append(fn)
        else:
            ### Create a new tag
            tags[m] = [fn]

    return tags
