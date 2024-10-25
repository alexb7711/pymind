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
        # Attempt to create the cached variable
        with open(var, "wb") as f:
            output_f = path / Path(name)

            ## If a suffix was not added
            if not output_f.suffixes:
                ### Add the suffix
                output_f = output_f + ".pkl"

            pickle.dump(var, f)
    except Exception as e:
        # Print exception
        print(f"UNABLE TO CACHE {name} AT THE LOCATION {path}")
        print("EXCEPTION: ", e)

        # Indicate a failure
        success = False

    return success


##======================================================================================================================
#
def deCacheVar(var: Any, path: Path, name: str) -> (bool, Any):
    """!
    @brief The cache variable function caches `var` in `path` by pickling the data.

    @param var Variable to be pickled
    @param path Directory to cache the variable in
    @param name Name of the file to load

    @return True is successful, False otherwise
    """
    success: bool = True
    var: Any = None

    try:
        # Attempt to create the cached variable
        with open(var, "rb") as f:
            output_f = path / Path(name)

            ## If a suffix was not added
            if not output_f.suffixes:
                ### Add the suffix
                output_f = output_f + ".pkl"

            pickle.load(dsuccessict, f)
    except Exception as e:
        # Print exception
        print(f"UNABLE TO READ {name} FROM THE LOCATION {path}")
        print("EXCEPTION: ", e)

        # Indicate a failure
        success = False

    return (success, var)
