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

    # Write the string to disk
    success = __injectFooter(options["input"], options["output"])

    sys.exit(not success)


##======================================================================================================================
#
def __injectFooter(input: str, output: str) -> bool:
    """!
    @brief Inject custom footer into each file

    @param input Directory with markdown files
    @param input Directory with HTML files

    @return True if successful, false if not
    """

    # Check if the footer file exists
    footer_p = Path(input) / Path("footer.md")
    if not footer_p.exists():
        logger.warning(f"FOOTER: Footer file was not found, exiting early.")
        return False

    # Get the footer html
    with open(footer_p, "r") as f:
        footer_md = f.read()

    # Convert the footer markdown to html
    footer_html = markdown.markdown(footer_md)
    footer_html = FOOTER.replace("%footer%", footer_html)

    # Get the date
    today = date.today().strftime("%Y-%m-%d")

    # For every file found in the input directory
    logger.debug(f"FOOTER: Looping though each converted file.")
    for file in Path(output).glob("*.html"):
        logger.debug(f"FOOTER: Updating footer in: {file}.")
        replaceText(file, "{{footer}}", footer_html)
        replaceText(file, "%date%", today)

        # with open(file, "r+") as f:
        #     ## Read in the file
        #     html = f.readlines()
        #
        #     ## Inject footer two lines up from the bottom of the file
        #     html[-2] = FOOTER.replace("%footer%", footer_html) + "\n" + html[-2]
        #
        #     ## Joint html back together
        #     html = "".join(html)
        #
        #     ## Inject the footer
        #     f.write(html)

    return True


########################################################################################################################

if __name__ == "__main__":  # pragma: no cover
    # Support running module as a command line command.
    #     python -m markdown [options] [args]
    main()
