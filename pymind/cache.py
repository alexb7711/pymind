"""!
@file cache.py

@module The `cache.py` module is a helper module to set and retrieve cached variables that may be useful to
plugin generating scripts.
"""

import pickle
from pathlib import Path
from typing import Any


##======================================================================================================================
#
def cacheVar(var: Any, path: Path, name: str) -> bool:
    """!
    @brief The cache variable function caches `var` in `path` by pickling the data.

    @param var Variable to be pickled
    @param path Directory to cache the variable in
    @param name Name of the file

    @return True is successful, False otherwise
    """
    success: bool = True

    try:
        # Construct the path
        output_f = path / Path(name)

        # Create the directory if it does not exist
        path.mkdir(parents=True, exist_ok=True)

        # If the 'pkl' suffix was not provided or too many suffixes were provided
        output_f = __checkSuffix(output_f)

        print(f"OUTPUT====> {output_f}")

        # Attempt to create the cached variable
        pickle.dump(var, open(output_f, "wb"))

    except Exception as e:
        # Print exception
        print(f"UNABLE TO CACHE {name} AT THE LOCATION {output_f}")
        print("EXCEPTION: ", e)

        # Indicate a failure
        success = False

    return success


##======================================================================================================================
#
def deCacheVar(path: Path, name: str) -> (bool, Any):
    """!
    @brief The cache variable function caches `var` in `path` by pickling the data.

    @param var Variable to be pickled
    @param path Directory to cache the variable in
    @param name Name of the file to load

    @return True is successful, False otherwise
    """
    # Variables
    success: bool = True
    var: Any = None

    try:
        # Construct the path
        output_f = path / Path(name)

        # If the 'pkl' suffix was not provided or too many suffixes were provided
        output_f = __checkSuffix(output_f)

        # Attempt to create the cached variable
        var = pickle.load(open(output_f, "rb"))

    except Exception as e:
        # Print exception
        print(f"UNABLE TO READ {name} FROM THE LOCATION {output_f}")
        print("EXCEPTION: ", e)

        # Indicate a failure
        success = False


        return (success, var)
##======================================================================================================================
#
def deleteCacheVar(path: Path, name, str):
    """!
    @brief Delete the cached variable.

    @param p Path to the cache variable.

    @return Path to the cache variable with the correct 'pkl' suffix.
    """
    # Variables
    success = True

    try:
        # Construct the path
        cached_f = path / Path(name)

        # If the 'pkl' suffix was not provided or too many suffixes were provided
        cached_f = __checkSuffix(output_f)

        # Delete the cached variable
        cached_f.unlink()

    except Exception as e:
        # Print exception
        print(f"UNABLE TO REMOVE {name} FROM THE LOCATION {output_f}")
        print("EXCEPTION: ", e)

    return success

##======================================================================================================================
#
def __checkSuffix(p: Path) -> Path:
    """!
    @brief Check the suffix of the file provided, and add the correct 'pkl' suffix if necessary.

    @param p Path to the cache variable.

    @return Path to the cache variable with the correct 'pkl' suffix.
    """
    return p.with_suffix(".pkl")
