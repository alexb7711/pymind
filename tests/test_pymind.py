import unittest
import pymind
from pathlib import Path

########################################################################################################################


class TestPyMindCore(unittest.TestCase):
    INPUT = "./tests/example"

    ##==================================================================================================================
    #
    def getPM(self):
        pm = pymind.PyMind(**{"input": TestPyMindCore.INPUT, "output": ""})
        return pm

    ##==================================================================================================================
    #
    def assertIsFile(self, path):
        if not Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))

    ##==================================================================================================================
    #
    def test_cache_directory_creation(self):
        pm = self.getPM()
        pm.run()

        self.assertIsFile(f"{Path.home()}/.cache/pymind/example_cache.json")

    ##==================================================================================================================
    #
    def test_found_project_name(self):
        pm = self.getPM()
        pm.run()

        # Check the project name
        self.assertEqual("example", pm.project_name)
        return

    ##==================================================================================================================
    #
    def test_find_files(self):
        pm = self.getPM()
        pm.run()

        # Check the input file
        self.assertEqual(pm.input, TestPyMindCore.INPUT)

        # Check the number of elements
        self.assertEqual(len(pm.files_found), 4)

        return

    ##==================================================================================================================
    #
    def test_modified_files(self):
        pm = self.getPM()
        pm.run()  # Run one extra time to make sure the cache file exists
        pm.run()

        # Unmodified project
        self.assertEqual(len(pm.build_files), 0)

        # Modify a file
        Path("./tests/example/file1.md").touch()
        pm.run()
        self.assertEqual(len(pm.build_files), 1)
        self.assertEqual(pm.build_files[0].name, "file1.md")

        return
