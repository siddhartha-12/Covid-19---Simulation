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

        self.kk=1
        

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

        container = tk.Frame(self)
        # container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.cont=controller
        label = tk.Label(self, text="Virus Simulation", font=LARGE_FONT)
        label.pack(pady=30,padx=300, side ='top')

        label0 = tk.Label(self, text="", font=LARGE_FONT)
        label0.pack(pady=200,padx=200)

        btnConfig = ttk.Button(self, text="Set Configuration",command=lambda: controller.show_frame(ConfigurationPanel))
        btnConfig.place(x=100,y=200)

        btnStart = ttk.Button(self, text="Simulation Window",command=self.sim_window)
        btnStart.place(x=100,y=250)

        btnRender = ttk.Button(self, text="Render")
        btnRender.place(x=100,y=300)
    
    def sim_window(self):
        label01 = tk.Label(self, text="", font=LARGE_FONT)
        label01.pack(pady=2000,padx=2000)
        self.cont.show_frame(StartPanel)

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
            conf.set_population(population)
            
        except:
            flag=1
            errorMessage+="Population\n"

        try:
            daysContagious = int(self.txtDaysContagious.get(1.0,"end-1c"))
            conf.set_days_contageous(daysContagious)
        except:
            flag=1
            errorMessage+="No of days contagious\n"

        try:
            initialInfectedPer = int(self.txtInitialInfectedPer.get(1.0,"end-1c"))
            conf.set_initial_infected_percentage(initialInfectedPer)
        except:
            flag=1
            errorMessage+="Initial infected percentage\n"

        try:
            maskIntroducedTimeline = int(self.txtMaskIntroducedTimeline.get(1.0,"end-1c"))
            conf.set_mask_introduced_timeline(maskIntroducedTimeline)
        except:
            flag=1
            errorMessage+="Mask introduced timeline\n"

        try:
            quarantineIntroducedTimeline = int(self.txtQuarantineIntroducedTimeline.get(1.0,"end-1c"))
            conf.set_quarantine_introduced_timeline(quarantineIntroducedTimeline)
        except:
            flag=1
            errorMessage+="Quarantine introduced timeline\n"

        try:
            vaccineIntroducedTimeline = int(self.txtVaccineIntroducedTimeline.get(1.0,"end-1c"))
            conf.set_vaccine_effectiveness(vaccineIntroducedTimeline)
        except:
            flag=1
            errorMessage+="Vaccine Introduced Timeline\n"
        if flag==1:
            tk.messagebox.showinfo("Error",errorMessage+" should be numbers")
        

        



