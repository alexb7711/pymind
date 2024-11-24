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

import optparse
import logging
import sys
from pathlib import Path

from pymind import utility

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
def parseInput(args=None) -> dict:
    """!
    @brief Read in the inputs and create a dictionary of parameters

    @param args Input arguments

    @return Dictionary of parameter inputs
    """
    parser = optparse.OptionParser(version=VERSION)

    # Add flags
    parser.add_option(
        "-i",
        "--input",
        dest="input",
        default="notes",
        metavar="INPUT_DIR",
        help="Relative path to a directory to recursively scan.",
    )
    parser.add_option(
        "-o",
        "--output",
        dest="output",
        default="doc",
        metavar="OUTPUT_DIR",
        help="Use to specify output directory, default is `doc`.",
    )
    parser.add_option(
        "-n",
        "--name",
        dest="name",
        default="",
        metavar="PROJECT_NAME",
        help="Name of the project, default is an empty string.",
    )
    parser.add_option(
        "-v",
        "--variable_p",
        dest="var_p",
        default="",
        metavar="VARIABLE_PATH",
        help="Path to the cached variable directory, default is an empty string.",
    )

    # Parse the input arguments
    (options, args) = parser.parse_args(args)

    opts = {
        "input": options.input,
        "output": options.output,
        "name": options.name,
        "var_p": options.var_p,
    }
    return opts


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
    options = parseInput()

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
        new_item = LIST_ITEM
        new_item = new_item.replace("%item%", i)
        new_item = new_item.replace("%name%", Path(i).name)
        new_item = new_item.replace("%class%", "%" + str(Path(i).name) + "%")
        ul.append(new_item)

    # Generate navigation bar source
    logger.debug("NAV: Generating navigation bar HTML.")
    ul = "\n".join(ul)
    nav_bar = NAV_BAR.replace("%list%", ul)

    # Inject Navigation bar to each file
    logger.debug(f"NAV: Beginning navigation bar code injection")

    # For every file
    logger.info(f"NAV: Updating `nav` tagged files.")
    for file in Path(input).glob("*.html"):
        # [
        #     Path(input) / Path(str(Path(x).name)).with_suffix(".html") for x in files
        # ]:
        logger.debug(f"NAV: Injecting navigation bar HTML to {file}")

        with open(file, "r") as f:
            file_content = f.read()

        with open(file, "w") as f:
            f.seek(0)
            f.write(nav_bar + file_content)

    return True


########################################################################################################################

if __name__ == "__main__":  # pragma: no cover
    # Support running module as a command line command.
    #     python -m markdown [options] [args]
    main()
