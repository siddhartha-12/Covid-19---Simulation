from Person import Person
from Config import Config
import logging
import numpy as np

class SimalationData():
    
    def __init__(self):
        self.population_set = None
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        self.config = Config.get_instance()
        section = self.config.get_property_name()
        if(section==None):
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
            self.config.update_to_infect()
            self.population_set[i].set_recoveryDays(np.random.randint(self.config.get_days_contageous(),self.config.get_days_contageous()+30))

    def initializePersonDataset(self,popualation: int)-> list:
        personDataset = list()
        for i in range(popualation):
            personDataset.append(Person(i))
        return personDataset

    
if __name__=="__main__":
    du = SimalationData()
    initial_infect = 0
    for i in du.getDataset():
        if i.get_infected():
            initial_infect+=1
    print(initial_infect,len(du.generateDataset()))
    # du.createStoreMatrix() #or we can call this in the intialData() funcion


        

    
    


