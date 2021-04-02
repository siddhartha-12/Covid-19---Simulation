
import configparser
import os
import logging

class ConfigUtil:
    _instance = None
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)
    defaultPath = str(os.getcwd())+"/config/config.cfg"
    cp = configparser.ConfigParser()
    isloaded = False
    __instance = None
    
    @staticmethod 
    def get_instance():
        """ Static access method. """
        if ConfigUtil.__instance == None:
            ConfigUtil()
        return ConfigUtil.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if ConfigUtil.__instance != None:
            logging.info("This is a singleton class. Use get_instance method")
            print("This is a singleton class. Use get_instance method")
            raise Exception("This class is a singleton!")
        else:
            ConfigUtil.__instance = self

    # def __init__(self):
    #     self.defaultPath = str(os.getcwd())+"/config/config.cfg"
    #     self.cp= configparser.ConfigParser()
    #     self.isloaded = False
        
    
    # Method to fetch the value based on the section and key passed.
    def get_value(self, section, setting):
        try:
            if(not self.isloaded):
                self.load_config()        
            ret = self.cp.get(section, setting)
        except configparser.NoOptionError:
            ret = None
        return ret

    # Method to load data   
    def load_config(self):
        try:
            if (os.path.exists(self.defaultPath) and os.path.isfile(self.defaultPath)):            
                self.cp.read(self.defaultPath)
                #print("Config File loaded")
                return True
            else:
                print("Config file not loaded")
                logging.info("\n \n Config file %s doesn't exist.",self.defaultPath)
        except:
            print("Config file not loaded")
            logging.info("Config file %s doesn't exist.")
            # print("False")
            return False

if __name__ == "__main__":
    cu =  ConfigUtil()
    print(cu.get_value("COVID19","name"))
    print(cu.cp.sections())
