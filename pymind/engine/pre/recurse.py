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
    success = __search_for_sub_wiki(Path(options["input"]), Path(options["output"]))

    sys.exit(not success)

    return


##======================================================================================================================
#
def __search_for_sub_wiki(input: Path, output: Path) -> bool:
    """!
    @brief List all the files in a directory

    @param input
    @param output

    @return True if successful, False otherwise
    """
    # Create a list of files and directories with the same name in the
    # cache directory
    sub_wikis = [
        x.with_suffix("")
        for x in input.iterdir()
        if x.is_file() and x.with_suffix("").is_dir()
    ]

    # For each sub wiki found
    for sw in sub_wikis:
        ## Create a list of files for each match
        sw_files = [x for x in sw.rglob("*") if x.is_file()]

        ## Populate the top level file with the wiki information
        success = __populate_file(sw, sw_files, input, output)

    return success


##======================================================================================================================
#
def __populate_file(sw: Path, sw_files: list, input: Path, output: Path) -> str:
    """!
    @brief Populate the top-level file with the content of the sub-wiki.

    @param sw Path to the top-level sub-wiki
    @param sw_files Files found in the sub-wiki
    @param input
    @param output

    @return
    """
    import os
    from string import Template
    from itertools import islice

    # Variables
    success = True
    out_files = [
        output / Path(x.stem).with_suffix(".html")
        for x in sorted(sw_files, key=lambda x: x.stat().st_ctime)
    ]

    # Get the first N lines from each file
    context = []
    for sf in sw_files:
        with open(sf) as f:
            context.append(list(islice(f, 20)))

    context = [[">  " + s for s in sublist] for sublist in context]

    # Append the content to the file
    content = "\n".join(
        [f"## [{x.stem}]({x})\n{''.join(context[y])}" for y, x in enumerate(out_files)]
    )

    try:
        ## Append the content to the top-level sub-wiki file
        appendFile(sw.with_suffix(".md"), content)
    except Exception as e:
        logger.error(f"Exception thrown! {e}")
        success = False

    return success


########################################################################################################################

if __name__ == "__main__":  # pragma: no cover
    # Support running module as a command line command.
    #     python -m markdown [options] [args]
    main()
