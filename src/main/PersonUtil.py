from Person import Person
from Config import Config
from random import random
import numpy as np


class PersonUtil:
    cu = Config.get_instance()
    def updatePerson(self, ContaminationContact:bool,person: Person, time: int) -> Person:
        quo =False
        if(not person.get_deceased()):
            #Update whether a person would get infected or not when he/she comes in contact with an infected person
            if(ContaminationContact):
                result = self.getInfectionStatus(person.get_medical_history_scale(), person.get_mask_usage(), person.get_qurantine())
                spread_infection = self.check_will_spread()
                if result:
                    if spread_infection:
                        can_infect = np.random.randint(0,self.cu.get_total_to_infect()/2)
                        self.cu.set_total_to_infect(self.cu.get_total_to_infect()-can_infect)
                        self.cu.update_to_infect()
                        person.set_can_infect(can_infect)
                    person.set_infected(True)
                    recovery_time_min = self.cu.get_days_contageous() - 20 if self.cu.get_days_contageous() - 20>0 else self.cu.get_days_contageous()
                    recovery_time_max = self.cu.get_days_contageous() + 30
                    person.set_recoveryDays(np.random.random_integers(recovery_time_min,recovery_time_max))
                    quo =True

            # Update movement for the person
            if not person.get_qurantine():
                x, y = self.updateMovement(person.get_x(), person.get_y())
                person.set_x(x)
                person.set_y(y)

            # Update recovery days or demise status if the person is infected
            if person.get_infected() and not person.get_recovered():
                r_days = person.get_recoveryDays()
                if r_days > 0:
                    updated_rday = r_days-1 if r_days -1>0 else 0
                    person.set_recoveryDays(updated_rday)
                elif r_days <= 0:
                    demise = self.updateDemiseOrRecovered(person.get_medical_history_scale())
                    person.set_deceased(demise)
                    person.set_recovered(not demise)
                    person.set_infected(False)

            # Check if quarantine has been introduced or not and check if the person will quarantine or not
            if self.cu.get_quarantine_introduced_timeline() < time:
                qurantine = person.get_qurantine()
                person.set_qurantine(self.updateQuarantine(qurantine))
            # Check if mask has been introduced or not and check if the person will wear mask or not
            if self.cu.get_mask_introduced_timeline() < time:
                mask = person.get_mask_usage()
                person.set_mask_usage(self.updateMak(mask))
            # Check if vaccine has been introduced or not and check if the person will get vaccinated or not
            if self.cu.get_vaccine_introduced_timeline() < time and not person.get_vaccinated() and not person.get_deceased() and not person.get_infected():
                    person.set_vaccinated(self.updateVaccination())
        else:
            person.set_infected(False)
            person.set_qurantine(False)
            person.set_mask_usage(False)

        return person,quo

    # Method to update the x and y coordinates of the person
    def updateMovement(self, x: int, y: int):
        step_x = np.random.randint(-5, 6)
        step_y = np.random.randint(-5, 6)
        new_x = x + step_x
        new_y = y + step_y
        return new_x, new_y

    #Method to check if the peson will recover from the disease or loose his life
    def updateDemiseOrRecovered(self, medical_history_scale):
        # How much vulnerable is the person to die based on past medical history
        p_medical_history = float(medical_history_scale)/10
        result_death = np.random.choice([True, False],1, p=[1-p_medical_history, p_medical_history])
        return result_death[0]

    #Method to update if the mask status quo will change for the person
    def updateMak(self,status) -> bool:
        
        if(status):
            result = np.random.choice([True, False],1,p = [0.7,0.3])
        else:
            result = np.random.choice([True, False],1,p = [0.3,0.7])
        return result[0]
    
    #Method to update if the quarantine status quo will change for the person
    def updateQuarantine(self,status:bool) -> bool:
        frame = [True,False]
        if(status):
            statusupdate = np.random.choice(frame,1,p = [0.7,0.3])
        else:
            statusupdate = np.random.choice(frame,1,p = [0.3,0.7])
        return (statusupdate[0])
    
    #Method to update if the vaccine status quo will change for the person
    def updateVaccination(self):
        usuage = self.cu.get_vaccine_usage_percentage()
        if(int(usuage)==0):
            return False
        low_usuage = usuage-10 if usuage-10>0 else 0
        high_usuage = usuage+10 if usuage<100 else 100
        probability_of_vaccine = float(np.random.randint(low_usuage,high_usuage)) / 100
        print(probability_of_vaccine)
        status = np.random.choice([True,False],1,p = [probability_of_vaccine,1-probability_of_vaccine])
        return status[0]

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
            maskEffectiveness = np.random.randint(maskEffectivenessLowerLimit,maskEffectivenessUpperLimit )
        if(quarantineFactor):
            quarantineEffectivenessFactor  =  int(self.cu.get_qurantine_effectiveness())
            quarantineEffectivenessLowerLimit = (quarantineEffectivenessFactor - 10) if (quarantineEffectivenessFactor - 10) >=0 else 0
            quarantineEffectivenessUpperLimit = (quarantineEffectivenessFactor + 10) if (quarantineEffectivenessFactor + 10) <=100 else 100
            quarantineEffectiveness = np.random.randint(quarantineEffectivenessLowerLimit,quarantineEffectivenessUpperLimit )
        if maskFactor and quarantineFactor:
            totalEffectiveProbability = (maskEffectiveness * quarantineEffectiveness * health_scale) / 100000
        elif maskFactor:
            totalEffectiveProbability = (maskEffectiveness * health_scale) / 1000
        elif quarantineFactor:
            totalEffectiveProbability = (quarantineEffectiveness * health_scale) / 1000
        else:
            totalEffectiveProbability = (health_scale) / 100
        sampleList = [False,True]
        result = np.random.choice(sampleList,1,p=[totalEffectiveProbability,1-totalEffectiveProbability])
        return result[0]

    def testInfectionProbability(self,health_scale):
        print("Result Mask Present | Quarantine Absent   ----" + str(self.getInfectionStatus("COVID19", 8, True, False)))
        print("Result Mask Absent  | Quarantine Present  ----" + str(self.getInfectionStatus("COVID19", 8, False, True)))
        print("Result Mask Absent  | Quarantine Absent   ----" + str(self.getInfectionStatus("COVID19", 8, False, False)))
        print("Result Mask Present | Quarantine Present  ----" + str(self.getInfectionStatus("COVID19", 8, True, True)))

    def check_will_spread(self)-> bool:
        k = float(self.cu.get_k_factor())
        if k>=1:
            k = 0.99
        elif k<0:
            k =0.01
        result =  np.random.choice([True,False],1, p = [k,1-k])
        return result[0]

if __name__=="__main__":
    cu = Config.get_instance()
    cu.load_from_file("COVID19")
    pu = PersonUtil()
    f1 = 0
    f2 = 0
    for i in range(10):
        a=pu.updateVaccination()
        if a:
            f1 +=1
        else:
            f2 +=1
    print("True : "+ str(f1) + " False : "+ str(f2))

