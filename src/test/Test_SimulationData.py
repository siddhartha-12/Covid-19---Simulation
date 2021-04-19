import os
import sys
cwd = os.getcwd()+"/src/main"
sys.path.insert(1,cwd)
import unittest
from Config import Config
from SimulationData import SimalationData

class ConfigTest(unittest.TestCase):

    def setUp(self):
        self.sd = SimalationData()
        self.config = Config.get_instance()
        self.config.load_from_file("COVID19")
        self.data = None
    
    def testPopulationCount(self):
        population = self.config.get_population()
        self.data = self.sd.initializePersonDataset(population)
        self.assertTrue(len(self.data)==population)
    
    def testInfectInitial(self):
        self.sd.generateDataset()
        count = self.sd.infect_initial()
        self.assertTrue(count>0)


if __name__ == "__main__":
	unittest.main()
	