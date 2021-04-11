from SimulationData import SimalationData
class GenerateInfectionData():
    def contaminatedLocationsDict(self,person_dataset) :
        infectedDict={}
        for i in person_dataset:
            if i.get_infected():
                x = i.get_x()
                y = i.get_y()
                tup = (x,y)
                print(tup)
                add = [(-1,-1),(-1,0),(-1,1),(0,1),(0,-1),(1,-1),(1,0),(1,1)]
                j=0
                while j<8 :
                    if tup in infectedDict:
                        if i.get_can_infect() > person_dataset[infectedDict.get(tup)].get_can_infect(): 
                            infectedDict[tup] = i.get_id()
                    else: 
                        infectedDict[tup] = i.get_id()
                    new_x = x+add[j][0]
                    new_y = y+add[j][1]
                    if new_x>0 and new_y>0:
                        tup = (new_x,new_y)                    
                    j=j+1
        return infectedDict            

if __name__=="__main__":    
    covid = SimalationData()
    generateInfectionData = GenerateInfectionData()
    infected = generateInfectionData.contaminatedLocationsDict(covid.getDataset()) 
    print((infected))
