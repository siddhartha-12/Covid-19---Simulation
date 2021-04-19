import unittest
import os
import sys
cwd = os.getcwd()+"/src/main"
sys.path.insert(1, cwd)
from ConfigUtil import ConfigUtil

class ConfigUtilClassTest(unittest.TestCase):

    def setUp(self):
        self.conf = ConfigUtil.get_instance()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
