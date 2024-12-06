"""!
@file navigation_bar.py
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
NAV_BAR = """<div id="navigation">
<ul>
%list%
</ul>
</div>
"""
LIST_ITEM = '<li><a class="%class%" href="%item%">%name%</a></li>'


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

    # Retrieve the list of files and tags
    var = utility.cache.unPickleVar(options["var_p"], options["name"])

    # Ensure the cached variables were loaded
    tags = var["tags"]
    files = var["files"]

    # Write the string to disk
    success = __navigationBar(options["output"], tags, files)

    sys.exit(not success)


##======================================================================================================================
#
def __navigationBar(input: str, tags: dict, files: dict) -> bool:
    """!
    @brief Inject custom HTML navigation bar to each file

    The navigation bar items are created based on the `nav` tag. When the navigation bar is being applied to a file
    with the `nav` tag, a custom `active` class is also included to highlight the currently selected tab.

    @return True if successful, false if not
    """
    # List navigation bar items
    items = tags.get("nav", [])
    items = [Path(input) / Path(x).name for x in items]
    items = [str(x.with_suffix(".html")) for x in items]

    # If `index.py` is not included
    index_p = Path(input) / Path("index.md")
    if not items or index_p not in items:
        logger.warning("NAV: Index has not been included, adding it to the list!")
        items.append(str(index_p))
        files[index_p] = 0

    # Create unordered list
    logger.debug("NAV: Creating list of navigation bar items")
    ul = []
    for i in items:
        i = Path(i)
        new_item = LIST_ITEM
        new_item = new_item.replace("%item%", str(i.with_suffix(".html")))
        new_item = new_item.replace("%name%", str(i.stem))
        new_item = new_item.replace("%class%", "%" + str(Path(i).name) + "%")
        ul.append(new_item)

    # Generate navigation bar source
    logger.debug("NAV: Generating navigation bar HTML.")
    ul = "\n".join(ul)
    nav_bar = NAV_BAR.replace("%list%", ul)

    # Inject Navigation bar to each file
    logger.debug(f"NAV: Beginning navigation bar code injection")

    # For every file
    logger.debug(f"NAV: Updating `nav` tagged files.")
    for file in Path(input).glob("*.html"):
        # Inject the navigation bar
        replaceText(file, "%nav%", nav_bar)

    return True


########################################################################################################################

if __name__ == "__main__":  # pragma: no cover
    # Support running module as a command line command.
    #     python -m markdown [options] [args]
    main()
