"""!
@file footer.py
@package Create a common footer

This module generates the footer used in the generated website.
"""

import optparse
import logging
import sys
from pathlib import Path
from typing import TypedDict

import pymind
from pymind import utility

logger = logging.getLogger("PYMIND")

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

    # Retrieve the list of files and tags
    var = utility.cache.unPickleVar(options["var_p"], options["name"])

    # Write the string to disk
    success = __createLandingPage(
        var["build_files"], options["input"], options["output"]
    )

    sys.exit(not success)


##======================================================================================================================
#
def __includeFile(in_f: Path, out_str: str, token: str) -> str:
    """!
    @brief Include text of a file in the output string at the location of the token

    @param in_f Path to the file
    @param out_str String to be updated
    @param token

    @return Updated output string
    """
    logger.debug(f"LANDING: Including text from {in_f}")
    updates = ""
    try:
        with open(in_f) as f:
            updates = f.read()
            out_str = out_str.replace(token, updates)
    except:
        logger.warning(
            f"LANDING: COULD NOT FIND {in_f}.\nREMOVING SECTION FROM LANDING PAGE."
        )
        out_str = out_str.replace(token, "")

    return out_str


##======================================================================================================================
#
def __createLandingPage(bf: list, input: str, output: str) -> bool:
    """!
    @brief Create the default landing page.

    @param bf
    @param output

    @return True if successful, false if not
    """
    # Create output strings
    out_str = """%index%
# UPDATES
%update%

# Recently Added/Updated

%recent%
    """
    # Include the `index.md` file
    out_str = __includeFile(Path(input) / Path("index.md"), out_str, "%index%")

    # Include the `uptades.md` file
    out_str = __includeFile(Path(input) / Path("updates.md"), out_str, "%update%")

    # Recently added/updated files
    logger.debug("LANDING: Recently updated")
    recent = []
    for f in bf:
        new_link = NEW_LINK
        new_link = new_link.replace("%file%", str(Path(f).name))
        new_link = new_link.replace("%path%", str(Path(f)))

        recent.append(new_link)

    recent = "\n".join(recent)

    out_str = out_str.replace("%recent%", recent)

    out_p = Path(input) / Path("index.md")
    logger.debug(f"LOGGER: Writing to disk {out_p}")
    with open(out_p, "w") as f:
        f.write(out_str)

    return True


########################################################################################################################

if __name__ == "__main__":  # pragma: no cover
    # Support running module as a command line command.
    #     python -m markdown [options] [args]
    main()
