
import configparser
import os
import logging

class ConfigUtil:
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

    def __init__(self):
        self.defaultPath = str(os.getcwd())+"/config/config.cfg"
        self.cp= configparser.ConfigParser()
        
    
    #Method to fetch the value based on the section and key passed.
    def getValue(self,section, prop):
        return self.cp[section][prop]
    
    def get_setting(self, section, setting):
        try:        
            ret = self.cp.get(section, setting)
        except configparser.NoOptionError:
            ret = None
        return ret

    # method to check if the there is any data loaded    
    def hasConfigData(self):
        if(len(self.cp)>0):
            return True
        else:
            return False

    # Method to load data   
    def loadConfig(self):
        try:
            if (os.path.exists(self.defaultPath) and os.path.isfile(self.defaultPath)):            
                self.cp.read(self.defaultPath)
                print("loaded")
                return True
            else:
                print("Not loaded")
                logging.info("\n \n Config file %s doesn't exist.",self.defaultPath)
        except:
            print("Not loaded")
            logging.info("Config file %s doesn't exist.")
            #print("False")
            return False

if __name__ == "__main__":
    cu =  ConfigUtil()
    cu.loadConfig()
    print(cu.cp.sections())
    print(cu.get_setting("COVID19","name"))