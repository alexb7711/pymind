import logging
import pickle
from pathlib import Path
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

        # Member variables
        self.files_found = []

        # Read in the input and output options
        self.input = kwargs.get("input", None)
        self.output = kwargs.get("output", None)

        # Read in the configuration if provided
        self.config_file = kwargs.get("config")

        if self.config_file:
            self.__setConfig()

        return

    ##=================================================================================================================
    #
    def run(self):
        """!
        @brief Execute PyMind.
        """
        self.__createBrain()
        return

    ####################################################################################################################
    # PRIVATE
    ####################################################################################################################

    ##==================================================================================================================
    #
    def __setConfig(self):
        """!
        @brief Read in the configuration file
        """

        # TODO: Read in the configuration file
        try:
            with open(self.config_file, "r") as conf:
                pass
        except:
            print(f"WARNING: Could not find the configuration file: {self.config_file}")

        return

    ##==================================================================================================================
    #
    def __createBrain(self):
        """!
        @brief Entry function to start creating the PyMind second brain.
        """
        # Get the list of files to convert
        self.__getFilesList()

        # Convert the files
        self.__convertFiles()

    ##==================================================================================================================
    #
    def __getFilesList(self) -> list[str]:
        """!
        @brief Returns a list of files to convert
        """
        # TODO: If `force_build` is not active
        ## Create database of files
        self.files_found = self.__findFiles()

        ## Compare database of files with cached database if one exists

        # Update the cached database

        return []

    ##==================================================================================================================
    #
    def __findFiles(self) -> list[Path]:
        """!
        @brief Create a database of all the files in the `input` directory
        """
        # Input directory
        i = self.input

        # Create a list `Path`s for each `*.md` file in the `input` directory
        files = [f.resolve() for f in Path(self.input).rglob("*.md")]

        print(f"HERE {files}")

        return files

    ##==================================================================================================================
    #
    def __convertFiles(self):
        """!
        @brief Convert the list of files to HTML
        """
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
