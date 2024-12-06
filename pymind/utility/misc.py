"""!
@file misc.py

@module This module exposes miscellaneous functions.
"""

import logging
import optparse
from pathlib import Path

logger = logging.getLogger("PYMIND")


##======================================================================================================================
#
def recursiveDelete(directory: Path):
    """!
    @brief Recursively delete files from the starting point `directory`

    @param directory Path to the directory to recursively delete
    """
    logger.debug(f"MISC: Recursively deleting {directory}")

    for path in directory.rglob("*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            recursiveDelete(path)
            path.rmdir()

    return


##======================================================================================================================
#
def parseInput(version, args=None) -> dict:
    """!
    @brief Read in the inputs and create a dictionary of parameters

    @param version Version of the plugin being passed in
    @param args Input arguments

    @return Dictionary of parameter inputs
    """
    parser = optparse.OptionParser(version=version)

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
