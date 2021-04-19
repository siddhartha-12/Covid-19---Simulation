import unittest
import os
import sys
cwd = os.getcwd()+"/src/main"
sys.path.insert(1, cwd)
from ConfigUtil import ConfigUtil

class ConfigUtilClassTest(unittest.TestCase):
    
    # Test case Constructor setup
    def setUp(self): 
        self.conf = ConfigUtil.get_instance()

    # Testing whether the object is created
    def testConfigObjectCreation(self):
        self.assertTrue(self.conf)

    # Testing if config values is being fetched from config.cfg file
    def test_get_value(self):
        test = self.conf.get_value("SIMULATION","population")
        self.assertTrue(test != None )
    
    # Testing if config file is getting loaded
    def test_load_config(self):
        self.assertTrue(self.conf.load_config())

    # Testing if we can retrieve all sections
    def test_get_all_sections(self):        
        sectionList = self.conf.get_all_sections()
        self.assertTrue(len(sectionList)>0)

if __name__ == "__main__":\
    unittest.main()
