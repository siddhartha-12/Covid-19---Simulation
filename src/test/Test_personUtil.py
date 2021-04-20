import unittest
import os
import sys
cwd = os.getcwd()+"/src/main"
sys.path.insert(1, cwd)
from Person import Person
from PersonUtil import PersonUtil
from Config import Config

class ConfigClassTest(unittest.TestCase):

    def setUp(self):
        self.person = Person(0)
        self.personUtil = PersonUtil()
        cu = Config.get_instance()
        cu.load_from_file("COVID19")
    
    # Test whether a person is getting updated randomly or not
    def test_updatePerson(self):
        person_x = self.person.get_x()
        person_y = self.person.get_y()        
        person_upd,quo = self.personUtil.updatePerson(True,self.person,0)             
        self.assertFalse(person_upd.get_x() == person_x and person_upd.get_y() == person_y)

    # Test update movement functionality
    def test_updateMovement(self):
        x = 10
        y = 5 
        new_x,new_y = self.personUtil.updateMovement(x,y)
        self.assertFalse(new_x == x and new_y == y)
    
    # Test demise or recovered functionality that it returns one of this
    def test_updateDemiseOrRecovered(self):
        medical = self.person.get_medical_history_scale()
        self.assertIsNotNone(self.personUtil.updateDemiseOrRecovered(medical))

    # Test if mask is on or off
    def test_updateMask(self):
        self.assertIsNotNone(self.personUtil.updateMak(True))

    # Test if person should quarantine  
    def test_updateQuarantine(self):
        self.assertIsNotNone(self.personUtil.updateQuarantine(True))

    # Test if person is vaccinated
    def test_updateVaccination(self):
        self.assertIsNotNone(self.personUtil.updateVaccination(True))

    # Test infection status of a person
    def test_getInfectionStatus(self):
        self.assertIsNotNone(self.personUtil.getInfectionStatus(self.person.get_medical_history_scale(),True,True))
    
    # Test if person will spread based on k-factor
    def test_check_will_spread(self):
        self.assertIsNotNone(self.personUtil.check_will_spread())

if __name__ == "__main__":
    unittest.main()