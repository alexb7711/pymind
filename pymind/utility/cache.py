"""!
@file cache.py

@module The `cache.py` module is a helper module to set and retrieve cached variables that may be useful to
plugin generating scripts.
"""

import json
import logging
import pickle
from pathlib import Path
from typing import Any

logger = logging.getLogger("PYMIND")

########################################################################################################################
# FILE DATABASE CACHING
########################################################################################################################


##======================================================================================================================
#
def loadCacheJSON(cache_file: Path):
    """!
    @brief Load the cached JSON file located in the path specified.

    @param cache_file Path to the cached JSON file

    @return Return dictionary of files and modified times
    """
    logger.debug(f"JSON: Attempting to load {cache_file}")

    try:
        # Ensure the cached file exists
        if cache_file.exists():
            ## Read in the cached files from the previous run
            with open(cache_file, "r") as cf:
                run_data = json.load(cf)
                logger.debug("JSON: Successfully loaded file")
                return run_data
    except:
        logger.warning("JSON: Failed to load")
        return {}


##======================================================================================================================
#
def writeCacheJSON(cache_dir: Path, var: Any):
    """!
    @brief Helper function to cache files in the specified location as a JSON.

    @param cache_dir Path to the directory
    @param var Variable to be cached as JSON file
    """
    logger.debug(f"JSON: Attempting to write to {cache_dir}")

    # Create JSON object
    file_data = json.dumps(var, indent=4)

    # Write the found file data to the cache file
    with open(cache_dir, "w") as cf:
        cf.write(file_data)

    return


########################################################################################################################
# VARIABLE CACHING
########################################################################################################################


##======================================================================================================================
#
def pickleVar(var: Any, path: Path, name: str):
    """!
    @brief The cache variable function caches `var` in `path` by pickling the data.

    @param var Variable to be pickled
    @param path Directory to cache the variable in
    @param name Name of the file
    """
    logger.debug(f"Pickle: Attempting to load {path}/{name}")

    # Variables
    output_f = path / Path(name)

    # If the 'pkl' suffix was not provided or too many suffixes were provided
    output_f = __checkSuffix(output_f)

    # Create the directory if it does not exist
    path.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_f, "wb") as f:
            # Attempt to create the cached variable
            pickle.dump(var, f, pickle.DEFAULT_PROTOCOL)

            # Verify creation
            if not output_f.exists():
                raise Exception(f"ERROR: PICKLING DID NOT CREATE THE FILE: {f}")

            logger.debug("Pickle: Successfully loaded")

    except Exception as e:
        # Print exception
        logger.warning(f"Pickle: UNABLE TO CACHE {name} AT THE LOCATION {output_f}")
        raise e

    return


##======================================================================================================================
#
def unPickleVar(path: Path, name: str) -> Any:
    """!
    @brief The cache variable function caches `var` in `path` by pickling the data.

    @param path Directory to cache the variable in
    @param name Name of the file to load

    @return var The loaded cached pickle file
    """
    logger.debug(f"Pickle: Attempting write to {path}/{name}")

    # Variables
    var: Any = None
    output_f = path / Path(name)

    # If the 'pkl' suffix was not provided or too many suffixes were provided
    output_f = __checkSuffix(output_f)

    try:
        with open(output_f, "rb") as f:
            # If the 'pkl' suffix was not provided or too many suffixes were provided
            output_f = __checkSuffix(output_f)

            # Attempt to create the cached variable
            var = pickle.load(f)

            logger.debug("Pickle: Successfully written")

    except Exception as e:
        # Print exception
        logger.warning(f"Pickle: UNABLE TO READ {name} FROM THE LOCATION {output_f}")
        raise e

    return var


##======================================================================================================================
#
def deleteCacheVar(path: Path, name: str):
    """!
    @brief Delete the cached variable.

    @param p Path to the cache variable.
    """
    logger.debug(f"Cache: Deleting cached variable {path}/{name}")

    try:
        # Construct the path
        cached_f = path / Path(name)

        # If the 'pkl' suffix was not provided or too many suffixes were provided
        cached_f = __checkSuffix(cached_f)

        # Delete the cached variable
        cached_f.unlink(missing_ok=True)

        logger.debug("Cache: Successfully deleted")

    except Exception as e:
        # Print exception
        logger.warning(f"Cache: UNABLE TO REMOVE {name} FROM THE LOCATION {cached_f}")
        raise e

    return


##======================================================================================================================
#
def __checkSuffix(p: Path) -> Path:
    """!
    @brief Check the suffix of the file provided, and add the correct 'pkl' suffix if necessary.

    @param p Path to the cache variable.

    @return Path to the cache variable with the correct 'pkl' suffix.
    """
    return p.with_suffix(".pkl")
