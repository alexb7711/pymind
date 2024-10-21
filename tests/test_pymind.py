import unittest
import pymind
from pathlib import Path
import os, glob
import platform

########################################################################################################################


class TestPyMindCore(unittest.TestCase):
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
                "input": TestPyMindCore.INPUT,
                "output": TestPyMindCore.OUTPUT,
                "force": force,
                "engine": False,
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

        cache_dir = Path(f"{TestPyMindCore.CACHE_PATH}/")

        return cache_dir

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

        cache_d = self.createCachePaths()

        path = cache_d / Path("example_cache.json")

        self.assertIsFile(path)

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
        self.assertEqual(pm.input, Path(TestPyMindCore.INPUT))

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

        self.assertEqual(pm.config_file, Path("./tests/config/pymind/pymind.yml"))
        self.assertEqual(pm.project_name, "example")
        self.assertEqual(pm.input, Path("./tests/example"))

        return

    ##==================================================================================================================
    #
    def test_html_output_cnt(self):
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
        k = [x for x in k]
        v = pm.tags.values()
        v = [Path(x[0]).name for x in v]

        self.assertEqual(k, ["tag1", "tag2", "tag3", "tag4", "tag5"])
        self.assertEqual(v, ["tags.md", "tags.md", "tags.md", "tags.md", "tags.md"])

        return

    ##==================================================================================================================
    #
    def test_dry_run(self):
        # Run PyMind with `dry_run = true` to only process the files, but convert anything
        pm = self.getPM(dry_run=True)
        pm.run()

        # Delete the OUTPUT directory if it exists
        self.recursive_delete(Path(TestPyMindCore.OUTPUT))

        # Count the number of files output
        fc = len(glob.glob(os.path.join(TestPyMindCore.OUTPUT, "*")))
        self.assertEqual(fc, 0)

        return

    ##==================================================================================================================
    #
    def test_work_directory_creation(self):
        # Run PyMind with `dry_run = true` to only process the files, but convert anything
        pm = self.getPM()
        pm.run()

        # Get path to the cache directory
        cache_d = self.createCachePaths()
        work_d = cache_d / Path("example")

        self.assertTrue(work_d.is_dir(), "The working directory was not created!")

        return
