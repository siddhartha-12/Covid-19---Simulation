from Person import Person
from SimulationData import SimalationData
import logging
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from DataUtil import DataUtil

#start from line 59

def getLocation1(dud):
    xlist = list()
    ylist = list()
    for i in dud:
        if i.get_infected()==False:
            xlist.append(i.get_x())
            ylist.append(i.get_y())
    return [xlist,ylist]

def getLocation2(dud):
    xlist = list()
    ylist = list()
    for i in dud:
        if i.get_infected()==True:
            xlist.append(i.get_x())
            ylist.append(i.get_y())
    return [xlist,ylist]

def getLocationP(dud): #personlist of infected
    plist = list()
    for i in dud:
        if i.get_infected()==False:
            continue
        plist.append(i)
    return plist

def infectOne(val, dud):
    plist = getLocationP(dud)
    #val = valal
    for i in plist: #every person infects one person
        aa = int(i.get_x()/50)
        bb = int(i.get_y()/50)
        new_val = val[aa][bb]
        lengt = len(new_val)
        if lengt>0:
            rnd = np.random.randint(0,lengt)
            if dud[dud.index(new_val[rnd])].get_infected() == False:
                dud[dud.index(new_val[rnd])].set_infected(True)
                #print(0)
    return dud
    
def countt(dud):
    counter =0
    for i in dud:
        if i.get_infected() == True:
            counter+=1
    return counter

# start from here

du = SimalationData()
du.intialData()
du.infect_initial()
k=du.intialData()
du.createStoreMatrix()
valal = du.getStoreMatrix()


#print(sum/cc)


# exit()
fig = plt.figure()
ax = plt.axes(xlim = (0,1001), ylim = (0,1001))
d, = ax.plot([],[],'g*')
d1, = ax.plot([],[],'r*')



def animate(i):
    k=du.movement()
    print(countt(k))
    k=infectOne(valal, k)
    print(countt(k)) #just to track if we are infecting
    k1=getLocation1(k)
    k2=getLocation2(k)
    d.set_data(k1[0],k1[1])
    d1.set_data(k2[0],k2[1])
    #circle = plt.Circle((1,2),1,color = 'Blue', fill = 'false')
    #ax.add_artist(circle)
    return d

anim = animation.FuncAnimation(fig, animate, frames=200,interval =100) #change interval to change speed


plt.show()