import logging
import os
import platform
import re
from pathlib import Path
from typing import Any

import markdown

from pymind.utility.cache import (
    deleteCacheVar,
    loadCacheJSON,
    pickleVar,
    writeCacheJSON,
)
from pymind.utility.misc import recursiveDelete, addOrAppend
from pymind.utility.search import findFiles
from pymind.utility.tags import getTags
from pymind.utility.modfile import multipleStrReplace

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
    # CORE_ENGINE_PATH = Path("pymind/engine/")
    CORE_ENGINE_PATH = Path(os.path.dirname(os.path.abspath(__file__))) / Path(
        "engine/"
    )

    # Select cache directory location based on the operating system
    CACHE_DIR = Path(".cache/pymind")
    CONF_DIR = Path("config/pymind")

    if platform.system() == "Windows":
        CACHE_DIR = Path("AppData\Local\Programs\pymind\cache")
        CONF_DIR = Path("AppData\Local\Programs\pymind")

    CONFIG_FILE = "pymind.yaml"
    CONFIG_DIR = Path(f"{Path.home()}/{CONF_DIR}")
    CONFIG_PATH = Path(f"{Path.home()}/{CONF_DIR}/{CONFIG_FILE}")
    CACHE_PATH = Path(f"{Path.home()}/{CACHE_DIR}")

    TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>%title%</title>
    <link href="%css%" rel="stylesheet">
