import os
import sys
cwd = os.getcwd()+"/src/main"
sys.path.insert(1,cwd)
import unittest
from Person import Person

class ConfigTest(unittest.TestCase):

	def setUp(self):
		self.person = Person(0)
	
	def testPersonObjectCreation(self):
		self.assertTrue(self.person)

	def testPersonObjectDefaultX(self):
		self.assertTrue(0<= self.person.get_x() <1000)
		
	def testPersonObjectDefaultY(self):
		self.assertTrue(0<= self.person.get_y() <1000)

	def testPersonObjectDefaultAge(self):
		self.assertTrue(0< self.person.get_age() <100)

	def testPersonObjectDefaultMedicalScale(self):
		self.assertTrue(0<= self.person.get_medical_history_scale() <100)
	
	def testPersonObjectDefaultRecoveryDays(self):
		self.assertEqual(int(self.person.get_recoveryDays()), -1)

	def testPersonID(self):
		self.assertEqual(int(self.person.get_id()), 0)
	
	def testGender(self):
		self.assertTrue(self.person.get_gender()=="M" or self.person.get_gender()=="F") 

	def checkFalseValues(self):
		self.assertFalse(self.person.get_vaccinated())
		self.assertFalse(self.person.get_asymtomatic())
		self.assertFalse(self.person.get_qurantine())
		self.assertFalse(self.person.get_mask_usage)
		self.assertFalse(self.person.get_infected())
		self.assertFalse(self.person.get_deceased())

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()