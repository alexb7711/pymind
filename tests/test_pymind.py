import unittest
import pymind

########################################################################################################################


class TestPyMindCore(unittest.TestCase):
    ##==================================================================================================================
    #
    def test_find_files(self):
        input = "./tests/example"
        pm = pymind.PyMind(**{"input": input, "output": ""})

        pm.run()

        # Check the input file
        self.assertEqual(pm.input, input)

        # Check the number of elements
        self.assertEqual(len(pm.files_found), 4)

        return
