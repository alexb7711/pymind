"""!
@file footer.py
@package Injects footer into the website
"""

import logging
import sys
from datetime import date
from pathlib import Path

import markdown
from pymind import utility
from pymind.utility.modfile import replaceText

logger = logging.getLogger("PYMIND")

##======================================================================================================================
# CONSTANTS

VERSION = "0.0.1"
FOOTER = """<footer>
%footer%
</footer>
"""


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
    bf = var["build_files"]
    cp = var["cache_p"]

    # Write the string to disk
    success = __injectFooter(options["input"], options["output"], bf, cp)

    sys.exit(not success)


##======================================================================================================================
#
def __injectFooter(input: str, output: str, bf: list, cp: str) -> bool:
    """!
    @brief Inject custom footer into each file

    @param input Directory with markdown files
    @param input Directory with HTML files

    @return True if successful, false if not
    """
    # Check if the footer file exists
    footer_p = Path(cp) / Path("footer.md")
    if not footer_p.exists():
        logger.warning(f"FOOTER: Footer file was not found. Using default footer.")
        footer_md = """Generated by Pymind: %date%"""
    # Else, get the footer html
    else:
        with open(footer_p, "r") as f:
            footer_md = f.read()

    # Convert the footer markdown to html
    footer_html = markdown.markdown(footer_md)
    footer_html = FOOTER.replace("%footer%", footer_html)

    # Get the date
    today = date.today().strftime("%Y-%m-%d")

    # Update the footer
    __replaceFooter(output, footer_html, bf, today)

    return True


##======================================================================================================================
#
def __replaceFooter(output: str, text: str, bf: list, today: str = None) -> str:
    logger.debug("FOOTER: Looping though each converted file.")
    for file in bf:
        file = Path(output).absolute() / Path(Path(file).name).with_suffix(".html")
        logger.debug(f"FOOTER: Updating footer in: {file}.")
        replaceText(file, "{{footer}}", text)

        ## If the date text was provided
        if today:
            ### Update the date
            replaceText(file, "%date%", today)

    return


########################################################################################################################

if __name__ == "__main__":  # pragma: no cover
    # Support running module as a command line command.
    #     python -m markdown [options] [args]
    main()
