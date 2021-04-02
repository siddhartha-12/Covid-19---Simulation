from Person import Person
from ConfigUtil import ConfigUtil
import logging
import numpy as np

class SimalationData():
    
    def __init__(self):
        self.population_set = None
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        self.config = ConfigUtil.get_instance()

    def intialData(self)-> list:
        if(self.population_set is None):
            return self.generateDataset()
        return self.population_set

    def generateDataset(self)-> list:
        self.population_set = self.initializePersonDataset(int(self.config.get_value('SIMULATION','population')))
        self.infect_initial()
        return self.population_set
        #The function above prepares the initial dataset with healthy and infected people

    def infect_initial(self):
        number_to_infect = int(float(self.config.get_value('SIMULATION','population')) * float(self.config.get_value('SIMULATION','initial_infected_percentage'))/100)
        infect_index = np.random.choice(int(self.config.get_value('SIMULATION','population')),number_to_infect, replace=True)
        for i in infect_index:
            self.population_set[i].set_infected(True)

    def initializePersonDataset(self,popualation: int)-> list:
        personDataset = list()
        for _ in range(popualation):
            personDataset.append(Person())
        return personDataset

    def movement(self):
        pass #take motivation from infect_initial

if __name__=="__main__":
    du = SimalationData()
    for i in du.intialData():
        print (i)


        

    
    


