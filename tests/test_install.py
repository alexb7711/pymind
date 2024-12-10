import os
import subprocess
import unittest
from pathlib import Path

########################################################################################################################

class TestInstall(unittest.TestCase):

    ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent

    ##==================================================================================================================
    #
    def test_pip_install(self):
        process = subprocess.run(["make", "install"])
        process.check_returncode()
        return

    ##==================================================================================================================
    #
    def test_execute_pymind(self):
        os.chdir(r"tests/")

        process = subprocess.run(["pymind", "-f", "-i", "example", "-o", "pymind-output"])
        process.check_returncode()
        return