</head>
<body>
%nav%
<div class="content">
%content%
</div>
{{footer}}
</body>
</html>
"""

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
        self.css: Path = None                       #!< CSS file location
        self.dry_run = False                        #!< Do everything except output files
        self.engine = True                          #!< Path to engine directory
        self.extensions: list = ["toc"]             #!< Markdown extensions list
        self.files_found = []                       #!< List of files found
        self.footer: Path = None                    #!< Footer file location
        self.force_build = False                    #!< Flag to rebuild entire project
        self.input = None                           #!< Input directory
        self.output = None                          #!< Output directory
        self.project_name: str = ""                 #!< Name of the project
        self.refs: dict = {}                        #!< Dictionary of file references

        # Read in the configuration if provided
        self.config_file = kwargs.get("config", None) #!< Path to configuration file
        if self.config_file:
            self.config_file = Path(self.config_file)
            self.CONFIG_PATH = self.config_file
            self.CONFIG_DIR = self.config_file.parent
            self.__setConfig()
        elif self.CONFIG_PATH.exists():
            self.config_file = self.CONFIG_FILE

        # Read in the parameters
        self.input = kwargs.get("input", self.input)
        self.output = kwargs.get("output", self.output)

        self.force_build = kwargs.get("force", self.force_build)
        self.dry_run = kwargs.get("dry_run", self.dry_run)

        self.engine = kwargs.get("engine", self.engine)

        # Configure the HTML template
        tmplt_path = self.CONFIG_DIR / Path("template.html")
        if tmplt_path.exists():
            logger.debug("Reading in template html file.")
            with open(tmplt_path, 'r') as f:
                self.template = f.read()
        else:
            self.template = self.TEMPLATE

        # Create input and output Path variables
        self.input = Path(self.input).absolute()
        self.output = Path(self.output).absolute()

        # Create the cache directory if it does not exist
        PyMind.CACHE_PATH.mkdir(parents=True, exist_ok=True)

        # Set the working directory
        self.__setWorkingDirectory()

        return

    ##==================================================================================================================
    #
    def __del__(self):
        """!
        @brief PyMind deconstructor.

        The deconstructor removes any cached files that should not be persistent between runs.
        """
        # Delete cached variables
        cache_dir = PyMind.CACHE_PATH / Path("variables")

        # Remove the cached variable
        try:
            deleteCacheVar(cache_dir, self.project_name)

        except Exception as e:
            logger.error(e)

        # Remove the copied working tree
        recursiveDelete(Path(self.work_d))

        return

    ##==================================================================================================================
    #
    def __call__(self):
        self.run()
        return

    ##==================================================================================================================
    #
    def run(self):
        """!
        @brief Execute PyMind.
        """
        # If an input directory was not provided
        if self.input == None:
            logger.critical("AN INPUT DIRECTORY WAS NEVER PROVIDED!!!\nABORTING!!!")
            return

        # Create the website
        self.__createBrain()
        return

    ##==================================================================================================================
    #
    def getCachePaths(self, path: str) -> Path:
        """!
        @brief Create `Path` objects for cache

        This method creates the cache file paths, and ensures that the path to the cache directory exists.

        @param path String that specifies the desired path to be returned. [base, database]

        @return Returns a path to either the cached directory, cached file database, or cached variable
        """
        # Variables
        dir = None
        path = path.lower()

        logger.debug(f"Retrieving the {path} cache path.")

        # Select the path
        if path == "base":
            dir = PyMind.CACHE_PATH
        elif path == "database":
            dir = PyMind.CACHE_PATH / Path(f"{self.project_name}_cache.json")
        elif path == "var":
            dir = PyMind.CACHE_PATH / Path("variables")
        else:
            raise ("PyMind: Path type not specified!")

        return dir

    ####################################################################################################################
    # PRIVATE
    ####################################################################################################################

    ##==================================================================================================================
    #
    def __setConfig(self):
        """!
        @brief Read in the configuration file
        """
        import tomllib

        # Read in the configuration file
        try:
            with open(self.config_file, "rb") as f:
                conf = tomllib.load(f)

                ## Read in the configuration file
                self.input = Path(conf.get("IO").get("input"))
                self.output = Path(conf.get("IO").get("output"))
                self.css = conf.get("HTML").get("css")
                self.footer = conf.get("HTML").get("footer")
                self.extensions = sorted(list(set(conf.get("Markdown").get("extensions", []) + self.extensions)))

        except Exception as e:
            logger.warning(
                f"WARNING: COULD NOT FIND THE CONFIGURATION FILE: {self.config_file}"
            )
            logger.error(f"Error: {e}")

        return

    ##==================================================================================================================
    #
    def __createBrain(self):
        """!
        @brief Entry function to start creating the PyMind second brain.
        """
        ##--------------------------------------------------------------------------------------------------------------
        # PRE-PROCESS
        self.__preProcess()

        ##--------------------------------------------------------------------------------------------------------------
        # EXECUTE CONVERSION PROCESS

        # Convert the files
        self.__convertFiles()

        ##--------------------------------------------------------------------------------------------------------------
        # POST-PROCESS
        self.__postProcess()

        return

    ##==================================================================================================================
    #
    def __preProcess(self):
        """!
        @brief Run the PyMind pre-processor.
        """
        import shutil

        # Create a copy of the input directory into a temporary directory
        self.__copyInputDirectory()

        # Copy the CSS file if it exists
        logger.debug(f"Copying footer {self.output}")
        if self.footer:
            shutil.copyfile(self.config_file.parent / Path(self.footer), self.work_d / Path(self.footer))

        # Get the list of files to convert
        self.build_files = self.__getFilesList()                              #!< List of files to be built

        # Get the list of tags from the files
        self.tags = getTags(self.build_files)                                 #!< Dictionary of tags found

        # Convert file references to links
        self.__refToLink()

        # Cache variables
        self.__cacheVar()

        # Run pre-processing engine
        self.__runEngine("PRE")

        return

    ##==================================================================================================================
    #
    def __postProcess(self):
        """!
        @brief Run the PyMind post-processor.
        """
        import shutil

        # Run post-processing engine
        self.__runEngine("POST")

        # Copy the CSS file if it exists
        logger.debug(f"Copying configuration file to {self.output}")
        if self.css:
            shutil.copyfile(self.config_file.parent / Path(self.css), self.output / Path(self.css))

        return

    ##==================================================================================================================
    #
    def __copyInputDirectory(self):
        """!
        @brief Copy `input` directory into `cache` directory
        """
        import shutil

        # Extract the project name based on the base directory name
        self.project_name = self.__getProjectName()
        cache_dir = self.getCachePaths("base")
        out_d = cache_dir / Path(self.project_name)

        logger.debug(f"Coping input directory to {out_d}")

        shutil.copytree(self.input, out_d, dirs_exist_ok=True)

        return

    ##==================================================================================================================
    #
    def __getFilesList(self) -> list[str]:
        """!
        @brief Returns a list of files to convert
        """
        # Create database of files
        logger.debug("Searching for files.")
        self.files_found = findFiles(self.work_d)

        # If `force_build` not active
        build_files = []
        if self.force_build:
            ## Use the found files as the build list
            logger.debug("Executing a force build.")
            build_files = [str(f) for f in self.files_found.keys()]
        else:
            ## Otherwise compare the database of files with cached database (if one exists)
            logger.debug("Filtering found files to only the update files.")
            build_files = self.__getBuildFiles()

        # Update the cached database
        writeCacheJSON(self.getCachePaths("database"), self.files_found)

        return build_files

    ##==================================================================================================================
    #
    def __getProjectName(self) -> str:
        """!
        @brief Return the project name.

        @return Project name as a string.
        """

        # Get the project name
        logger.debug("Retrieving the project name.")
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
        logger.debug("Filtering the found files to only the modified files.")

        # List of files to process
        p_files = []

        # Get data from the previous run
        prev_data = loadCacheJSON(self.getCachePaths("database"))

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
    def __convertFiles(self):
        """!
        @brief Convert the list of files to HTML
        """
        logger.debug("Converting the build files.")

        # Do not convert the files if `dry_run` is True
        if self.dry_run:
            return

        # Ensure the output directory exists
        self.output.mkdir(parents=True, exist_ok=True)

        # Convert each markdown file
        for bf in self.build_files:
            ## Create the output file path
            output_file = self.output / Path(bf).stem
            output_file = output_file.with_suffix(".html")

            ## Open the file to be converted
            with open(bf, "r") as f:
                ### Read the text from the markdown file
                md = f.read()

            ## Convert the markdown to HTML
            content = markdown.markdown(md, extensions=self.extensions)

            ## Inject content into html file
            html = PyMind.TEMPLATE.replace("%content%", content)

            if self.css:
                html = html.replace("%css%", str(self.css))

            ## Write the HTML to file
            with open(output_file, "w") as f:
                f.write(html)

        return

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

        PRE_PATH = engine_dir / Path("pre")
        POST_PATH = engine_dir / Path("post")
        path = Path("")

        # If pre-processing, look for a `pre` directory
        if process_type == "PRE" and str(PRE_PATH) in engine_path:
            path = PRE_PATH.absolute()
        # Else if post-processing, look for a `post` directory
        elif process_type == "POST" and str(POST_PATH) in engine_path:
            path = POST_PATH.absolute()

        # For each file in the engine directories
        logger.debug(f"Beginning {process_type}-engine...")
        self.__executeSubprocess(path)

        # If the engine being ran is the pre-processor
        if process_type == "PRE":
            # Update the build files
            self.build_files = self.__getFilesList()

        return

    ##==================================================================================================================
    #
    def __executeSubprocess(self, script_d):
        """!
        @brief Executes a subprocess from PyMind.

        @param Path to scripts directory

        @return True if successful execution, False otherwise
        """
        import subprocess

        # Convert cache variable directory path to a string
        cache_p = str(self.getCachePaths("var"))

        # Execute subprocesses
        for file in script_d.iterdir():
            ## Ensure the item is a python script
            if file.is_file() and file.suffix == ".py":
                logger.debug(f"Executing {file}")

                ### Execute the process
                process = subprocess.run(
                    [
                        "python",
                        file,
                        "-i",
                        self.work_d,
                        "-o",
                        self.output,
                        "-n",
                        self.project_name,
                        "-v",
                        cache_p,
                    ]
                )

                ### Check if the process succeeded
                process.check_returncode()

                logger.debug(f"{file} executed successfully.")
        return

    ##==================================================================================================================
    #
    def __setWorkingDirectory(self):
        """!
        @brief Set the working directory

        The working directory is where the actions performed by PyMind or the engine scripts will take place.
        """
        print(f"====>{self.input}")
        self.work_d = Path(PyMind.CACHE_PATH) / Path(self.input).parts[-1]
        return

    ##==================================================================================================================
    #
    def __refToLink(self):
        """!
        @brief Convert file references to markdown styled links.
        """

        # For each file to be built
        for file in self.build_files:
            with open(file, "r+") as f:
                ## Read in the file
                file_content = f.read()

                ## Search text for file reference syntax
                name_regex = "[^]]+"
                url_regex = "[^)]+"
                markup_regex = '\[({0})]\(\s*({1})\s*\)'.format(name_regex, url_regex)

                ## Search for the links
                rx_match = re.findall(markup_regex, file_content)

                ## if regex matches were found
                searchAndReplace = {}
                if rx_match:
                    ### For every match
                    for x in rx_match:
                        #### Check if the link is not for an external site
                        if not re.search("http[s]?://", x[1]):
                            ##### Add the URL to the search and replace list
                            key = f"[{x[0]}]({x[1]})"
                            value = f"[{x[0]}]({Path(x[1]).stem}.html)"
                            searchAndReplace[key] = value

                            ##### Add the files to the refs list
                            key = str(x[1])
                            value = str(Path(file).stem)
                            self.refs = addOrAppend(self.refs, key, value)

                    ### Replace all matches found
                    file_content = multipleStrReplace(file_content, searchAndReplace)

                ## Update the file
                f.seek(0)
                f.write(file_content)
                f.truncate()

        return

    ##==================================================================================================================
    #
    def __cacheVar(self):
        """!
        @brief Cache variables
        """
        logger.debug("Caching the environment variables.")

        # Variables
        var = {
            "files": self.files_found,
            "build_files": self.build_files,
            "tags": self.tags,
            "refs": self.refs,
        }
        cache_dir = self.getCachePaths("var")

        # Cache the variable
        pickleVar(var, cache_dir, self.project_name)

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
    @param kwargs['dry_run'] Run PyMind, but don't output anything
    @param kwargs['engine'] Execute the plugin engine
    @param kwargs['config'] Configuration file to read from
    """
    pm = PyMind(**kwargs)
    pm()
    return