class StartPanel(tk.Frame):

    def __init__(self, parent, controller):        
        self.cont = controller
        self.dots_graph = None
        self.lineCanvas = None
        self.lgCanvas = None
        self.time =0
       
        self.pare = parent

        self.infected_log = np.array([])
        self.healthy_log = np.array([])
        self.recovered_log = np.array([])
        self.deceased_log = np.array([])
        self.super_log = np.array([])
        self.mask_log = np.array([])
        self.quarantine_log = np.array([])
        self.vaccine_log = np.array([])
        self.time_log = np.array([])

        self.xlimit = 100
        self.ylimit = 0

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Simulation", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        self.timer_name = tk.Label(self,text="Timer")
        self.timer_name.place(x=150,y=200)
        self.timer_label = tk.Label(self, text="")
        self.timer_label.place(x=200,y=200)
        self.no_of_infected = tk.Label(self,text="No. of Infected")
        self.no_of_infected.place(x=100,y=250)

        #---------- radio buttons ------------
        self.infected_box=tk.BooleanVar()
        self.infected_box.set(True)
        self.checkInfected = tk.Checkbutton(self,text='Infected', var=self.infected_box,onvalue=1,offvalue=0)
        self.checkInfected.place(x=950,y=80)

        self.healthy_box=tk.BooleanVar()
        self.healthy_box.set(True)
        self.checkHealthy = tk.Checkbutton(self,text='Healthy', var=self.healthy_box,onvalue=1,offvalue=0)
        self.checkHealthy.place(x=950,y=110)

        self.recovered_box=tk.BooleanVar()
        self.recovered_box.set(True)
        self.checkRecovered = tk.Checkbutton(self,text='Recovered', var=self.recovered_box,onvalue=1,offvalue=0)
        self.checkRecovered.place(x=950,y=140)

        self.dead_box=tk.BooleanVar()
        self.dead_box.set(True)
        self.checkDead = tk.Checkbutton(self,text='Dead', var=self.dead_box,onvalue=1,offvalue=0)
        self.checkDead.place(x=950,y=170)

        self.super_box=tk.BooleanVar()
        self.super_box.set(True)
        self.checkSuper = tk.Checkbutton(self,text='Super Spreader', var=self.super_box,onvalue=1,offvalue=0)
        self.checkSuper.place(x=950,y=200)

        self.mask_box=tk.BooleanVar()
        self.mask_box.set(True)
        self.checkMask = tk.Checkbutton(self,text='Mask usage', var=self.mask_box,onvalue=1,offvalue=0)
        self.checkMask.place(x=950,y=230)

        self.quarantine_box=tk.BooleanVar()
        self.quarantine_box.set(True)
        self.checkquarantine = tk.Checkbutton(self,text='Quarantine usage', var=self.quarantine_box,onvalue=1,offvalue=0)
        self.checkquarantine.place(x=950,y=260)

        self.vaccine_box=tk.BooleanVar()
        self.vaccine_box.set(True)
        self.checkquarantine = tk.Checkbutton(self,text='Quarantine usage', var=self.vaccine_box,onvalue=1,offvalue=0)
        self.checkquarantine.place(x=950,y=290)

        btnBack = ttk.Button(self, text = "<< back", command=self.backOnClick)
        btnBack.place(x=20, y=80)

        btnSim = ttk.Button(self, text = "Simulate", command=self.startSim)
        btnSim.place(x=950, y=330)

        self.canvass = tk.Canvas(self,height=300, width = 500,background='white')
        self.canvass.place(x=300,y=50)

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        # self.fig.clear()
       
        self.ax.set_title('Time series graph')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('No of people')
        self.ax.set_xlim(0,self.xlimit)
        self.ax.set_ylim(0,self.ylimit)
        
       
        self.lines = self.ax.plot([],[],'-r',label='Infected')[0]
        self.ax.plot([],[],'-b',label='Healthy')[0]
        self.ax.plot([],[],'-g',label='Recovered')[0]
        

        self.lineCanvas = po.FigureCanvasTkAgg(self.fig, master = self)
        self.lineCanvas.get_tk_widget().place(x=50,y=420, width = 500,height = 300)
        

        self.fig_lg = Figure()
        self.ax_lg = self.fig_lg.add_subplot(111)
       

        self.ax_lg.set_title('Logarithmic graph')
        self.ax_lg.set_xlabel('Time')
        self.ax_lg.set_ylabel('Log og no of people')
        
       
        self.lines_lg = self.ax_lg.plot([],[],'r',label ='Infected')[0]

        self.lgCanvas = po.FigureCanvasTkAgg(self.fig_lg, master = self)
        self.lgCanvas.get_tk_widget().place(x=600,y=420, width = 500,height = 300)
        self.lgCanvas.draw()


        self.canvass.delete('all')
        
    def backOnClick(self):
        
        self.fig.clear(True)
        self.ax_lg.clear()
        self.cancel_oval()
        self.canvass.delete('all')
        
        if self.time>0:
            self.time=0
            self.time_log=np.array([])
        
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
       
        self.ax.set_title('Time series graph')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('No of people')
        self.ax.set_xlim(0,self.xlimit)
        self.ax.set_ylim(0,self.ylimit)
        
       
        self.lines = self.ax.plot([],[],'-r',label='Infected')[0]
        self.ax.plot([],[],'-b',label='Healthy')[0]
        self.ax.plot([],[],'-g',label='Recovered')[0]
        self.leg = self.ax.legend()

        self.lineCanvas = po.FigureCanvasTkAgg(self.fig, master = self)
        self.lineCanvas.get_tk_widget().place(x=50,y=420, width = 500,height = 300)

        self.fig_lg = Figure()
        self.ax_lg = self.fig_lg.add_subplot(111)
       

        self.ax_lg.set_title('Logarithmic graph')
        self.ax_lg.set_xlabel('Time')
        self.ax_lg.set_ylabel('Log og no of people')
        
       
        self.lines_lg = self.ax_lg.plot([],[],'r',label ='Infected')[0]

        self.lgCanvas = po.FigureCanvasTkAgg(self.fig_lg, master = self)
        self.lgCanvas.get_tk_widget().place(x=600,y=420, width = 500,height = 300)
        self.lgCanvas.draw()
        self.cont.show_frame(DefaultPanel)

    def startSim(self):

        self.canvass.delete('all')
        self.cancel_line()
        self.cancel_oval()
        self.cancel_lg()
        self.lineCanvas= None
        self.lgCanvas=None


        self.cu = Config.get_instance()
        self.sd = SimalationData()
        self.du = DataUtil()
        self.dataset = self.sd.getDataset()
        self.pu = PersonUtil()
        self.time = 0
        self.infected_location_dict = dict()
        self.ylimit = self.cu.get_population()

        self.canvass = tk.Canvas(self,height=300, width = 500,background='white')
        self.canvass.place(x=300,y=50)


        #--------- time series graph ------------
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
       
        self.ax.set_title('Time series graph')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('No of people')
        self.ax.set_xlim(0,self.xlimit)
        self.ax.set_ylim(0,self.ylimit)
        
       
        self.lines = self.ax.plot([],[],'-r',label='Infected')[0]
        self.ax.plot([],[],'-b',label='Healthy')[0]
        self.ax.plot([],[],'-g',label='Recovered')[0]
        self.ax.plot([],[],'black',label='Deceased')[0]
        self.leg = self.ax.legend()

        self.lineCanvas = po.FigureCanvasTkAgg(self.fig, master = self)
        self.lineCanvas.get_tk_widget().place(x=50,y=420, width = 500,height = 300)
        self.lineCanvas.draw()

        #--------- log graph ------------

        self.fig_lg = Figure()
        self.ax_lg = self.fig_lg.add_subplot(111)
       

        self.ax_lg.set_title('Logarithmic graph')
        self.ax_lg.set_xlabel('Time')
        self.ax_lg.set_ylabel('Log of no of people')
        self.ax_lg.set_xlim(0,self.xlimit)
        self.ax_lg.set_ylim(0,np.log(self.ylimit))
       
        self.lines_lg = self.ax_lg.plot([],[],'r',label ='Infected')[0]
        self.leg_lg = self.ax_lg.legend()
        self.lgCanvas = po.FigureCanvasTkAgg(self.fig_lg, master = self)
        self.lgCanvas.get_tk_widget().place(x=600,y=420, width = 500,height = 300)
        self.lgCanvas.draw()


        self.move_oval()
    
    def add_infected_to_dict(self,x,y,id):
        if (x,y) in self.infected_location_dict:
            oid = self.infected_location_dict[(x,y)]
            old = int(self.dataset[oid].get_can_infect())
            new = int(self.dataset[id].get_can_infect())
            if new>old:
                self.infected_location_dict[x,y] = id
        else:
            self.infected_location_dict[x,y] = id
 
    
    def createCluster(self,x,y,id):
        self.add_infected_to_dict(x, y, id)
        self.add_infected_to_dict(x-1, y-1, id)
        self.add_infected_to_dict(x-1, y, id)
        self.add_infected_to_dict(x-1, y+1, id)
        self.add_infected_to_dict(x, y+1, id)
        self.add_infected_to_dict(x, y-1, id)
        self.add_infected_to_dict(x+1, y-1, id)
        self.add_infected_to_dict(x+1, y, id)
        self.add_infected_to_dict(x+1, y+1, id)

    def cancel_oval(self):
        if self.dots_graph is not None:
            self.canvass.after_cancel(self.dots_graph)
            self.dots_graph = None
           

    def cancel_line(self):
        if self.lineCanvas is not None:
            self.lineCanvas.close_event()
        self.ax.plot([],[])
        self.infected_log=np.array([])
        self.healthy_log=np.array([])
        self.recovered_log=np.array([])
        self.deceased_log = np.array([])
        self.time_log = np.array([])
        self.super_log = np.array([])
        self.mask_log = np.array([])
        self.quarantine_log = np.array([])
        self.vaccine_log = np.array([])
    
    def cancel_lg(self):
        if self.lgCanvas is not None:
            self.lgCanvas.close_event()

    def move_oval(self):
        # self.ax.get_legend().remove()

        self.time += 1
        self.canvass.delete('all')
        #Repopulating infected zones
        locations = self.du.getLocationInfected(self.dataset)
        for x,y,z in zip(locations[0],locations[1],locations[2]):
            self.createCluster(x, y, z)

        #Updating status for every person
        for i in range(len(self.dataset)):
            if not self.dataset[i].get_deceased():
                if not self.dataset[i].get_recovered() and not self.dataset[i].get_infected() and not self.dataset[i].get_vaccinated():
                    x,y = self.dataset[i].get_x(), self.dataset[i].get_y()
                    if (x,y) in self.infected_location_dict:
                        self.dataset[i],quo = self.pu.updatePerson(True, self.dataset[i],self.time)
                        if(quo):
                            got_infected_from = self.infected_location_dict[(x,y)]
                            self.dataset[got_infected_from].set_can_infect(self.dataset[got_infected_from].get_can_infect()-1)
                    else:
                         self.dataset[i] = self.pu.updatePerson(False,self.dataset[i],self.time)[0]
                # elif self.dataset[i].get_infected() and not self.dataset[i].get_vaccinated():
                #     # if self.dataset[i].get_can_infect() > 0:
                #     #     self.createCluster( self.dataset[i].get_x(), self.dataset[i].get_y(), self.dataset[i].get_id())
                else:
                    self.dataset[i] = self.pu.updatePerson(False, self.dataset[i],self.time)[0]

        counts  = self.du.getTotalCountAll(self.dataset)

            
        # infectedDS = self.du.getLocationInfected(self.dataset)
        # healthyDS =  self.du.getLocationHealthy(self.dataset)
        # self.infectedxlist=infectedDS[0]
        # self.infectedylist=infectedDS[1]
        # self.healthyXlist = healthyDS[0]
        # self.healthyYlist = healthyDS[1]
        # self.infected_length = len(self.infectedxlist)
        # self.healthy_lenght = len(self.healthyXlist)
        self.timer_label.config(text="Time : " + str(int(self.time)))
        self.no_of_infected.config(text="Infected  :" +str(counts["Infected"]) +"\nSuper Spreader : " + str(counts["Super"]) + "\nRecovered  :" +str(counts["Recover"]) + "\nDeceased  :" +str(counts["Dead"]) +"\nHealthy : " + str(counts["Healthy"]) + "\nMask Usage  :" +str(counts["Mask"]) + "\nQuarantined  :" +str(counts["Quarantine"]) +"\nVaccinated : " + str(counts["Vaccinate"]) +"\nPredicted more infection: " + str(int(self.cu.get_total_to_infect())) )
        for i in range(len(self.dataset)):
            if(self.dataset[i].get_infected()):
                if(self.dataset[i].get_can_infect()>0):
                    c='orange'
                else:
                    c='red'
            else:
                c='blue'
            if(self.dataset[i].get_recovered()):
                c='green'
            if(self.dataset[i].get_deceased()):
                c="black"
            self.canvass.create_oval(self.dataset[i].get_x()/2-4,self.dataset[i].get_y()/3-4,self.dataset[i].get_x()/2+4,self.dataset[i].get_y()/3+4, fill = c)
        
        if self.time == self.xlimit:
            self.xlimit *=2
            self.ax_lg.set_xlim(0, self.xlimit)
            self.ax.set_xlim(0,self.xlimit)
        # self.infected_count = self.du.getTotalCountInfected(self.sd.getDataset())
        # self.healthy_count = self.du.getTotalCountHealthy(self.sd.getDataset())
        # self.recovered_count = self.du.getTotalCountRecovered(self.sd.getDataset())


        
        self.infected_log = np.append(self.infected_log,counts["Infected"])
        self.healthy_log = np.append(self.healthy_log, counts["Healthy"])
        self.recovered_log = np.append(self.recovered_log, counts["Recover"])
        self.deceased_log = np.append(self.deceased_log, counts["Dead"])
        
        self.super_log = np.append(self.super_log,counts["Super"])
        self.mask_log = np.append(self.mask_log,counts["Mask"])
        self.quarantine_log = np.append(self.quarantine_log,counts["Quarantine"])
        self.vaccine_log = np.append(self.vaccine_log,counts["Vaccinate"])
        self.time_log = np.append(self.time_log,self.time)


        if self.infected_box.get() ==1:
            self.ax.plot(self.time_log,self.infected_log,'r')[0]
        if self.healthy_box.get() ==1:
            self.ax.plot(self.time_log,self.healthy_log,'b')[0]
        if self.recovered_box.get() ==1:
            self.ax.plot(self.time_log,self.recovered_log,'g')[0]
        if self.dead_box.get() ==1:
            self.ax.plot(self.time_log,self.deceased_log,'black')[0]
        if self.super_box.get() ==1:
            self.ax.plot(self.time_log,self.super_log,'yellow')[0]
        if self.mask_box.get() ==1:
            self.ax.plot(self.time_log,self.mask_log,'pink')[0]
        if self.quarantine_box.get() ==1:
            self.ax.plot(self.time_log,self.quarantine_log,'cyan')[0]
        if self.vaccine_box.get() ==1:
            self.ax.plot(self.time_log,self.vaccine_log,'lime')[0]
        # self.leg =self.ax.legend()
        
        self.lineCanvas.draw()

        self.ax_lg.plot(self.time_log,np.log(self.infected_log),'r')[0]
        # self.ax.plot(np.arange(0,self.time),self.healthy_log,'g-')[0]
        
        self.lgCanvas.draw()
        self.dots_graph=self.canvass.after(100,self.move_oval)
        

    

window = DefaultFrame()
window.geometry('1150x1500')
window.resizable(True,True)
window.mainloop()
