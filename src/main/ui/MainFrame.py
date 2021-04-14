import os
import sys
cwd = os.getcwd()+"/src/main"
sys.path.insert(1,cwd)
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.backends.backend_tkagg as po
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import numpy as np
import matplotlib.pyplot as plt
import time
import asyncio

import tkinter as tk
from tkinter import ttk

from Config import Config
from SimulationData import SimalationData
from DataUtil import DataUtil
from PersonUtil import PersonUtil

LARGE_FONT= ("Verdana", 25)
style.use("ggplot")



class DefaultFrame(tk.Tk):

    popo=10
    # cu = Config.get_instance()
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Covid 19 simulation")

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        con = Config.get_instance()
        con.load_from_file("COVID19")
        

        self.frames = {}
        

        for F in (DefaultPanel, ConfigurationPanel, StartPanel):

            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(DefaultPanel)
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class DefaultPanel(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Virus Simulation", font=LARGE_FONT)
        label.pack(pady=30,padx=30)

        btnConfig = ttk.Button(self, text="Set Configuration",command=lambda: controller.show_frame(ConfigurationPanel))
        btnConfig.place(x=100,y=200)

        btnStart = ttk.Button(self, text="Start Simulation",command=lambda: controller.show_frame(StartPanel))
        btnStart.place(x=100,y=250)

        btnRender = ttk.Button(self, text="Render")
        btnRender.place(x=100,y=300)

class ConfigurationPanel(tk.Frame):

    def __init__(self, parent, controller):
        conf=Config.get_instance()
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Configuration", font=LARGE_FONT)
        self.label.pack(pady=10,padx=10)
        self.pop=0
        
        self.btnBack = ttk.Button(self, text = "<< back", command=lambda: controller.show_frame(DefaultPanel))
        self.btnBack.place(x=20, y=80)

        self.lblVirusType = tk.Label(self, text="Select Virus")
        self.lblVirusType.place(x=400, y=150)

        self.comboBoxVirus = ttk.Combobox(self, state = 'readonly', values = ['Covid19','Sars','Mers'])
        self.comboBoxVirus.place(x=500, y=150)
        self.comboBoxVirus.current(0)

        #combobox on change

        self.lblPopulation = tk.Label(self, text="Population")
        self.lblPopulation.place(x=200,y=250)

        self.txtPopulation = tk.Text(self, height =1, width = 25)
        self.txtPopulation.insert("end",str(conf.get_population()))
        self.txtPopulation.place(x=300,y=250)

        self.lblInitialInfectedPer = tk.Label(self, text="Initial Infected Percentage")
        self.lblInitialInfectedPer.place(x=105,y=300)

        self.txtInitialInfectedPer = tk.Text(self, height =1, width = 25)
        self.txtInitialInfectedPer.insert("end",str(conf.get_initial_infected_percentage()))
        self.txtInitialInfectedPer.place(x=300,y=300)

        self.lblRFactor = tk.Label(self, text="R factor")
        self.lblRFactor.place(x=215,y=350)

        self.sdrRFactor = tk.Scale(self, from_=0, to=10, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=1,command=self.set_valueRFactor)
        self.sdrRFactor.set(conf.get_r_factor())
        self.sdrRFactor.place(x=300,y=350)

        self.lblRFactorVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =3)
        self.lblRFactorVal.place(x=450,y=350)

        self.lblKFactor = tk.Label(self, text="K factor")
        self.lblKFactor.place(x=215,y=400)

        self.sdrKFactor = tk.Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.01,command=self.set_valueKFactor)
        self.sdrKFactor.set(conf.get_k_factor())
        self.sdrKFactor.place(x=300,y=400)

        self.lblKFactorVal = tk.Label(self,text=self.sdrKFactor.get(), height =1, width =3)
        self.lblKFactorVal.place(x=450,y=400)

        self.lblDaysContagious = tk.Label(self, text="Days Contagious")
        self.lblDaysContagious.place(x=160,y=450)

        self.txtDaysContagious = tk.Text(self, height =1, width = 25)
        self.txtDaysContagious.insert("end",str(conf.get_days_contageous()))
        self.txtDaysContagious.place(x=300,y=450)

        #mask

        self.lblMaskIntroducedTimeline = tk.Label(self, text="Mask Timeline")
        self.lblMaskIntroducedTimeline.place(x=180,y=500)

        self.txtMaskIntroducedTimeline = tk.Text(self, height =1, width = 25)
        self.txtMaskIntroducedTimeline.insert("end",str(conf.get_mask_introduced_timeline()))
        self.txtMaskIntroducedTimeline.place(x=300,y=500)

        self.lblMaskUsuageEffectiveness = tk.Label(self, text="Mask Usuage Effectiveness")
        self.lblMaskUsuageEffectiveness.place(x=95,y=550)

        self.sdrMaskUsuageEffectiveness = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueMaskUsuageEffectiveness)
        self.sdrMaskUsuageEffectiveness.set(conf.get_mask_usage_effectiveness())
        self.sdrMaskUsuageEffectiveness.place(x=300,y=550)

        self.lblMaskUsuageEffectivenessVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblMaskUsuageEffectivenessVal.place(x=450,y=550)

        self.lblMaskUsuagePercentage = tk.Label(self, text="Mask Usage Percentage")
        self.lblMaskUsuagePercentage.place(x=115,y=600)

        self.sdrMaskUsuagePercentage = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueMaskUsuagePercentage)
        self.sdrMaskUsuagePercentage.set(conf.get_mask_usage_percentage())
        self.sdrMaskUsuagePercentage.place(x=300,y=600)

        self.lblMaskUsuagePercentageVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblMaskUsuagePercentageVal.place(x=450,y=600)

        #quarantine

        self.lblQuarantineIntroducedTimeline = tk.Label(self, text = "Quarantine Timeline")
        self.lblQuarantineIntroducedTimeline.place(x=100+500,y=250)

        self.txtQuarantineIntroducedTimeline = tk.Text(self, height =1, width = 25)
        self.txtQuarantineIntroducedTimeline.insert("end",str(conf.get_quarantine_introduced_timeline()))
        self.txtQuarantineIntroducedTimeline.place(x=250+500,y=250)

        self.lblQuarantineEffectiveness = tk.Label(self, text="Quarantine Effectiveness")
        self.lblQuarantineEffectiveness.place(x=70+500,y=300)

        self.sdrQuarantineUsuageEffectiveness = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueQuarantineUsuageEffectiveness)
        self.sdrQuarantineUsuageEffectiveness.set(conf.get_qurantine_effectiveness())
        self.sdrQuarantineUsuageEffectiveness.place(x=250+500,y=300)

        self.lblQuarantineUsuageEffectivenessVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblQuarantineUsuageEffectivenessVal.place(x=400+500,y=300)

        self.lblQuarantinePercentage = tk.Label(self, text="Quarantining Percentage")
        self.lblQuarantinePercentage.place(x=70+500,y=350)

        self.sdrQuarantinePercentage = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueQuarantinePercentage)
        self.sdrQuarantinePercentage.set(conf.get_qurantine_usage_percentage())
        self.sdrQuarantinePercentage.place(x=250+500,y=350)

        self.lblQuarantinePercentageVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblQuarantinePercentageVal.place(x=400+500,y=350)

        #vaccine

        self.lblVaccineIntroducedTimeline = tk.Label(self, text="Vaccine Timeline")
        self.lblVaccineIntroducedTimeline.place(x=115+500,y=400)

        self.txtVaccineIntroducedTimeline = tk.Text(self, height =1, width = 25)
        self.txtVaccineIntroducedTimeline.insert("end",str(conf.get_vaccine_introduced_timeline()))
        self.txtVaccineIntroducedTimeline.place(x=250+500,y=400)

        self.lblVaccineEffectiveness = tk.Label(self, text="Vaccine Effectiveness")
        self.lblVaccineEffectiveness.place(x=85+500,y=450)

        self.sdrVaccineEffectiveness = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueVaccineEffectiveness)
        self.sdrVaccineEffectiveness.set(conf.get_vaccine_effectiveness())
        self.sdrVaccineEffectiveness.place(x=250+500,y=450)

        self.lblVaccineEffectivenessVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblVaccineEffectivenessVal.place(x=400+500,y=450)

        self.lblVaccinePercentage = tk.Label(self, text="Vaccine Percentage")
        self.lblVaccinePercentage.place(x=100+500,y=500)

        self.sdrVaccinePercentage = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueVaccinePercentage)
        self.sdrVaccinePercentage.set(conf.get_vaccine_usage_percentage())
        self.sdrVaccinePercentage.place(x=250+500,y=500)

        self.lblVaccinePercentageVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblVaccinePercentageVal.place(x=400+500,y=500)

        self.btnSet = ttk.Button(self, text="Set",command = self.setButtonOnClick)
        self.btnSet.place(x=470,y=650)
    
    def set_valueRFactor(self,v):
        self.lblRFactorVal.config(text=v)

    def set_valueKFactor(self,v):
        self.lblKFactorVal.config(text=v)

    def set_valueMaskUsuageEffectiveness(self,v):
        self.lblMaskUsuageEffectivenessVal.config(text=v+'%')

    def set_valueMaskUsuagePercentage(self,v):
        self.lblMaskUsuagePercentageVal.config(text=v+'%')

    def set_valueQuarantineUsuageEffectiveness(self,v):
        self.lblQuarantineUsuageEffectivenessVal.config(text=v+'%')

    def set_valueQuarantinePercentage(self,v):
        self.lblQuarantinePercentageVal.config(text=v+'%')

    def set_valueVaccineEffectiveness(self,v):
        self.lblVaccineEffectivenessVal.config(text=v+'%')

    def set_valueVaccinePercentage(self,v):
        self.lblVaccinePercentageVal.config(text=v+'%')
        #print(self.txtVaccineIntroducedTimeline.get(1.0,"end-1c"))

    def setButtonOnClick(self):
        conf = Config.get_instance()
        errorMessage =""
        flag =0

        try:
            population = int(self.txtPopulation.get(1.0,"end-1c"))
            print(population)
            conf.set_population(population)
            
        except:
            flag=1
            errorMessage+="Population\n"

        try:
            daysContagious = int(self.txtDaysContagious.get(1.0,"end-1c"))
            print(daysContagious)
            conf.set_days_contageous(daysContagious)
        except:
            flag=1
            errorMessage+="No of days contagious\n"

        try:
            initialInfectedPer = int(self.txtInitialInfectedPer.get(1.0,"end-1c"))
            print(initialInfectedPer)
            conf.set_initial_infected_percentage(initialInfectedPer)
        except:
            flag=1
            errorMessage+="Initial infected percentage\n"

        try:
            maskIntroducedTimeline = int(self.txtMaskIntroducedTimeline.get(1.0,"end-1c"))
            print(maskIntroducedTimeline)
            conf.set_mask_introduced_timeline(maskIntroducedTimeline)
        except:
            flag=1
            errorMessage+="Mask introduced timeline\n"

        try:
            quarantineIntroducedTimeline = int(self.txtQuarantineIntroducedTimeline.get(1.0,"end-1c"))
            print(quarantineIntroducedTimeline)
            conf.set_quarantine_introduced_timeline(quarantineIntroducedTimeline)
        except:
            flag=1
            errorMessage+="Quarantine introduced timeline\n"

        try:
            vaccineIntroducedTimeline = int(self.txtVaccineIntroducedTimeline.get(1.0,"end-1c"))
            print(vaccineIntroducedTimeline)
            conf.set_vaccine_effectiveness(vaccineIntroducedTimeline)
        except:
            flag=1
            errorMessage+="Vaccine Introduced Timeline\n"
        if flag==1:
            tk.messagebox.showinfo("Error",errorMessage+" should be numbers")
        

        



