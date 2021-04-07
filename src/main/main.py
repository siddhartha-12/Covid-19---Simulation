from ConfigUtil import ConfigUtil
from Person import Person
from matplotlib import pyplot as plt
import matplotlib.animation
import numpy as np



if __name__=="__main__":
    config = ConfigUtil.get_instance()
    population_set = list()
    population = int(config.get_value("SIMULATION","population"))
    for i in range(population):
        population_set.append(Person())
    xm = list()
    xf =list()
    ym = list()
    yf = list()
    color = list()
    x= list()
    y = list()
    current = 0
    
    for i in population_set:
        if(i.get_gender()=="M"):
            xm.append(i.get_x())
            ym.append(i.get_y())
            color.append("green")
        else:
            xf.append(i.get_x())
            yf.append(i.get_y())
            color.append("purple")
        x.append(i.get_x())
        y.append(i.get_y())


    # # plotting the points 
    # plt.scatter(x, y, label= "stars", color= color, marker= "*",s=50)
    
    # # naming the x axis
    # plt.xlabel('x - cordinate')
    # # naming the y axis
    # plt.ylabel('y - cordinate')
    
    # # giving a title to my graph
    # plt.title('Population Scatter Graph')
    
    fig, ax = plt.subplots()
    x1, y1 = [],[]
    sc = ax.scatter(x1, y1, label= "stars", marker= "*",s=50)
    plt.xlim(0,75)
    plt.ylim(0,75)

    

    def animate(i):
        global current
        x1.append(x[current])
        y1.append(y[current])
        current +=1
        sc.set_offsets(np.c_[x1,y1])
    
    ani = matplotlib.animation.FuncAnimation(fig, animate,frames=len(x)-2, interval=10, repeat=False) 


    # function to show the plot
    plt.show()