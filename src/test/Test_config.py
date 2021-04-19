from Config import Config
import unittest
import os
import sys
cwd = os.getcwd()+"/src/main"
sys.path.insert(1, cwd)


class ConfigClassTest(unittest.TestCase):

    def setUp(self):
        self.conf = Config.get_instance()

    def testConfigObjectCreation(self):
        self.assertTrue(self.conf)

    def testDefaultValues(self):
        # self.assertTrue()
        self.assertTrue(self.conf.get_property_name() == None)

    def test_set_property_name(self, property_name):
        self.conf.set_property_name("Test"))
        self.assertTrue(self.conf.get_property_name()=="Test")


    def test_get_population(self):
        self.conf.set.conf.get_population())


    def test_set_population(self, population):
        self.assertTrue(
            self.conf.set_population(population))


    def test_get_initial_infected_percentage(self):
        self.assertTrue(
            self.conf.get_initial_infected_percentage())


    def test_set_initial_infected_percentage(self, initial_infected_percentage):
        self.assertTrue(
            self.conf.set_initial_infected_percentage(initial_infected_percentage))


    def test_get_r_factor(self):
        self.conf.set.conf.get_r_factor())


    def test_set_r_factor(self, r_factor):
        self.assertTrue(
            self.conf.set_r_factor(r_factor))


    def test_get_k_factor(self):
        self.conf.set.conf.get_k_factor())


    def test_set_k_factor(self, k_factor):
        self.assertTrue(
            self.conf.set_k_factor(k_factor))


    def test_get_days_contageous(self):
        self.conf.set.conf.get_days_contageous())


    def test_set_days_contageous(self, days_contageous):
        self.assertTrue(
            self.conf.set_days_contageous(days_contageous))


    def test_get_mask_introduced_timeline(self):
        self.assertTrue(
            self.conf.get_mask_introduced_timeline())


    def test_set_mask_introduced_timeline(self, mask_introduced_timeline):
        self.assertTrue(
            self.conf.set_mask_introduced_timeline(mask_introduced_timeline))


    def test_get_mask_usage_effectiveness(self):
        self.assertTrue(
            self.conf.get_mask_usage_effectiveness())


    def test_set_mask_usage_effectiveness(self, mask_usage_effectiveness):
        self.assertTrue(
            self.conf.set_mask_usage_effectiveness(mask_usage_effectiveness))


    def test_get_mask_usage_percentage(self):
        self.assertTrue(
            self.conf.get_mask_usage_percentage())


    def test_set_mask_usage_percentage(self, mask_usage_percentage):
        self.assertTrue(
            self.conf.set_mask_usage_percentage(mask_usage_percentage))


    def test_get_quarantine_introduced_timeline(self):
        self.assertTrue(
            self.conf.get_quarantine_introduced_timeline())


    def test_set_quarantine_introduced_timeline(self, quarantine_introduced_timeline):
        self.assertTrue(
            self.conf.set_quarantine_introduced_timeline(quarantine_introduced_timeline))


    def test_get_qurantine_effectiveness(self):
        self.assertTrue(
            self.conf.get_qurantine_effectiveness())


    def test_set_qurantine_effectiveness(self, qurantine_effectiveness):
        self.assertTrue(
            self.conf.set_qurantine_effectiveness(qurantine_effectiveness))


    def test_get_qurantine_usage_percentage(self):
        self.assertTrue(
            self.conf.get_qurantine_usage_percentage())


    def test_set_qurantine_usage_percentage(self, qurantine_usage_percentage):
        self.assertTrue(
            self.conf.set_qurantine_usage_percentage(qurantine_usage_percentage))


    def test_get_vaccine_introduced_timeline(self):
        self.assertTrue(
            self.conf.get_vaccine_introduced_timeline())


    def test_set_vaccine_introduced_timeline(self, vaccine_introduced_timeline):
        self.assertTrue(
            self.conf.set_vaccine_introduced_timeline(vaccine_introduced_timeline))


    def test_get_vaccine_effectiveness(self):
        self.assertTrue(
            self.conf.get_vaccine_effectiveness())


    def test_set_vaccine_effectiveness(self, vaccine_effectiveness):
        self.assertTrue(
            self.conf.set_vaccine_effectiveness(vaccine_effectiveness))


    def test_get_vaccine_usage_percentage(self):
        self.assertTrue(
            self.conf.get_vaccine_usage_percentage())


    def test_set_vaccine_usage_percentage(self, vaccine_usage_percentage):
        self.assertTrue(
            self.conf.set_vaccine_usage_percentage(vaccine_usage_percentage))


    def test_get_total_to_infect(self):
        self.conf.set.conf.get_total_to_infect())


    def test_set_total_to_infect(self, total_to_infect):
        self.assertTrue(
            self.conf.set_total_to_infect(total_to_infect))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
