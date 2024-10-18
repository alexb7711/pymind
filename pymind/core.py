import json
import logging
import platform
import re
import markdown
import yaml
from pathlib import Path
from typing import Any, TypedDict, List


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
    CORE_ENGINE_PATH = "pymind/engine/"

    # Select cache directory location based on the operating system
    CACHE_DIR = ".cache/pymind"
    CONF_DIR = ".config/pymind"

    if platform.system() == "Windows":
        CACHE_DIR = "AppData\Local\Programs\pymind\cache"
        CONF_DIR = "AppData\Local\Programs\pymind"
        TMP_DIR = f"{Path.home()}\AppData\Local\Temp"

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

        # Read in the parameters
        self.input = kwargs.get("input", None)
        self.output = kwargs.get("output", None)
        self.config_file = kwargs.get("config", None)

        self.force_build = kwargs.get("force", False)
        self.dry_run = kwargs.get("dry_run", False)

        self.engine = kwargs.get("engine", True)

        # Read in the configuration if provided
        if self.config_file:
            self.__setConfig()

        # Set the working directory
        self.__setWorkingDirectory()

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

        # Create a copy of the input directory into a temporary directory
        self.__copyInputDirectory()

        # Get the list of tags from the files
        self.tags = self.__getTags()

        # Run pre-processing engine
        self.__runEngine("PRE")

        # TODO: Generate home page
        # self.__createHome()

        # Convert the files
        self.__convertFiles()

        # Run post-processing engine
        self.__runEngine("POST")

        return

    ##==================================================================================================================
    #
    def __copyInputDirectory(self):
        """!
        @brief Copy `input` directory into `tmp` directory
        """

        # If the engine is not enabled, there is no need to create the working directory
        if not self.engine:
            return

        import shutil

        cache_dir, _ = self.__createCachePaths()
        out_d = str(cache_dir) + "/" + self.project_name + "/"
        shutil.copytree(self.input, out_d, dirs_exist_ok=True)
        return

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
        i = self.work_d

        # Create a list `Path`s for each `*.md` file in the `input` directory
        files = [f.resolve() for f in Path(self.work_d).rglob("*.md")]

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

        # Do not convert the files if `dry_run` is True
        if self.dry_run:
            return

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
    def __getTags(self) -> TypedDict:
        """!
        @brief Retrieve tags from the files

        @return A dictionary where the key is the tag found and the item is a list of files where the tag was found.
        """
        bf = self.build_files
        tags = {}

        # For each file in the 'build files' list
        for f in bf:
            ## Open the build file
            with open(f, "r") as txt:
                ### For each row in the build file
                for l in txt:
                    #### Search for tags in the file
                    matches = re.findall(r"^<!--\s*:?(.*?):\s*-->", l)

                    #### If tags were found
                    if matches:
                        ## Create a list of the tags
                        matches = matches[0].split(":")

                        ##### Add the tag to the table of tags
                        tags = self.__updateTags(f, tags, matches)

                        ##### Continue looking for tags in other files
                        continue

        return tags

    ##==================================================================================================================
    #
    def __updateTags(self, fn: str, tags: TypedDict, matches: List):
        """!
        @brief Updates `tags` with the data found in `matches` for the provided `file`

        @param fn Name of the parse file
        @param tags Dictionary of found tags associated with a list of the files in which that tag was found
        @param

        @return Update dictionary of tag => [list of files with tag]
        """
        # Loop through each matched tag found in `fn`
        for m in matches:
            ## If the tag already exists
            if tags.get(m):
                ### Append the tag
                tags[m].append(fn)
            else:
                ### Create a new tag
                tags[m] = [fn]

        return tags

    ##==================================================================================================================
    #
    def __runEngine(self, process_type: str):
        """!
        @brief Executes the pre- and post-processing engine.

        @param process_type Options are PRE and POST for pre- and post-processing, respectively
        """

        # Do not execute if the engine is not specified to run
        if not self.engine:
            return

        # Get the absolute path to the engine directory
        engine_dir = Path(PyMind.CORE_ENGINE_PATH).absolute()

        # List the directories in the engine directory
        engine_path = [str(x) for x in engine_dir.iterdir() if x.is_dir()]

        PRE_PATH = str(engine_dir) + "/pre"
        POST_PATH = str(engine_dir) + "/post"
        path = Path("")

        # If pre-processing, look for a `pre` directory
        if process_type == "PRE" and PRE_PATH in engine_path:
            path = Path(str(engine_dir) + "/pre/").absolute()
        # Else if post-processing, look for a `post` directory
        elif process_type == "POST" and POST_PATH in engine_path:
            path = Path(str(engine_dir) + "/post/").absolute()

        # For each file in the engine directories
        self.__executeSubprocess(path)

        return

    ##==================================================================================================================
    #
    def __executeSubprocess(self, script_d: str) -> bool:
        """!
        @brief Executes a subprocess from PyMind.

        @param Path to scripts directory

        @return True if successful execution, False otherwise
        """
        import subprocess

        # Execute subprocesses
        for file in script_d.iterdir():
            ## Ensure the items is a python script
            if file.is_file() and file.suffix == ".py":
                subprocess.run(["python", file, "-i", self.work_d, "-o", self.output])

        return True

    ##==================================================================================================================
    #
    def __setWorkingDirectory(self):
        """!
        @brief Set the working directory
        """
        if self.engine and self.input:
            self.work_d = Path(PyMind.CACHE_PATH) / Path(self.input).parts[-1]
        else:
            self.work_d = self.input
        return


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
