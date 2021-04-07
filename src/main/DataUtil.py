from Person import Person
from ConfigUtil import ConfigUtil
import logging
import numpy as np
from SimulationData import SimalationData
import random
from numpy.random import choice


class DataUtil:

    def __init__(self):
        self.cu = ConfigUtil.get_instance()

    def getLocationInfected(self,personDataset:list) -> list:
        x_coordinate  = list()
        y_coordinate = list()
        for i in personDataset:
            if i.get_infected():
                x_coordinate.append(i.get_x())
                Y_coordinate.append(i.get_y())
        return [x_coordinate,y_coordinate]
    
    def getLocationInfected(self,personDataset:list) -> list:
        x_coordinate  = list()
        y_coordinate = list()
        for i in personDataset:
            if i.get_infected()==True:
                x_coordinate.append(i.get_x())
                y_coordinate.append(i.get_y())
        return [x_coordinate,y_coordinate]
    
    def getLocationHealthy(self,personDataset:list) -> list:
        x_coordinate  = list()
        y_coordinate = list()
        for i in personDataset:
            if not i.get_infected() or i.get_recovered:
                x_coordinate.append(i.get_x())
                Y_coordinate.append(i.get_y())
        return [x_coordinate,y_coordinate]

    def getLocationRecovered(self,personDataset:list) -> list:
        x_coordinate  = list()
        y_coordinate = list()
        for i in personDataset:
            if i.get_recovered:
                x_coordinate.append(i.get_x())
                Y_coordinate.append(i.get_y())
        return [x_coordinate,y_coordinate]

    def getLocationVaccincated(self,personDataset:list) -> list:
        x_coordinate  = list()
        y_coordinate = list()
        for i in personDataset:
            if i.get_recovered:
                x_coordinate.append(i.get_x())
                Y_coordinate.append(i.get_y())
        return [x_coordinate,y_coordinate]

    def getLocationOfMaskedPerson(self,personDataset:list) -> list:
        x_coordinate  = list()
        y_coordinate = list()
        for i in personDataset:
            if i.get_mask_usage:
                x_coordinate.append(i.get_x())
                Y_coordinate.append(i.get_y())
        return [x_coordinate,y_coordinate]
    
    def getTotalCountInfected(self,personDataset:list) -> int:
        count = 0 
        for i in personDataset:
            if i.get_infected():
                count +=1
        return count

    def getInfectionProbability(self,disease,health_scale:int,maskFactor:bool,quarantineFactor:bool)-> bool:
        
        if(health_scale<1):
            health_scale = 1
        if(health_scale>10):
            health_scale =10

        if(maskFactor):
            maskEffectivenessFactor  =  int(self.cu.get_value(disease, "mask_usuage_effectiveness"))
            maskEffectivenessLowerLimit = (maskEffectivenessFactor - 10) if (maskEffectivenessFactor - 10) >=0 else 0
            maskEffectivenessUpperLimit = (maskEffectivenessFactor + 10) if (maskEffectivenessFactor + 10) <=100 else 100
            maskEffectiveness = random.randint(maskEffectivenessLowerLimit,maskEffectivenessUpperLimit )
        if(quarantineFactor):
            quarantineEffectivenessFactor  =  int(self.cu.get_value(disease, "qurantine_effectiveness"))
            quarantineEffectivenessLowerLimit = (quarantineEffectivenessFactor - 10) if (quarantineEffectivenessFactor - 10) >=0 else 0
            quarantineEffectivenessUpperLimit = (quarantineEffectivenessFactor + 10) if (quarantineEffectivenessFactor + 10) <=100 else 100
            quarantineEffectiveness = random.randint(quarantineEffectivenessLowerLimit,quarantineEffectivenessUpperLimit )
        if maskFactor and quarantineFactor:
            totalEffectiveProbability = (maskEffectiveness * quarantineEffectiveness * health_scale) / 100000
        elif maskFactor:
            totalEffectiveProbability = (maskEffectiveness * health_scale) / 1000
        elif quarantineFactor:
            totalEffectiveProbability = (quarantineEffectiveness * health_scale) / 1000
        else:
            totalEffectiveProbability = (health_scale) / 100
        print(totalEffectiveProbability)
        sampleList = [False,True]
        result = choice(sampleList,p=[totalEffectiveProbability,1-totalEffectiveProbability])
        return result

    def testInfectionProbability(self,health_scale):
        print("Result Mask Present | Quarantine Absent   ----" + str(self.getInfectionProbability("COVID19", 8, True, False)))
        print("Result Mask Absent  | Quarantine Present  ----" + str(self.getInfectionProbability("COVID19", 8, False, True)))
        print("Result Mask Absent  | Quarantine Absent   ----" + str(self.getInfectionProbability("COVID19", 8, False, False)))
        print("Result Mask Present | Quarantine Present  ----" + str(self.getInfectionProbability("COVID19", 8, True, True)))

if __name__=="__main__":
    du = DataUtil()
    # covid = SimalationData()
    # covid.intialData() #pass the name of the virus to fetch corresponding data
    # print("Infected person " + str(du.getTotalCountInfected(covid.intialData())))

    du.testInfectionProbability(8)