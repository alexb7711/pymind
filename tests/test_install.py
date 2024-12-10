import os
import subprocess

class TestInstall(unittest.TestCase):

    ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent

    ##==================================================================================================================
    #
    def test_pip_install(self):
        process = subprocess.run(["make", "install"])
        process.check_returncode()
        return
