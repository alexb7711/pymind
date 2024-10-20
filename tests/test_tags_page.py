import glob
import os
import platform
import unittest
from pathlib import Path

import pymind

########################################################################################################################


class TestTagsPage(unittest.TestCase):
    ####################################################################################################################
    # CONSTANTS
    ####################################################################################################################
    INPUT = Path("./tests/example")
    OUTPUT = Path("./tests/example-output")

    CORE_ENGINE_PATH = Path("pymind/engine/")

    # Select cache directory location based on the operating system
    CACHE_DIR = Path(".cache/pymind")
    CONF_DIR = Path(".config/pymind")

    if platform.system() == "Windows":
        CACHE_DIR = Path("AppData\Local\Programs\pymind\cache")
        CONF_DIR = Path("AppData\Local\Programs\pymind")
        TMP_DIR = Path(f"{Path.home()}\AppData\Local\Temp")

    CONFIG_FILE = "pymind.yaml"
    CONFIG_PATH = Path(f"{Path.home()}/{CONF_DIR}/{CONFIG_FILE}")
    CACHE_PATH = Path(f"{Path.home()}/{CACHE_DIR}")

    ##==================================================================================================================
    #
    def getPM(self, force: bool = False, dry_run: bool = False):
        pm = pymind.PyMind(
            **{
                "input": str(TestTagsPage.INPUT),
                "output": str(TestTagsPage.OUTPUT),
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

        cache_dir = Path(f"{TestTagsPage.CACHE_PATH}/")

        return cache_dir

    ##==================================================================================================================
    #
    def deleteTagsFile(self):
        Path(f"{TestTagsPage.INPUT}/tags_page.md").unlink(missing_ok=True)
        Path(f"{self.createCachePaths()}/example/tags_page.md").unlink(missing_ok=True)

    ##==================================================================================================================
    #
    def test_file_creation(self):
        pm = self.getPM(force=True)
        pm.run()

        # Get the cache path
        cache_d = self.createCachePaths()
        tags_page_md = cache_d / Path("example/tags_page.md")

        # Ensure the tags file is created
        self.assertTrue(
            # Path(f"{TestTagsPage.INPUT}/tags_page.md").exists(),
            tags_page_md.exists(),
            f"The tags page was not created: {tags_page_md}",
        )

        # Verify the tags file was converted
        tags_page_html = Path(f"{TestTagsPage.OUTPUT}/tags_page.html").exists()
        self.assertTrue(
            tags_page_html, f"The tags HTML file was not created: {tags_page_html}"
        )

        # Delete the tags file page
        self.deleteTagsFile()

        return
