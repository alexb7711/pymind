"""!
@file reference.py
@package Referenced files
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
    success = __referenced_in(options["input"], var["refs"])

    sys.exit(not success)


##======================================================================================================================
#
def __referenced_in(input: Path, refs: dict) -> bool:
    """!
    @brief Create a list of file that is the currently visited file is referenced in

    At the end of each normal page (i.e. basically every page that is not generated) a list of files will be included
    which indicates that the currently visited file was referenced in that file.

    @param refs Dictionary where the key is a file name and the value is a dictionary of files that the
    key is referenced in.

    @return True if successful, false if not
    """
    # For every file in the directory
    ref_keys = list(refs.keys())
    for file in ref_keys:
        logger.debug(f"REF: Appending to {file}.")

        ## Convert python list into a Markdown list
        md_refs = [f"- [{x}]({x}.html)" for x in refs[file]]
        md_refs = "\n".join(md_refs)

        ## Append the list to the file
        refs_section = f"# Related Topics\n{md_refs}"
        fp = recursiveSearch(Path(input), file, "md")
        if fp:
            appendFile(fp.with_suffix(".md"), refs_section)
    return True


########################################################################################################################

if __name__ == "__main__":  # pragma: no cover
    # Support running module as a command line command.
    #     python -m markdown [options] [args]
    main()
