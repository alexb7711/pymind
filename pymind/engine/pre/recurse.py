"""!
@file recurse.py
@package Recursively search files in directories to create sub-page
"""

import logging
import sys
from pathlib import Path

from pymind import utility
from pymind.utility.modfile import appendFile
from pymind.utility.search import recursiveSearch

logger = logging.getLogger("PYMIND")

##======================================================================================================================
# CONSTANTS

VERSION = "0.0.1"


##======================================================================================================================
#
def main(**kwargs) -> int:
    """!
    @brief Executes the referenced in functionally.

    @param kwargs["input"] Input directory path
    @param kwargs["var_p"] Path to cached variables

    @return True if successful, False if failed
    """
    # Success flag
    success = True

    # Parse the input arguments
    options = utility.misc.parseInput(VERSION)

    # If the input or output directory were not provided
    if (
        not options["input"]
        or not options["output"]
        or not options["name"]
        or not options["var_p"]
    ):
        ## Fail the file creation
        return False

    # Retrieve the list of files and tags
    var = utility.cache.unPickleVar(options["var_p"], options["name"])

    # Write the string to disk
    success = __search_for_sub_wiki(Path(options["input"]))
    sys.exit(not success)
    return


##======================================================================================================================
#
def __search_for_sub_wiki(input: Path) -> bool:
    """!
    @brief List all the files in a directory

    @return True if successful, False otherwise
    """
    # Create a list of files and directories with the same name in the
    # cache directory
    # for x in input.iterdir(): print(x.with_suffix(''))
    return True

    sub_wikis = [
        x.name
        for x in input.iterdir()
        if x.is_file()
        and x.with_suffex("").stem.is_dir()
        and file.name == directory_path.name
    ]

    print(sub_wikis)
    return True

    # For each sub wiki found
    for sw in sub_wikis:
        ## Create a list of files for each match
        content = recurse(sw)

        ## Populate the top level file with the wiki information
        __populate_file()
    return True


##======================================================================================================================
#
def __recurse(input: Path) -> list:
    """!
    @brief List all the files in a directory

    @return List of file names
    """
    return []


##======================================================================================================================
#
def __populate_file() -> bool:
    """!"""
    return


########################################################################################################################

if __name__ == "__main__":  # pragma: no cover
    # Support running module as a command line command.
    #     python -m markdown [options] [args]
    main()
