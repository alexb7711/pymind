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
    logger.debug(f"SEARCH: Creating database of file and modification date.")
    file_database = {}
    for f in files:
        mod_time = f.lstat().st_mtime
        file_database[str(f)] = mod_time

    return file_database
