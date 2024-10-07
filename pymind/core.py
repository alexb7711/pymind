import json
import logging
import platform
from pathlib import Path
from typing import Any, TypedDict

import markdown
import yaml

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

    ####################################################################################################################
    # CONSTANTS
    ####################################################################################################################

    # Select cache directory location based on the operating system
    CACHE_DIR = ".cache/pymind"
    CONF_DIR = ".config/pymind"

    if platform.system() == "Windows":
        CACHE_DIR = "AppData/Local/Programs/pymind/cache"
        CACHE_DIR = "AppData/Local/Programs/pymind"

    CONFIG_FILE = "pymind.yaml"
    CONFIG_PATH = f"{Path.home()}/{CONF_DIR}/{CONFIG_FILE}"
    CACHE_PATH = f"{Path.home()}/{CACHE_DIR}"

    ####################################################################################################################
    # PUBLIC
    ####################################################################################################################

    ##==================================================================================================================
    #
    def __init__(self, **kwargs):
        """!
        @brief Creates a new PyMind Instance

        @param **kwargs Dictionary of arguments
        """

        # Member variables
        self.files_found = []
        self.project_name = ""

        # Read in the input and output options
        self.input = kwargs.get("input", None)
        self.output = kwargs.get("output", None)
        self.force_build = kwargs.get("force", False)

        # Read in the configuration if provided
        self.config_file = kwargs.get("config")

        if self.config_file:
            self.__setConfig()

        return

    ##==================================================================================================================
    #
    def run(self):
        """!
        @brief Execute PyMind.
        """
        # If an input directory was not provided
        if self.input == None:
            print("WARNING: AN INPUT DIRECTORY WAS NEVER PROVIDED!!!\nABORTING!!!")
            return

        # Create the website
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

        # Read in the configuration file
        try:
            with open(self.config_file, "r") as f:
                conf = yaml.load(f, Loader=yaml.SafeLoader)

                ## Read in the configuration file
                self.input = conf.get("input", None)
                self.output = conf.get("output", None)

        except Exception as e:
            print(f"WARNING: COULD NOT FIND THE CONFIGURATION FILE: {self.config_file}")
            print(f"Error: {e}")

        return

    ##==================================================================================================================
    #
    def __createBrain(self):
        """!
        @brief Entry function to start creating the PyMind second brain.
        """
        # Get the list of files to convert
        self.build_files = self.__getFilesList()

        # Convert the files
        self.__convertFiles()

    ##==================================================================================================================
    #
    def __getFilesList(self) -> list[str]:
        """!
        @brief Returns a list of files to convert
        """
        # Create database of files
        self.files_found = self.__findFiles()

        # Extract the project name based on the base directory name
        self.project_name = self.__getProjectName()

        # If `force_build` not active
        build_files = {}
        if self.force_build:
            ## Use the found files as the build list
            build_files = [str(f) for f in self.files_found.keys()]
        else:
            ## Otherwise compare the database of files with cached database (if one exists)
            build_files = self.__getBuildFiles()

        # Update the cached database
        self.__cacheFiles()

        return build_files

    ##==================================================================================================================
    #
    def __findFiles(self) -> dict[Path]:
        """!
        @brief Create a database of all the files in the `input` directory

        @return Dictionary of files and their modified times from within the `input` directory
        """
        # Input directory
        i = self.input

        # Create a list `Path`s for each `*.md` file in the `input` directory
        files = [f.resolve() for f in Path(self.input).rglob("*.md")]

        # Create file database
        file_database = {}
        for f in files:
            mod_time = f.lstat().st_mtime
            file_database[str(f)] = mod_time

        return file_database

    ##==================================================================================================================
    #
    def __getProjectName(self):
        """!
        @brief Return the project name.
        """

        # Get the project name
        project_name = Path(self.input)
        project_name = project_name.absolute()
        project_name = project_name.parts[-1]

        return project_name

    ##==================================================================================================================
    #
    def __getBuildFiles(self) -> list[Path]:
        """!
        @brief Create a list of files that have been modified or added
        @return List of files that need to be re-generated.
        """
        # List of files to process
        p_files = []

        # Get data from the previous run
        prev_data = self.__loadCache()

        # For each file that has been found in the input directory
        for f, mod in self.files_found.items():
            ## Check if the file is new
            if not prev_data.get(f, False):
                p_files.append(Path(f))
                continue

            ## Check if the file has been updated
            if mod > prev_data.get(f):
                p_files.append(Path(f))
                continue

        return p_files

    ##==================================================================================================================
    #
    def __loadCache(self):
        """!
        @brief Load the cached dictionary of modified files.
        @return Return dictionary of files and modified times
        """
        # Create the path objects
        _, cache_file = self.__createCachePaths()

        # Ensure the cached file exists
        if cache_file.exists():
            ## Read in the cached files from the previous run
            with open(cache_file, "r") as cf:
                run_data = json.load(cf)
                return run_data

        return {}

    ##==================================================================================================================
    #
    def __cacheFiles(self):
        """!
        @brief Cache files in the default cache location.
        """
        # Create the path objects
        cache_dir, cache_file = self.__createCachePaths()

        # Create JSON object
        file_data = json.dumps(self.files_found, indent=4)

        # Write the found file data to the cache file
        with open(cache_file, "w") as cf:
            cf.write(file_data)

        return

    ##==================================================================================================================
    #
    def __createCachePaths(self):
        """!
        @brief Create `Path` objects for cache

        This method creates the cache file paths, and ensures that the path to the cache directory exists.

        @return Returns tuple of strings (cache_dir, cache_file)
        """
        cache_dir = Path(f"{PyMind.CACHE_PATH}/")
        cache_file = Path(f"{PyMind.CACHE_PATH}/{self.project_name}_cache.json")

        # Create the directory if it does not exist
        cache_dir.mkdir(parents=True, exist_ok=True)

        return (cache_dir, cache_file)

    ##==================================================================================================================
    #
    def __convertFiles(self):
        """!
        @brief Convert the list of files to HTML
        """

        # Ensure the output directory exists
        Path(self.output).mkdir(parents=True, exist_ok=True)

        # Convert each markdown file
        for bf in self.build_files:
            ## Create the output file path
            output_file = self.output + "/" + Path(bf).stem + ".html"

            ## Convert the markdown file to HTML
            html = markdown.markdownFromFile(input=str(bf), output=output_file)

        return

    ##==================================================================================================================
    #
    def __getTag(self) -> TypedDict:
        """!
        @brief Retrieve tags from the files
        """
        bf = self.build_files
        tags = {}

        # For each file in the 'build files' list
        for f in bf:
            ## Search for tags in the file
            ## Add the tag to the table of tags
            pass

        return tags


########################################################################################################################
# EXPORTED FUNCTIONS
########################################################################################################################


##======================================================================================================================
#
def pymind(**kwargs: Any):
    """!
    @brief Read Markdown files from a directory and write output to `self.out_dir`

    This is a shortcut function which initializes an instance of `PyMind` and calls the `generate_output` function.

    @param kwargs['input'] Path to directory to read from
    @param kwargs['output'] Path to directory to output to
    @param kwargs['force'] Regenerate all files
    @param kwargs['config'] Configuration file to read from
    """
    pm = PyMind(**kwargs)
    return
