import unittest
import os
import sys
cwd = os.getcwd()+"/src/main"
sys.path.insert(1, cwd)
from DataUtil import DataUtil
from SimulationData import SimalationData
from Config import Config

class ConfigClassTest(unittest.TestCase):

    def setUp(self):
            self.du = DataUtil()
            self.cu = Config.get_instance()
            self.sd= SimalationData()
            self.dataset = self.sd.getDataset()

# Test to validate locations of infected person
    def testGetLocationInfected(self):
        data = self.du.getLocationInfected(self.dataset)
        flag = True
        pid = data[2]
        for i in pid:
            if self.dataset[i].get_infected() is not True:
                flag = False
        self.assertTrue(flag)

# Test to validate locations of Healthy person
    def testGetLocationHealthy(self):
        data = self.du.getLocationHealthy(self.dataset)
        flag = True
        pid = data[2]
        for i in pid:
            if self.dataset[i].get_infected() is True:
                flag = False
        self.assertTrue(flag)

 # Test to validate locations of Recovered person
    def testGetLocationRecovered(self):
        data = self.du.getLocationRecovered(self.dataset)
        flag = True
        pid = data[2]
        for i in pid:
            if self.dataset[i].get_recovered() is not True:
                flag = False
        self.assertTrue(flag)

# Test to validate locations of Vaccinated person
    def testGetLocationVaccincated(self):
        data = self.du.getLocationVaccincated(self.dataset)
        flag = True
        pid = data[2]
        for i in pid:
            if self.dataset[i].get_vaccinated() is not True:
                flag = False
        self.assertTrue(flag)

 # Test to validate locations of people with mask
    def testGetLocationOfMaskedPerson(self):
        data = self.du.getLocationOfMaskedPerson(self.dataset)
        flag = True
        pid = data[2]
        for i in pid:
            if self.dataset[i].get_mask_usage() is not True:
                flag = False
        self.assertTrue(flag)

 # Test to validate locations of people in Quarantine
    def testGetLocationOfQuarantinedPerson(self):
        data = self.du.getLocationOfQuarantinedPerson(self.dataset)
        flag = True
        pid = data[2]
        for i in pid:
            if self.dataset[i].get_mask_usage() is not True:
                flag = False
        self.assertTrue(flag)

if __name__ == "__main__":
	unittest.main()