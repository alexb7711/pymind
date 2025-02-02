"""!
@file title.py
@package Tags Page

This module generates the file that groups and links to all of the tags found. The file structure will be as follows:

```markdown
## Tag 1
[file1](path/to/file), [file2](path/to/file), [file3](path/to/file)

## Tag 2
[file2](path/to/file), [file3](path/to/file)
```
"""

import logging
import sys
from pathlib import Path

from pymind import utility
from pymind.utility.modfile import replaceText

logger = logging.getLogger("PYMIND")

##======================================================================================================================
# CONSTANTS

VERSION = "0.0.1"


##======================================================================================================================
#
def main(**kwargs) -> int:
    """!
    @brief Executes the tag page creation engine.

    @param in_d Input directory path

    @return True if creation was successful, False if creation failed
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

    # Write the string to disk
    success = __title(options["output"])

    sys.exit(not success)


##======================================================================================================================
#
def __title(input: str) -> bool:
    """!
    @brief Inject custom HTML title bar to each file

    The title bar items are created based on the `nav` tag. When the title bar is being applied to a file
    with the `nav` tag, a custom `active` class is also included to highlight the currently selected tab.

    @return True if successful, false if not
    """
    # For every file in the directory
    logger.debug(f"TITLE: Updating `title` for each file.")
    for file in Path(input).glob("*.html"):
        # Inject the title bar
        replaceText(file, "%title%", file.stem)

    return True


########################################################################################################################

if __name__ == "__main__":  # pragma: no cover
    # Support running module as a command line command.
    #     python -m markdown [options] [args]
    main()
