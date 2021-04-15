from Person import Person
from Config import Config
import logging
import numpy as np

class SimalationData():
    
    def __init__(self):
        self.population_set = None
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        self.config = Config.get_instance()
        self.config.load_from_file("COVID19")

    def getDataset(self)-> list:
        if(self.population_set is None):
            return self.generateDataset()
        return self.population_set

    def generateDataset(self)-> list:
        self.population_set = self.initializePersonDataset(int(self.config.get_population()))
        self.infect_initial()
        return self.population_set
        #The function above prepares the initial dataset with healthy and infected people

    def infect_initial(self):
        number_to_infect = int(float(self.config.get_population()) * float(self.config.get_initial_infected_percentage())/100)
        infect_index = np.random.choice(int(self.config.get_population()),number_to_infect, replace=True)
        for i in infect_index:
            self.population_set[i].set_infected(True)
            self.population_set[i].set_can_infect(self.config.get_r_factor())
            self.population_set[i].set_recoveryDays(self.config.get_days_contageous())

    def initializePersonDataset(self,popualation: int)-> list:
        personDataset = list()
        for i in range(popualation):
            personDataset.append(Person(i))
        return personDataset

    
if __name__=="__main__":
    du = SimalationData()
    for i in du.getDataset():
        print (i)
    # du.createStoreMatrix() #or we can call this in the intialData() funcion


        

    
    


