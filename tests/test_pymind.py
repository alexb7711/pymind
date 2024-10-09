import unittest
import pymind
from pathlib import Path

########################################################################################################################


class TestPyMindCore(unittest.TestCase):
    INPUT = "./tests/example"
    OUTPUT = "./tests/example-output"

    ##==================================================================================================================
    #
    def getPM(self, force: bool = False):
        pm = pymind.PyMind(
            **{
                "input": TestPyMindCore.INPUT,
                "output": TestPyMindCore.OUTPUT,
                "force": force,
            }
        )
        return pm

    ##==================================================================================================================
    #
    def assertIsFile(self, path):
        if not Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))

    ##==================================================================================================================
    #
    def recursive_delete(self, directory):
        import pathlib

        for path in directory.rglob("*"):
            if path.is_file():
                path.unlink()
            elif path.is_dir(missing_ok=True):
                recursive_delete(path)
                path.rmdir()

        return

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
        self.assertEqual(len(pm.files_found), 5)

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

    ##==================================================================================================================
    #
    def test_load_config_file(self):
        import os

        dir_path = os.path.dirname(os.path.realpath("."))

        pm = pymind.PyMind(**{"config": "./tests/config/pymind/pymind.yml"})
        pm.run()

        self.assertEqual(pm.config_file, "./tests/config/pymind/pymind.yml")
        self.assertEqual(pm.project_name, "example")
        self.assertEqual(pm.input, "./tests/example")

        return

    ##==================================================================================================================
    #
    def test_html_output_cnt(self):
        import os, glob

        # Delete the OUTPUT directory if it exists
        self.recursive_delete(Path(TestPyMindCore.OUTPUT))

        # Run PyMind with `force = false` to generate all the files
        pm = self.getPM()
        Path("./tests/example/file2.md").touch()
        pm.run()

        # Count the number of files output
        fc = len(glob.glob(os.path.join(TestPyMindCore.OUTPUT, "*")))
        self.assertEqual(fc, 1)

        return

    ##==================================================================================================================
    #
    def test_force_html_output_cnt(self):
        import os, glob

        # Delete the OUTPUT directory if it exists
        self.recursive_delete(Path(TestPyMindCore.OUTPUT))

        # Run PyMind with `force = true` to generate all the files
        pm = self.getPM(force=True)
        pm.run()

        # Count the number of files output
        fc = len(glob.glob(os.path.join(TestPyMindCore.OUTPUT, "*")))
        self.assertEqual(fc, 5)

        return

    ##==================================================================================================================
    #
    def test_tag_search(self):
        # Run PyMind with `force = true` to generate all the files
        pm = self.getPM(force=True)
        pm.run()

        # Verify the tag output
        k = pm.tags.keys()
        v = pm.tags.values()
        print(f"====>{v}")
        v = [Path(x).name for x in v]

        self.assertEqual(k, ["tag1", "tag2", "tag3", "tag4", "tag5"])
        self.assertEqual(v, [ ["tags.md"], ["tags.md"], ["tags.md"], ["tags.md"], ["tags.md"] ])

        return
