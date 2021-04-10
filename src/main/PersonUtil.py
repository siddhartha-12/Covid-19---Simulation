from Person import Person
from Config import Config
from random import random
import numpy as np


class PersonUtil:
    cu = Config()
    def updatePerson(self, person: Person, time: int) -> Person:
        
        # Update movement for the person
        if not person.get_qurantine():
            x, y = self.updateMovement(person.get_x(), person.get_y())
            person.set_x(x)
            person.set_y(y)

        # Update recovery days or demise status if the person is infected
        if person.get_infected():
            r_days = person.get_recoveryDays()
            if r_days != 0:
                person.set_recoveryDays(r_days-1)
            elif r_day == 0:
                recovered, demise = self.updateDemiseOrRecovered(
                    person.get_medical_history_scale())
                person.set_deceased(demise)
                person.set_recovered(recovered)
        
        # Check if quarantine has been introduced or not and check if the person will quarantine or not
        if self.cu.get_quarantine_introduced_timeline() > time:
            qurantine = person.get_qurantine()
            if self.updateQuarantine(qurantine) != qurantine:
                person.set_qurantine(not qurantine)
        # Check if mask has been introduced or not and check if the person will wear mask or not
        if self.cu.get_mask_introduced_timeline > time:
            mask = person.get_mask_usage()
            if self.updateMak(mask) != mask:
                person.set_mask_usage(not mask)
        # Check if vaccine has been introduced or not and check if the person will get vaccinated or not
        if self.cu.get_vaccine_introduced_timeline() > time:
            vaccinated = person.get_vaccinated()
            if not vaccinated:
                person.set_mask_usage(self.updateMak())

        return person

    # Method to update the x and y coordinates of the person
    def updateMovement(self, x: int, y: int):
        step_x = np.random.randint(-5, 5)
        step_y = np.random.randint(-5, 5)
        new_x = x + step_x
        new_y = y + step_y
        return new_x, new_y

    #Method to check if the peson will recover from the disease or loose his life
    def updateDemiseOrRecovered(self, medical_history_scale):
        # How much vulnerable is the person to die based on past medical history
        p_medical_history = float(medical_history_scale)/10
        probability_of_survival = (0.95 * p_medical_history)/10
        result = np.random.choice(
            True, False, p=[probability_of_survival, 1-probability_of_survival])
        return result, not result

    #Method to update if the mask status quo will change for the person
    def updateMak(self) -> bool:
        if(status):
            status = np.random.choice(True,False,p = [0.7,0.1])
        else:
            status = np.random.choice(np.random.choice(True,False,p = [0.7,0.3]))
        return status
    
    #Method to update if the quarantine status quo will change for the person
    def updateQuarantine(self,status:bool) -> bool:
        
        if(status):
            status = np.random.choice(True,False,p = [0.7,0.1])
        else:
            status = np.random.choice(np.random.choice(True,False,p = [0.5,0.5]))
        return status
    
    #Method to update if the vaccine status quo will change for the person
    def updateVaccination(self):
        usuage = self.cu.get_vaccine_usage_percentage()
        low_usuage = usuage-30 if usuage-30>0 else 0
        high_usuage = usuage+30 if usuage<100 else 100
        low_percentage = float(low)
        high_percentage = float(high)
        probability_of_vaccine = float(np.random.randint(low,high)) / 100
        status = np.random.choice(True,False,p = [probability_of_vaccine,1-probability_of_vaccine])
        return status

    #Method to update if the person will get infected or not
    def getInfectionStatus(self,health_scale:int,maskFactor:bool,quarantineFactor:bool)-> bool:
        
        if(health_scale<1):
            health_scale = 1
        if(health_scale>10):
            health_scale =10

        if(maskFactor):
            maskEffectivenessFactor  =  int(self.cu.get_mask_usage_effectiveness())
            maskEffectivenessLowerLimit = (maskEffectivenessFactor - 10) if (maskEffectivenessFactor - 10) >=0 else 0
            maskEffectivenessUpperLimit = (maskEffectivenessFactor + 10) if (maskEffectivenessFactor + 10) <=100 else 100
            maskEffectiveness = random.randint(maskEffectivenessLowerLimit,maskEffectivenessUpperLimit )
        if(quarantineFactor):
            quarantineEffectivenessFactor  =  int(self.cu.get_qurantine_effectiveness())
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
        print("Result Mask Present | Quarantine Absent   ----" + str(self.getInfectionStatus("COVID19", 8, True, False)))
        print("Result Mask Absent  | Quarantine Present  ----" + str(self.getInfectionStatus("COVID19", 8, False, True)))
        print("Result Mask Absent  | Quarantine Absent   ----" + str(self.getInfectionStatus("COVID19", 8, False, False)))
        print("Result Mask Present | Quarantine Present  ----" + str(self.getInfectionStatus("COVID19", 8, True, True)))
