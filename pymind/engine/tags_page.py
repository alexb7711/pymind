"""!
@file tags_page.py
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
from typing import TypedDict
from pathlib import Path

import pymind


##======================================================================================================================
# CONSTANTS

NEW_LINK = "[%file%](%path%)"
VERSION = "0.0.1"


##======================================================================================================================
#
def parseInput(args=None) -> TypedDict:
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

    # Parse the input arguments
    (options, args) = parser.parse_args(args)

    opts = {
        "input": options.input,
        "output": options.output,
        "force": True,
        "post_engine": False,
        "dry_run": True,
    }
    return opts


##======================================================================================================================
#
def main(**kwargs) -> bool:
    """!
    @brief Executes the tag page creation engine.

    @param in_d Input directory path

    @return True if creation was successful, False if creation failed
    """
    # Parse the input arguments
    options = parseInput()

    # If the input or output directory were not provided
    if not options["input"] or not options["output"]:
        ## Fail the file creation
        return False

    # Create an instance of PyMind
    pm = pymind.PyMind(**options)
    pm.run()

    # Retrieve the list of files and tags
    tags = pm.tags

    # Write the string to disk
    __createTagsPage(options["input"], tags)

    # Re-run PyMind without the `force` and `dry_run` flags
    pm.force_build = False
    pm.dry_run = False
    pm.run()

    return True


##======================================================================================================================
#
def __createTagsPage(input: str, tags: TypedDict) -> bool:
    """!
    @brief Create an HTML file given a dictionary of tags provided

    @return True if successful, false if not
    """
    # Create output strings
    out_str = """# Tags Page\n"""

    # For each tag and files list
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
            new_link = new_link.replace("%path%", str(Path(f)))

            ### Create another item in the list
            link_list.append(new_link)

        ## Append the list of files to the output string
        out_str += ", ".join(link_list)

    with open(f"{input}/tags_page.md", "w") as f:
        f.write(out_str)

    return True


########################################################################################################################

if __name__ == "__main__":  # pragma: no cover
    # Support running module as a command line command.
    #     python -m markdown [options] [args]
    main()
