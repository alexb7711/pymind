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
    def deleteTagsFile(self):
        Path(f"{TestLandingPage.INPUT}/index.md").unlink(missing_ok=True)
        Path(f"{self.createCachePaths()}/example/index.md").unlink(missing_ok=True)

    ##==================================================================================================================
    #
    def test_file_creation(self):
        pm = self.getPM(force=True)
        pm.run()

        # Get the cache path
        cache_d = self.createCachePaths()
        index_md = cache_d / Path("example/index.md")

        # Ensure the tags file is created
        self.assertTrue(
            index_md.exists(),
            f"The tags page was not created: {index_md}",
        )

        # Verify the tags file was converted
        index_html = Path(f"{TestLandingPage.OUTPUT}/index.html")
        self.assertTrue(
            index_html.exists(),
            f"The tags HTML file was not created: {index_html}",
        )

        # Delete the tags file page
        self.deleteTagsFile()

        return
