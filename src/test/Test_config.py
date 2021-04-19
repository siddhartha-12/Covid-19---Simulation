import unittest
import os
import sys
cwd = os.getcwd()+"/src/main"
sys.path.insert(1, cwd)
from Config import Config

class ConfigClassTest(unittest.TestCase):

    def setUp(self):
        self.conf = Config.get_instance()

    def testConfigObjectCreation(self):
        self.assertTrue(self.conf)

    def testDefaultValues(self):
        # self.assertTrue()
        self.assertTrue(self.conf.get_property_name() == None)

    def test_property_name(self):
        self.conf.set_property_name("Test")
        self.assertTrue(self.conf.get_property_name()=="Test")

    def test_population(self):
        self.conf.set_population(1000)
        self.assertTrue(self.conf.get_population() == 1000)

    def test_initial_infected_percentage(self):
        self.conf.set_initial_infected_percentage(10)
        self.assertTrue(self.conf.get_initial_infected_percentage()==10)

    def test_r_factor(self):
        self.conf.set_r_factor(3)
        self.assertTrue(self.conf.get_r_factor()==3)

    def test_k_factor(self):
        self.conf.set_k_factor(1)
        self.assertTrue(self.conf.get_k_factor()==1)

    def test_days_contageous(self):
        self.conf.set_days_contageous(30)
        self.assertTrue(self.conf.get_days_contageous()==30)

    def test_mask_introduced_timeline(self):
        self.conf.set_mask_introduced_timeline(50)
        self.assertTrue(self.conf.get_mask_introduced_timeline()==50)

    def test_mask_usage_effectiveness(self):
        self.conf.set_mask_usage_effectiveness(50)
        self.assertTrue(self.conf.get_mask_usage_effectiveness()==50)

    def test_mask_usage_percentage(self):
        self.conf.set_mask_usage_percentage(50)
        self.assertTrue(self.conf.get_mask_usage_percentage()==50)

    def test_quarantine_introduced_timeline(self):
        self.conf.set_quarantine_introduced_timeline(50)
        self.assertTrue(self.conf.get_quarantine_introduced_timeline()==50)

    def test_qurantine_effectiveness(self):
        self.conf.set_qurantine_effectiveness(50)
        self.assertTrue(self.conf.get_qurantine_effectiveness()==50)

    def test_qurantine_usage_percentage(self):
        self.conf.set_qurantine_usage_percentage(50)
        self.assertTrue(self.conf.get_qurantine_usage_percentage()==50)

    def test_vaccine_introduced_timeline(self):
        self.conf.set_vaccine_introduced_timeline(50)
        self.assertTrue(self.conf.get_vaccine_introduced_timeline()==50)

    def test_vaccine_effectiveness(self):
        self.conf.set_vaccine_effectiveness(50)
        self.assertTrue(self.conf.get_vaccine_effectiveness()==50)

    def test_vaccine_usage_percentage(self):
        self.conf.set_vaccine_usage_percentage(50)
        self.assertTrue(self.conf.get_vaccine_usage_percentage()==50)

    def test_total_to_infect(self):
        self.conf.set_total_to_infect(10)
        self.assertTrue(self.conf.get_total_to_infect()==10)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
