
import configparser
import os
import logging

class ConfigUtil:
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

    def __init__(self):
        self.defaultPath = str(os.getcwd())+"/config/config.cfg"
        self.cp= configparser.ConfigParser()
        self.isloaded = False
        
    
    #Method to fetch the value based on the section and key passed.
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
                print("Config File loaded")
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
    print(cu.cp.sections())
    print(cu.get_value("COVID19","name"))