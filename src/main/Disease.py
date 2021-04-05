from ConfigUtil import ConfigUtil

class Disease:
        
    def __init__(self,id):        
        self.config = ConfigUtil.get_instance()
        if id == 1:
            section="COVID19"
        elif id==2:
            section="second virus"

        self._name = str(self.config.get_value(section,"name"))
        self._r_factor = int(self.config.get_value(section,"r_factor"))
        self._k_factor = int(self.config.get_value(section,"k_factor"))
        self._days_contageous = int(self.config.get_value(section,"days_contageous"))
        self._mask_usage_effectiveness = int(self.config.get_value(section,"mask_usuage_effectiveness"))
        self._quarantine_timeline = int(self.config.get_value(section,"quarantine_timeline"))
        self._qurantine_effectiveness = int(self.config.get_value(section,"qurantine_effectiveness"))
        self._vaccine_timeline = int(self.config.get_value(section,"vaccine_timeline"))
        self._vaccine_effectiveness = int(self.config.get_value(section,"vaccine_effectiveness"))

    def get_name(self):
        return self._name

    def set_name(self,name:str):
        self._name = name

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
    
    def get_mask_usage_effectiveness(self):
        return self._mask_usage_effectiveness

    def set_mask_usage_effectiveness(self,mask_usage_effectiveness:int):
        self._mask_usage_effectiveness = mask_usage_effectiveness

    def get_quarantine_timeline(self):
        return self._quarantine_timeline

    def set_quarantine_timeline(self,quarantine_timeline:int):
        self._quarantine_timeline = quarantine_timeline
    
    def get_qurantine_effectiveness(self):
        return self._qurantine_effectiveness

    def set_qurantine_effectiveness(self,qurantine_effectiveness:int):
        self._qurantine_effectiveness = qurantine_effectiveness        

    def get_vaccine_timeline(self):
        return self._vaccine_timeline

    def set_vaccine_timeline(self,vaccine_timeline:int):
        self._vaccine_timeline = vaccine_timeline
    
    def get_vaccine_effectiveness(self):
        return self._vaccine_effectiveness

    def set_vaccine_effectiveness(self,vaccine_effectiveness:int):
        self._vaccine_effectiveness = vaccine_effectiveness    

        
    def __str__(self):
        return("\n Name: "+str(self.get_name())+"\n R-Factor: "+str(self.get_r_factor())
                +"\n K-Factor: "+ str(self.get_k_factor())+"\n Days Contageous: "+ str(self.get_days_contageous())
                +"\n Mask Usage Effectiveness: "+ str(self.get_mask_usage_effectiveness())+"\n Quarantine Timeline: "+str(self.get_quarantine_timeline())
                +"\n Qurantine Effectiveness: "+ str(self.get_qurantine_effectiveness())+"\n Vaccine Timeline: "+str(self.get_vaccine_timeline())
                +"\n Vaccine Effectiveness: "+ str(self.get_vaccine_effectiveness())+"\n")

d = Disease(2)
print (d)

