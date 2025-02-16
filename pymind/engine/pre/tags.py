"""!
@file tags.py
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

import pymind.utility as utility

logger = logging.getLogger("PYMIND")

##======================================================================================================================
# CONSTANTS

NEW_LINK = "[%file%](%path%)"
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

    # Retrieve the list of files and tags
    var = utility.cache.unPickleVar(options["var_p"], options["name"])

    # Ensure the cached variables were loaded
    tags = var["tags"]

    # Write the string to disk
    success = __createTagsPage(options["input"], tags)

    # Update `var` cached variable with newly created file
    var["build_files"].append(Path(options["input"]) / "tags_page.md")
    utility.cache.pickleVar(var, Path(options["var_p"]), options["name"])

    sys.exit(not success)


##======================================================================================================================
#
def __createTagsPage(input: str, tags: dict) -> bool:
    """!
    @brief Create an HTML file given a dictionary of tags provided

    @return True if successful, false if not
    """
    # Create output strings
    out_str = """# Tags Page\n"""

    # For each tag and files list
    logger.debug("TAGS: Searching for tags")
    for k, files in tags.items():
        ## Create a new section header
        out_str += f"\n## {k.capitalize()}\n"

        ## Create dummy variable to store the file link
        link_list = []

        ## For every file in the files list
        for f in files:
            ### Create a copy of NEW_LINK and replace with file attributes
            new_link = NEW_LINK
            new_link = new_link.replace("%file%", str(Path(f).name))
            new_link = new_link.replace(
                "%path%", str(Path(Path(f).name).with_suffix(".html"))
            )

            ### Create another item in the list
            link_list.append(new_link)

        ## Append the list of files to the output string
        logger.debug("TAGS: Creating a list out of the tags")
        out_str += ", ".join(link_list)

    out_p = Path(input) / Path("tags_page.md")

    logger.debug(f"TAGS: Writing to disk {out_p}")
    with open(out_p, "w") as f:
        f.write(out_str)

    return True


########################################################################################################################

if __name__ == "__main__":  # pragma: no cover
    # Support running module as a command line command.
    #     python -m markdown [options] [args]
    main()
