import unittest
import os
import sys
cwd = os.getcwd()+"/src/main"
sys.path.insert(1, cwd)
from Config import Config
from ConfigUtil import ConfigUtil

class ConfigClassTest(unittest.TestCase):

    def setUp(self):
        self.conf = Config.get_instance()

    # Test if config object is created
    def testConfigObjectCreation(self):
        self.assertTrue(self.conf)

    # Test if default values are set
    def testDefaultValues(self):
        self.assertTrue(self.conf.get_property_name() == None)

    # Test get and set property name
    def test_property_name(self):
        self.conf.set_property_name("Test")
        self.assertTrue(self.conf.get_property_name()=="Test")

    # Test get and set population
    def test_population(self):
        self.conf.set_population(1000)
        self.assertTrue(self.conf.get_population() == 1000)

    # Test get and set initial infected percentage
    def test_initial_infected_percentage(self):
        self.conf.set_initial_infected_percentage(10)
        self.assertTrue(self.conf.get_initial_infected_percentage()==10)

    # Test get and set R factor
    def test_r_factor(self):
        self.conf.set_r_factor(3)
        self.assertTrue(self.conf.get_r_factor()==3)

    # Test get and set K factor
    def test_k_factor(self):
        self.conf.set_k_factor(1)
        self.assertTrue(self.conf.get_k_factor()==1)

    # Test get and set Days Contagious
    def test_days_contageous(self):
        self.conf.set_days_contageous(30)
        self.assertTrue(self.conf.get_days_contageous()==30)

    # Test get and set mask introduced timeline
    def test_mask_introduced_timeline(self):
        self.conf.set_mask_introduced_timeline(50)
        self.assertTrue(self.conf.get_mask_introduced_timeline()==50)

    # Test get and set mask usage effectiveness
    def test_mask_usage_effectiveness(self):
        self.conf.set_mask_usage_effectiveness(50)
        self.assertTrue(self.conf.get_mask_usage_effectiveness()==50)

    # Test get and set mask usage percentage
    def test_mask_usage_percentage(self):
        self.conf.set_mask_usage_percentage(50)
        self.assertTrue(self.conf.get_mask_usage_percentage()==50)

    # Test get and set quarantine introduced timeline
    def test_quarantine_introduced_timeline(self):
        self.conf.set_quarantine_introduced_timeline(50)
        self.assertTrue(self.conf.get_quarantine_introduced_timeline()==50)

    # Test get and set quarantine effectiveness
    def test_qurantine_effectiveness(self):
        self.conf.set_qurantine_effectiveness(50)
        self.assertTrue(self.conf.get_qurantine_effectiveness()==50)

    # Test get and set quarantine percentage
    def test_qurantine_usage_percentage(self):
        self.conf.set_qurantine_usage_percentage(50)
        self.assertTrue(self.conf.get_qurantine_usage_percentage()==50)

    # Test get and set vaccine introduced timeline
    def test_vaccine_introduced_timeline(self):
        self.conf.set_vaccine_introduced_timeline(50)
        self.assertTrue(self.conf.get_vaccine_introduced_timeline()==50)

    # Test get and set vaccine effectiveness
    def test_vaccine_effectiveness(self):
        self.conf.set_vaccine_effectiveness(50)
        self.assertTrue(self.conf.get_vaccine_effectiveness()==50)

    # Test get and set vaccine percentage
    def test_vaccine_usage_percentage(self):
        self.conf.set_vaccine_usage_percentage(50)
        self.assertTrue(self.conf.get_vaccine_usage_percentage()==50)

    # Test total to infect
    def test_total_to_infect(self):
        self.conf.set_total_to_infect(10)
        self.assertTrue(self.conf.get_total_to_infect()==10)

    # Test if config values are loaded from config.cfg file
    def test_load_from_file(self):
        factor = 1
        cu = ConfigUtil.get_instance()
        self.conf.load_from_file("COVID19")
        disease_section = "COVID19"
        self.assertTrue(self.conf.get_property_name()==(disease_section))
        self.assertTrue(self.conf.get_population()==(int(cu.get_value("SIMULATION","population"))))
        self.assertTrue(self.conf.get_initial_infected_percentage()==(int(cu.get_value("SIMULATION","initial_infected_percentage"))))
        self.assertTrue(self.conf.get_r_factor()==(int(cu.get_value(disease_section,"r_factor"))))
        self.assertTrue(self.conf.get_k_factor()==(float(cu.get_value(disease_section,"k_factor"))))
        self.assertTrue(self.conf.get_days_contageous()==(int(cu.get_value(disease_section,"days_contageous"))*factor))
        self.assertTrue(self.conf.get_mask_introduced_timeline()==(int(cu.get_value(disease_section,"mask_timeline"))*factor))
        self.assertTrue(self.conf.get_mask_usage_effectiveness()==(float(cu.get_value(disease_section,"mask_usuage_effectiveness"))))
        self.assertTrue(self.conf.get_mask_usage_percentage()==(float(cu.get_value(disease_section,"mask_usuage_percentage"))))
        self.assertTrue(self.conf.get_quarantine_introduced_timeline()==(int(cu.get_value(disease_section,"quarantine_timeline"))*factor))
        self.assertTrue(self.conf.get_qurantine_effectiveness()==(float(cu.get_value(disease_section,"qurantine_effectiveness"))))
        self.assertTrue(self.conf.get_qurantine_usage_percentage()==(float(cu.get_value(disease_section,"qurantine_percentage"))))
        self.assertTrue(self.conf.get_vaccine_introduced_timeline()==(int(cu.get_value(disease_section,"vaccine_timeline"))*factor))
        self.assertTrue(self.conf.get_vaccine_effectiveness()==(float(cu.get_value(disease_section,"vaccine_effectiveness"))))
        self.assertTrue(self.conf.get_vaccine_usage_percentage()==(float(cu.get_value(disease_section,"vaccinated_percentage"))))
     
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()