from ConfigUtil import ConfigUtil
from Person import Person
import matplotlib.pyplot as plt



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
    for i in population_set:
        if(i.get_gender()=="M"):
            print("-----------------------------------------------------")
            xm.append(i.get_x())
            ym.append(i.get_y())
        else:
            xf.append(i.get_x())
            yf.append(i.get_y())


    # plotting the points 
    plt.scatter(xm, ym, label= "stars", color= "green", marker= "*",s=50)
    plt.scatter(xf, yf, label= "stars", color= "red", marker= "*",s=50)
    
    # naming the x axis
    plt.xlabel('x - cordinate')
    # naming the y axis
    plt.ylabel('y - cordinate')
    
    # giving a title to my graph
    plt.title('Population Scatter Graph')
    
    # function to show the plot
    plt.show()