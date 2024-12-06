import glob
import os
import platform
import unittest
from pathlib import Path

import pymind

########################################################################################################################


class TestLandingPage(unittest.TestCase):
    ####################################################################################################################
    # CONSTANTS
    ####################################################################################################################
    INPUT = "./tests/example"
    OUTPUT = "./tests/example-output"

    CORE_ENGINE_PATH = "pymind/engine/"

    # Select cache directory location based on the operating system
    CACHE_DIR = ".cache/pymind"
    CONF_DIR = ".config/pymind"

    if platform.system() == "Windows":
        CACHE_DIR = Path("AppData\Local\Programs\pymind\cache")
        CONF_DIR = Path("AppData\Local\Programs\pymind")

    CONFIG_FILE = "pymind.yaml"
    CONFIG_PATH = f"{Path.home()}/{CONF_DIR}/{CONFIG_FILE}"
    CACHE_PATH = f"{Path.home()}/{CACHE_DIR}"

    ##==================================================================================================================
    #
    def getPM(self, force: bool = False, dry_run: bool = False):
        pm = pymind.PyMind(
            **{
                "input": str(TestLandingPage.INPUT),
                "output": str(TestLandingPage.OUTPUT),
                "force": force,
                "dry_run ": dry_run,
            }
        )
        return pm

    ##==================================================================================================================
    #
    def createCachePaths(self):
        """!
        @brief Create `Path` objects for cache

        This method creates the cache file paths, and ensures that the path to the cache directory exists.

        @return Returns tuple of strings (cache_dir, cache_file)
        """

        cache_dir = Path(f"{TestLandingPage.CACHE_PATH}/")

        return cache_dir

    ##==================================================================================================================
    #
    def test_file_creation(self):
        import re

        pm = self.getPM(force=True)
        pm.run()

        # Check that each file has a footer
        for file in Path(pm.output).glob("*.html"):
            with open(file, "r") as f:
                t = f.read()
                regex = re.compile('<div id="navigation">.*</div>', flags=re.DOTALL)
                match = regex.search(t)
                self.assertNotEqual(match, None)

        return
