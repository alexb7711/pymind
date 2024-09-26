import logging
from typing import Any

__all__ = ["PyMind", "pymind"]

logger = logging.getLogger("PYMIND")

########################################################################################################################
# PYMIND CLASS
########################################################################################################################


class PyMind:
    """!
    @brief A tool to convert a directory of markdown files into a structured website!

    The PyMind class is the heart of the application. It contains the front end function calls that the user will
    interact with. The primary interface will be done via a configuration file so the user simply has to invoke the
    `pymind` command to generate their personal website.
    """

    ###################################################################################################################
    # PUBLIC
    ###################################################################################################################

    ##=================================================================================================================
    #
    def __init__(self, **kwargs):
        """!
        @brief Creates a new PyMind Instance

        @param **kwargs
        """

        # Read in the configuration if provided
        self.config_file = kwargs.get("config")

        if self.config_file:
            self.__setConfig()

        # Read the arguments provided
        return

    ###################################################################################################################
    # PRIVATE
    ###################################################################################################################

    ##=================================================================================================================
    #
    def __setConfig(self):
        """!
        @brief Read in the configuration file
        """

        try:
            with open(self.config_file, "r") as conf:
                pass
        except:
            print(f"WARNING: Could not find the configuration file: {self.config_file}")

        return


########################################################################################################################
# EXPORTED FUNCTIONS
########################################################################################################################


##======================================================================================================================
#
def pymind(**kwargs: Any):
    """!
    @brief Read Markdown files from a directory and write output to `self.out_dir`

    This is a shortcut function which initializes an instace of `PyMind` and calls the `generate_output` function.

    @param kwargs['input'] Path to directory to read from
    @param kwargs['output'] Path to directory to output to
    @param kwargs['config'] Configuration file to read from
    """
    pm = PyMind(**kwargs)
    return
