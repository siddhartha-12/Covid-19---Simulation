from Config import Config
import random as rd
import numpy as np

class Person :
    
    # Default constructor 
    def __init__(self,id):
        self._id = id
        self.config = Config.get_instance()
        matrix = self.config.get_population()
        population = int(matrix if matrix else 10)
        self._x_cordinate = rd.randint(0, population) 
        self._y_cordinate = rd.randint(0, population) 
        self._age = rd.randint(1, 100)
        self._gender = rd.choice(["M","F"])
        self._medical_history_scale = rd.randint(11, 109)//10 #''' Medical history scale is vulnerability of immune system due to past illess. 1 being poor healthy and 10 good health'''
        self._k_factor = 0
        self._vaccinated = False
        self._asymtomatic = False
        self._qurantine = False
        self._mask_usage = False
        self._infected = False
        self._recovered = False
        self._deceased = False
        self._recoveryDays = -1
        self._can_infect = 0
        

    # Getter and setter method for properties
    
    def get_can_infect(self):
        return self._can_infect

    def set_can_infect(self,can_infect:int):
        self._can_infect = can_infect

    def get_recoveryDays(self):
        return self._recoveryDays

    def set_recoveryDays(self,recoveryDays:int):
        self._recoveryDays = recoveryDays
    
    def get_id(self):
        return self._id

    def set_id(self,age:int):
        self._id = id
    
    def get_age(self):
        return self._age

    def set_age(self,age:int):
        self._age = age
    
    def get_x(self):
        return self._x_cordinate

    def set_x(self,x:int):
        self._x_cordinate = x
    
    def get_y(self):
        return self._y_cordinate

    def set_y(self,y:int):
        self._y_cordinate = y
    
    def get_gender(self):
        return self._gender

    def set_gender(self,gender:str):
        self._gender = gender
    
    def get_medical_history_scale(self):
        return self._medical_history_scale

    def set_medical_history_scale(self,medical_history_scale:float):
        self._medical_history_scale = medical_history_scale
    
    def get_k_factor(self):
        return self._k_factor

    def set_k_factor(self,k_factor:int):
        self._k_factor = k_factor
    
    def get_vaccinated(self):
        return self._vaccinated

    def set_vaccinated(self,vaccinated:bool):
        self._vaccinated = vaccinated
    
    def get_asymtomatic(self):
        return self._asymtomatic

    def set_asymtomatic(self,asymtomatic:bool):
        self._asymtomatic = asymtomatic

    def get_qurantine(self):
        return self._qurantine

    def set_qurantine(self,qurantine:bool):
        self._qurantine = qurantine

    def get_mask_usage(self):
        return self._mask_usage

    def set_mask_usage(self,mask_usage:bool):
        self._mask_usage = mask_usage

    def get_infected(self):
        return self._infected

    def set_infected(self,infected:bool):
        self._infected = infected
    
    def get_recovered(self):
        return self._recovered

    def set_recovered(self,recovered:bool):
        self._recovered = recovered

    def get_deceased(self):
        return self._deceased

    def set_deceased(self,deceased:bool):
        self._deceased = deceased
       

# Local toString method

    def __str__(self):
        return( "\n ID :" + str(self.get_id()) + "\n X-cordinate :" + str(self.get_x()) + "\n Y-cordinate :" + str(self.get_y()) + "\n age :" + str(self.get_age()) + "\n gender :" + str(self.get_gender()) + "\n medical_history_scale :" + 
        str(self.get_medical_history_scale()) + "\n k_factor :" + str(self.get_k_factor()) + "\n vaccinated :" 
        + str(self.get_vaccinated()) + "\n asymtomatic :" + str(self.get_asymtomatic()) + "\n qurantine :" 
        + str(self.get_qurantine()) + "\n mask_usage :" + str(self.get_mask_usage()) + "\n Infected :" 
        + str(self.get_infected()) + "\n Recovered :" + str(self.get_recovered()) + "\n Can Infect :" + str(self.get_can_infect()) + "\n Deceased :" + str(self.get_deceased()))
         

if __name__ == "__main__":
    persons=[]

    for i in range(5):
        persons.append(Person(i))

    for i in persons:
       print (i.get_id())
