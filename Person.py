class Person :
    
    # Default constructor 
    def __init__(self):
        self._age = None
        self._gender = None
        self._medical_history_scale = None
        self._k_factor = None
        self._vaccinated = None
        self._asymtomatic = None
        self._qurantine = None
        self._mask_usage = None
        self._infected = None
    # Parameterized contructor
    def __init__(self,age,gender,medical_history_scale,k_factor,vaccinated,asymtomatic,qurantine,mask_usage,infected):
        self._age = age
        self._gender = gender
        self._medical_history_scale = medical_history_scale
        self._k_factor = k_factor
        self._vaccinated = vaccinated
        self._asymtomatic = asymtomatic
        self._qurantine = qurantine
        self._mask_usage = mask_usage
        self._infected = infected

    # Getter and setter method for properties
    def get_age(self):
        return _age

    def set_age(self,age:int):
        self._age = age
    
    def get_gender(self):
        return _gender

    def set_gender(self,gender:str):
        self._gender = gender
    
    def get_medical_history_scale(self):
        return _medical_history_scale

    def set_medical_history_scale(self,age:float):
        self._medical_history_scale = medical_history_scale
    
    def get_k_factor(self):
        return _k_factor

    def set_k_factor(self,age:int):
        self._k_factor = k_factor
    
    def get_vaccinated(self):
        return _vaccinated

    def set_vaccinated(self,vaccinated:bool):
        self._vaccinated = vaccinated
    
    def get_asymtomatic(self):
        return _asymtomatic

    def set_asymtomatic(self,asymtomatic:bool):
        self._asymtomatic = asymtomatic

    def get_qurantine(self):
        return _qurantine

    def set_qurantine(self,qurantine:bool):
        self._qurantine = qurantine

    def get_mask_usage(self):
        return _mask_usage

    def set_mask_usage(self,mask_usage:bool):
        self._mask_usage = mask_usage

    def get_infected(self):
        return _infected

    def set_infected(self,infected:bool):
        self._infected = infected
       

# Local toString method

    def __str__(self):
        print( "age :" + self.get_age + "\n gender :" + self.get_gender + "\n medical_history_scale :" + self.medical_history_scale + "\n k_factor :" + self.get_k_factor + "\n vaccinated :" + self.get_vaccinated + "\n asymtomatic :" + self.get_asymtomatic + "\n qurantine :" + self.get_qurantine + "\n mask_usage :" + self.get_mask_usage + "\n age :" + self.get_infected + "\n age :" + self.get_infected

