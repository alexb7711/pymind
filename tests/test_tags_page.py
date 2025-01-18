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
            tags_page_md.exists(),
            f"The tags page was not created: {tags_page_md}",
        )

        # Verify the tags file was converted
        tags_page_html = Path(f"{TestTagsPage.OUTPUT}/tags_page.html")
        self.assertTrue(
            tags_page_html.exists(),
            f"The tags HTML file was not created: {tags_page_html}",
        )

        # Delete the tags file page
        self.deleteTagsFile()

        return

    ##==================================================================================================================
    #
    def test_tag_removal(self):
        import re

        pm = self.getPM(force=True)
        pm.run()

        # Ensure all of the tags have been stripped
        for file in Path(pm.output).glob("*.html"):
            with open(file, "r") as f:
                t = f.read()
                regex = re.compile(r"^<!--\s*:?(.*?):\s*-->", flags=re.DOTALL)
                match = regex.search(t)
                self.assertEqual(match, None)

        return