class StartPanel(tk.Frame):

    def __init__(self, parent, controller):
        self.sd = SimalationData()
        self.du = DataUtil()
        self.sd.getDataset()
        self.pu = PersonUtil()
        self.time =0
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Simulation", font=LARGE_FONT)
        label.pack(pady=10,padx=10) 
        btnBack = ttk.Button(self, text = "<< back", command=lambda: controller.show_frame(DefaultPanel))
        btnBack.place(x=20, y=80)
        self.canvass = tk.Canvas(self,height=300, width = 500,background='white')
        self.canvass.place(x=300,y=50)
        self.lineCanvas = tk.Canvas(self,height =300, width =500, background ='white')
        self.lineCanvas.place(x=300, y=450)
        self.dataset = self.sd.getDataset()
        infectedDS = self.du.getLocationInfected(self.dataset)
        healthyDS =  self.du.getLocationHealthy(self.dataset)
        self.infectedxlist=infectedDS[0]
        self.infectedylist=infectedDS[1]
        self.healthyXlist = healthyDS[0]
        self.healthyYlist = healthyDS[1]
        self.x_delta=list()
        self.y_delta=list()
        self.infected_length = len(self.infectedxlist)
        self.healthy_lenght = len(self.healthyXlist)

        # for i in range(self.infected_length):
        #     # self.xlist.append(np.random.randint(5,495))
        #     # self.ylist.append(np.random.randint(5,295))
        #     self.x_delta.append(1)
        #     self.y_delta.append(0.7)

        # for i in range(self.healthy_lenght):
        #     # self.xlist.append(np.random.randint(5,495))
        #     # self.ylist.append(np.random.randint(5,295))
        #     self.x_delta.append(1)
        #     self.y_delta.append(0.7)
        
        self.dotlist1=list()
        for i in range(1000):
            self.dotlist1.append(0)
        self.dotlist2=list()
        for i in range(1000):
            self.dotlist2.append(0)
        # self.prevy=0
        # for i in range(self.infected_length):
        #     self.dotlist.append(self.canvass.create_oval(self.infectedxlist[i]-4,self.infectedylist[i]-4,self.infectedxlist[i]+4,self.infectedylist[i]+4, fill='red'))
        # for i in range(self.healthy_lenght):
        #     self.dotlist.append(self.canvass.create_oval(self.healthyXlist[i]-4,self.healthyYlist[i]-4,self.healthyXlist[i]+4,self.healthyYlist[i]+4, fill='blue'))
        
        self.move_oval()
        # self.create_line()

        
    # def create_line(self):
        
    #     for i in range(490):
    #         self.lineCanvas.create_line(i,300-(self.prevy),i+1,300-(i*i), width=3,fill ='red')
    #         self.prevy=i*i

    #     self.lineCanvas.after(10,create_line)
        


    def move_oval(self):
        # for i in range(self.infected_length):
        #     chance=np.random.randint(0,100)
        #     if chance>90:
        #         kx=np.random.random()*np.random.choice([-1,1])
        #         if kx>0.5 or kx<-0.5:
        #             self.x_delta[i] = kx
        #         ky=np.random.random()*np.random.choice([-1,1])
        #         if ky>0.5 or ky<-0.5:
        #             self.y_delta[i] = ky
        #     if self.xlist[i]+self.x_delta[i]<0 or self.xlist[i]+self.x_delta[i]>500:
        #         self.x_delta[i]*=-1
        #     if self.ylist[i]+self.y_delta[i]<0 or self.ylist[i]+self.y_delta[i]>300:
        #         self.y_delta[i]*=-1
        #     self.xlist[i]+=self.x_delta[i]
        #     self.ylist[i]+=self.y_delta[i]
        self.time += 1
        for i in self.dataset:
            i = self.pu.updatePerson(True,i,self.time)[0]
            
        
        infectedDS = self.du.getLocationInfected(self.dataset)
        healthyDS =  self.du.getLocationHealthy(self.dataset)
        

        self.infectedxlist=infectedDS[0]
        self.infectedylist=infectedDS[1]

        self.healthyXlist = healthyDS[0]
        self.healthyYlist = healthyDS[1]

        self.x_delta=list()
        self.y_delta=list()

        self.infected_length = len(self.infectedxlist)
        self.healthy_lenght = len(self.healthyXlist)
        
        for i in range(self.infected_length):
            self.canvass.delete(self.dotlist1[i])
            self.dotlist1[i]=self.canvass.create_oval(self.infectedxlist[i]-4,self.infectedylist[i]-4,self.infectedxlist[i]+4,self.infectedylist[i]+4, fill='red')
            
        for i in range(self.healthy_lenght):
            self.canvass.delete(self.dotlist2[i])
            self.dotlist2[i]=self.canvass.create_oval(self.healthyXlist[i]-4,self.healthyYlist[i]-4,self.healthyXlist[i]+4,self.healthyYlist[i]+4, fill='blue')

            # self.canvass.move(self.dotlist[i],1,1)
            # self.canvass.move(self.dotlist[i],self.x_delta[i],self.y_delta[i])
            #self.canvass.itemconfig(self.dotlist[i],fill='green')
            #print(self.xlist[i]," ,",self.ylist[i])
            #print(self.x_delta[i],",",self.y_delta[i],np.random.randint(4))
            # print(DefaultFrame.popo,np.random.randint(4))

        
        self.canvass.after(10,self.move_oval)



window = DefaultFrame()
window.geometry('1000x1000')
window.mainloop()
