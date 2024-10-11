import unittest
import pymind
from pathlib import Path
import os, glob

########################################################################################################################


class TestTagsPage(unittest.TestCase):
    INPUT = "./tests/example"
    OUTPUT = "./tests/example-output"

    ##==================================================================================================================
    #
    def getPM(self, force: bool = False, dry_run: bool = False):
        pm = pymind.PyMind(
            **{
                "input": TestTagsPage.INPUT,
                "output": TestTagsPage.OUTPUT,
                "force": force,
                "dry_run ": dry_run,
            }
        )
        return pm

    ##==================================================================================================================
    #
    def deleteTagsFile(self):
        Path(f"{TestTagsPage.INPUT}/tags_page.md").unlink()

    ##==================================================================================================================
    #
    def test_file_creation(self):
        pm = self.getPM(force=True)
        pm.run()

        # Ensure the tags file is created
        self.assertTrue(
            Path(f"{TestTagsPage.INPUT}/tags_page.md").exists(),
            "The tags page was not created!",
        )

        # Verify the tags file was converted
        self.assertTrue(
            Path(f"{TestTagsPage.OUTPUT}/tags_page.html").exists(),
            "The tags page was not converted!",
        )

        # Delete the tags file page
        self.deleteTagsFile()

        return
