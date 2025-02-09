"""!
@file search.py

@module The search module exposes the search functions from PyMind for plug-ins to reuse.
"""

import logging
from pathlib import Path

logger = logging.getLogger("PYMIND")

##======================================================================================================================
#
def findFiles(dir: Path) -> dict[Path]:
    """!
    @brief Create a database of all the files in the `input` directory

    @param dir Base path to start searching for markdown files.

    @return Dictionary of files and their modified times from within the `input` directory
    """
    # Create a list `Path`s for each `*.md` file in the `input` directory
    logger.debug(f"SEARCH: Searching for files in {dir}")
    files = [f.resolve() for f in Path(dir).rglob("*.md")]

    # Create file database
    logger.debug("SEARCH: Creating database of file and modification date.")
    file_database = {}
    for f in files:
        mod_time = f.lstat().st_mtime
        file_database[str(f)] = mod_time

    return file_database

##======================================================================================================================
#
def recursiveSearch(dir: Path, fn: str, extension: str = None) -> Path:
    """!
    @brief Recursively search for a file

    @param dir Directory path from which to start searching from
    @param fn Name of the file to search for
    @param extension Optional parameter to provide the file extension

    @returns
    The first instance where the file `fn` is found.
    """
    # Convert the file name int a Path object
    fn = Path(fn)

    # If a suffix is provided in the file name, use that by default
    if fn.suffixes:
        extension = "." + (fn).suffixes[0]
    # Else if an extension is not in the file name and one is not provided in the extension variable, search every file
    # for the the file name `fn`
    elif not fn.suffixes and not extension:
        extension = ""
    elif extension and not fn.suffixes:
        extension = "." + extension
        fn = fn.with_suffix(extension)

    # Search for the file `fn`
    for path in dir.rglob('*'+extension):
        if str(path.name) == str(fn):
            return path

    return None
