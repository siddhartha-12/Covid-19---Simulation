import unittest
import os
import sys
cwd = os.getcwd()+"/src/main"
sys.path.insert(1, cwd)
from Person import Person
from PersonUtil import PersonUtil

class ConfigClassTest(unittest.TestCase):

    def setUp(self):
        self.person = Person(0)
        self.personUtil = PersonUtil()

if __name__ == "__main__":
    unittest.main()