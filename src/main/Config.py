import logging
from ConfigUtil import ConfigUtil

class Config:
    __instance = None

    @staticmethod 
    def get_instance():
        """ Static access method. """
        if Config.__instance == None:
            Config()
        return Config.__instance

    def __init__(self):
        
        if Config.__instance != None:
            logging.info("This is a singleton class. Use get_instance method")
            print("This is a singleton class. Use get_instance method")
            raise Exception("This class is a singleton!")
        else:
            Config.__instance = self                       
        
        self._property_name =                  None
        self._population =                     None
        self._initial_infected_percentage =    None
        self._r_factor =                       None
        self._k_factor =                       None
        self._days_contageous =                None
        self._mask_introduced_timeline =       None
        self._mask_usage_effectiveness =       None
        self._mask_usage_percentage =          None
        self._quarantine_introduced_timeline = None
        self._qurantine_effectiveness =        None
        self._qurantine_usage_percentage =     None
        self._vaccine_introduced_timeline =    None
        self._vaccine_effectiveness =          None
        self._vaccine_usage_percentage =       None
        self._total_to_infect =                None        
 
    def get_property_name(self):
        return self._property_name

    def set_property_name(self,property_name:str):
        self._property_name = property_name

    def get_population(self):
        return self._population

    def set_population(self,population:int):
        self._population = population

    def get_initial_infected_percentage(self):
        return self._initial_infected_percentage

    def set_initial_infected_percentage(self,initial_infected_percentage:int):
        self._initial_infected_percentage = initial_infected_percentage

    def get_r_factor(self):
        return self._r_factor

    def set_r_factor(self,r_factor:int):
        self._r_factor = r_factor
    
    def get_k_factor(self):
        return self._k_factor

    def set_k_factor(self,k_factor:int):
        self._k_factor = k_factor
    
    def get_days_contageous(self):
        return self._days_contageous

    def set_days_contageous(self,days_contageous:int):
        self._days_contageous = days_contageous

    def get_mask_introduced_timeline(self):
        return self._mask_introduced_timeline

    def set_mask_introduced_timeline(self,mask_introduced_timeline:int):
        self._mask_introduced_timeline = mask_introduced_timeline

    def get_mask_usage_effectiveness(self):
        return self._mask_usage_effectiveness

    def set_mask_usage_effectiveness(self,mask_usage_effectiveness:int):
        self._mask_usage_effectiveness = mask_usage_effectiveness

    def get_mask_usage_percentage(self):
        return self._mask_usage_percentage

    def set_mask_usage_percentage(self,mask_usage_percentage:int):
        self._mask_usage_percentage = mask_usage_percentage

    def get_quarantine_introduced_timeline(self):
        return self._quarantine_introduced_timeline

    def set_quarantine_introduced_timeline(self,quarantine_introduced_timeline:int):
        self._quarantine_introduced_timeline = quarantine_introduced_timeline
    
    def get_qurantine_effectiveness(self):
        return self._qurantine_effectiveness

    def set_qurantine_effectiveness(self,qurantine_effectiveness:int):
        self._qurantine_effectiveness = qurantine_effectiveness        

    def get_qurantine_usage_percentage(self):
        return self._qurantine_usage_percentage

    def set_qurantine_usage_percentage(self,qurantine_usage_percentage:int):
        self._qurantine_usage_percentage = qurantine_usage_percentage        

    def get_vaccine_introduced_timeline(self):
        return self._vaccine_introduced_timeline

    def set_vaccine_introduced_timeline(self,vaccine_introduced_timeline:int):
        self._vaccine_introduced_timeline = vaccine_introduced_timeline
    
    def get_vaccine_effectiveness(self):
        return self._vaccine_effectiveness

    def set_vaccine_effectiveness(self,vaccine_effectiveness:int):
        self._vaccine_effectiveness = vaccine_effectiveness    

    def get_vaccine_usage_percentage(self):
        return self._vaccine_usage_percentage

    def set_vaccine_usage_percentage(self,vaccine_usage_percentage:int):
        self._vaccine_usage_percentage = vaccine_usage_percentage        

    def get_total_to_infect(self):
        return self._total_to_infect

    def set_total_to_infect(self,total_to_infect:int):
        self._total_to_infect = total_to_infect   

    def __str__(self):
        return("\n Property Name: "+str(self.get_property_name())+"\n Population: "+str(self.get_population())
                +"\n Initial Infected Percentage: "+ str(self.get_initial_infected_percentage())+"\n R-Factor: "+ str(self.get_r_factor())
                +"\n K-Factor: "+ str(self.get_k_factor())+"\n Days Contageous: "+ str(self.get_days_contageous())
                +"\n Mask Usage Effectiveness: "+ str(self.get_mask_usage_effectiveness())+"\n Quarantine Timeline: "+str(self.get_quarantine_introduced_timeline())
                +"\n Qurantine Effectiveness: "+ str(self.get_qurantine_effectiveness())+"\n Vaccine Timeline: "+str(self.get_vaccine_introduced_timeline())
                +"\n Vaccine Effectiveness: "+ str(self.get_vaccine_effectiveness())+"\n")

    def update_to_infect(self):
        self.set_total_to_infect(self.get_total_to_infect() + self.get_r_factor())
    
    def update_to_infect_number(self,number):
        self.set_total_to_infect(self.get_total_to_infect() + self.get_r_factor())

    def load_from_file(self,disease_section):
        cu = ConfigUtil()
        self.set_property_name(disease_section)
        self.set_population(int(cu.get_value("SIMULATION","population")))
        self.set_initial_infected_percentage(int(cu.get_value("SIMULATION","initial_infected_percentage")))
        self.set_r_factor(int(cu.get_value(disease_section,"r_factor")))
        self.set_k_factor(float(cu.get_value(disease_section,"k_factor")))
        self.set_days_contageous(int(cu.get_value(disease_section,"days_contageous")))
        self.set_mask_introduced_timeline(int(cu.get_value(disease_section,"mask_timeline")))
        self.set_mask_usage_effectiveness(int(cu.get_value(disease_section,"mask_usuage_effectiveness")))
        self.set_mask_usage_percentage(int(cu.get_value(disease_section,"mask_usuage_percentage")))
        self.set_quarantine_introduced_timeline(int(cu.get_value(disease_section,"quarantine_timeline")))
        self.set_qurantine_effectiveness(int(cu.get_value(disease_section,"qurantine_effectiveness")))
        self.set_qurantine_usage_percentage(int(cu.get_value(disease_section,"qurantine_percentage")))
        self.set_vaccine_introduced_timeline(int(cu.get_value(disease_section,"vaccine_timeline")))
        self.set_vaccine_effectiveness(int(cu.get_value(disease_section,"vaccine_effectiveness")))
        self.set_vaccine_usage_percentage(int(cu.get_value(disease_section,"vaccinated_percentage")))
        to_be_infected = int(self.get_r_factor()) * (int(self.get_population())*int(self.get_initial_infected_percentage())/100)
        self.set_total_to_infect(to_be_infected)


if __name__=="__main__":

    a = Config()
    b =Config.get_instance()
    print(a,b)