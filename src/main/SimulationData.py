from Person import Person
from ConfigUtil import ConfigUtil
import logging
import numpy as np

class SimalationData():
    
    def __init__(self):
        self.population_set = None
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        self.config = ConfigUtil.get_instance()

    def getDataset(self)-> list:
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
        for i in range(popualation):
            personDataset.append(Person(i))
        return personDataset

    def createStoreMatrix(self):
        self.store = list()
        number_of_people = int(self.config.get_value('SIMULATION','population'))
        for i in range(int(number_of_people/50)+1):
            self.store.append([])
        for i in range(int(number_of_people/50)+1):
            for j in range(int(number_of_people/50)+1):
                self.store[i].append([])
        for p in self.population_set:
            x_coef = int(p.get_x()/50)
            y_coef = int(p.get_y()/50)
            self.store[x_coef][y_coef].append(p)

    def updateStore(self, person_obj, old_x, old_y, new_x, new_y):
        self.store[int(old_x/50)][int(old_y/50)].remove(person_obj)
        self.store[int(new_x/50)][int(new_y/50)].append(person_obj)
    
    def getStoreMatrix(self):
        return self.store

    def movement(self):
        population_total = int(self.config.get_value('SIMULATION','POPULATION'))
        number_to_move = np.random.randint(int(population_total*0.05),int(population_total*0.075))
        movement_index = np.random.choice(population_total,number_to_move)
        toss =[-3,-2,-1,1,2,3]
        for i in movement_index:
            old_x = self.population_set[i].get_x()
            old_y = self.population_set[i].get_y()
            new_x = old_x + toss[np.random.randint(0,6)]
            new_y = old_y + toss[np.random.randint(0,6)]
            #update store matrix if needed
            if new_x <=1000 and new_y<=1000 and new_x >=0 and new_y>=0:

                self.population_set[i].set_x(new_x)
                self.population_set[i].set_y(new_y)
                self.updateStore(self.population_set[i],old_x,old_y,new_x,new_y)  #updates the value in the matrix
            #print(old_x, self.population_set[i].get_x(),"\n")
        return self.population_set

if __name__=="__main__":
    du = SimalationData()
    for i in du.getDataset():
        print (i)
    # du.createStoreMatrix() #or we can call this in the intialData() funcion


        

    
    


