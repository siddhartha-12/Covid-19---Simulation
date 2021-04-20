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
matplotlib.rcParams['figure.autolayout'] = True
from math import log2,log
import numpy as np
import matplotlib.pyplot as plt
import time
import asyncio
from tkinter import StringVar
import tkinter as tk
from tkinter import ttk
from Config import Config
from SimulationData import SimalationData
from DataUtil import DataUtil
from PersonUtil import PersonUtil
from ConfigUtil import ConfigUtil

LARGE_FONT= ("Verdana", 25)
MED_FONT = ("Verdana", 18)
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
        
#------------ image on first panel ---------------
        self.img = tk.PhotoImage(file =cwd+"/images/background_image.png")
        bg_img = tk.Label(self,image=self.img)
        bg_img.place(x=500,y=100)
        
        label = tk.Label(self, text="Virus Simulation", font=LARGE_FONT)
        label.pack(pady=30,padx=300, side ='top')

        # label0 = tk.Label(self, text="", font=LARGE_FONT)
        # label0.pack(pady=200,padx=200)

#------------ config and window buttons -------------

        btnConfig = ttk.Button(self, text="Set Configuration",command=lambda: controller.show_frame(ConfigurationPanel),width=20)
        btnConfig.place(x=600,y=200)

        btnStart = ttk.Button(self, text="Simulation Window",command=self.sim_window,width=20)
        btnStart.place(x=600,y=250)
        
    
    def sim_window(self):
        label01 = tk.Label(self, text="", font=LARGE_FONT)
        label01.pack(pady=2000,padx=2000)
        self.cont.show_frame(StartPanel)

class ConfigurationPanel(tk.Frame):

    def __init__(self, parent, controller):
        self.conf=Config.get_instance()
        tk.Frame.__init__(self, parent)
        self.xadd=200
        self.label = tk.Label(self, text="Configuration", font=LARGE_FONT)
        self.label.pack(pady=10,padx=10)
        self.pop=0
        self.cutil = ConfigUtil.get_instance()

        
        self.btnBack = ttk.Button(self, text = "<< back", command=lambda: controller.show_frame(DefaultPanel))
        self.btnBack.place(x=20, y=80)

        self.lblVirusType = tk.Label(self, text="Select Virus")
        self.lblVirusType.place(x=400+self.xadd, y=150)


#---------------- combobox to select virus -----------------------

        self.combovar= StringVar()
        self.combovar.trace('w',self.on_change)
        list_disease = self.cutil.get_all_sections()
        self.comboBoxVirus = ttk.Combobox(self, textvar=self.combovar, state = 'readonly', values = list_disease[1:])
        self.comboBoxVirus.place(x=500+self.xadd, y=150)
        self.comboBoxVirus.current(0)
        self.set_virus_properties()

        #combobox on change
    def set_virus_properties(self):
        self.conf=Config.get_instance()
        self.lblPopulation = tk.Label(self, text="Population")
        self.lblPopulation.place(x=200+self.xadd,y=250)

        self.txtPopulation = tk.Text(self, height =1, width = 25)
        self.txtPopulation.insert("end",str(self.conf.get_population()))
        self.txtPopulation.place(x=300+self.xadd,y=250)

        self.lblInitialInfectedPer = tk.Label(self, text="Initial Infected Percentage")
        self.lblInitialInfectedPer.place(x=105+self.xadd,y=300)

        self.txtInitialInfectedPer = tk.Text(self, height =1, width = 25)
        self.txtInitialInfectedPer.insert("end",str(self.conf.get_initial_infected_percentage()))
        self.txtInitialInfectedPer.place(x=300+self.xadd,y=300)

        self.lblRFactor = tk.Label(self, text="R factor")
        self.lblRFactor.place(x=215+self.xadd,y=350)

        self.sdrRFactor = tk.Scale(self, from_=0, to=10, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=1,command=self.set_valueRFactor)
        self.sdrRFactor.set(self.conf.get_r_factor())
        self.sdrRFactor.place(x=300+self.xadd,y=350)

        self.lblRFactorVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =3)
        self.lblRFactorVal.place(x=450+self.xadd,y=350)

        self.lblKFactor = tk.Label(self, text="K factor")
        self.lblKFactor.place(x=215+self.xadd,y=400)

        self.sdrKFactor = tk.Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.01,command=self.set_valueKFactor)
        self.sdrKFactor.set(self.conf.get_k_factor())
        self.sdrKFactor.place(x=300+self.xadd,y=400)

        self.lblKFactorVal = tk.Label(self,text=self.sdrKFactor.get(), height =1, width =3)
        self.lblKFactorVal.place(x=450+self.xadd,y=400)

        self.lblDaysContagious = tk.Label(self, text="Days Contagious")
        self.lblDaysContagious.place(x=160+self.xadd,y=450)

        self.txtDaysContagious = tk.Text(self, height =1, width = 25)
        self.txtDaysContagious.insert("end",str(self.conf.get_days_contageous()))
        self.txtDaysContagious.place(x=300+self.xadd,y=450)

#------------------------- mask -------------------------

        self.lblMaskIntroducedTimeline = tk.Label(self, text="Mask Timeline")
        self.lblMaskIntroducedTimeline.place(x=180+self.xadd,y=500)

        self.txtMaskIntroducedTimeline = tk.Text(self, height =1, width = 25)
        self.txtMaskIntroducedTimeline.insert("end",str(self.conf.get_mask_introduced_timeline()))
        self.txtMaskIntroducedTimeline.place(x=300+self.xadd,y=500)

        self.lblMaskUsuageEffectiveness = tk.Label(self, text="Mask Usuage Effectiveness")
        self.lblMaskUsuageEffectiveness.place(x=95+self.xadd,y=550)

        self.sdrMaskUsuageEffectiveness = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueMaskUsuageEffectiveness)
        self.sdrMaskUsuageEffectiveness.set(self.conf.get_mask_usage_effectiveness())
        self.sdrMaskUsuageEffectiveness.place(x=300+self.xadd,y=550)

        self.lblMaskUsuageEffectivenessVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblMaskUsuageEffectivenessVal.place(x=450+self.xadd,y=550)

        self.lblMaskUsuagePercentage = tk.Label(self, text="Mask Usage Percentage")
        self.lblMaskUsuagePercentage.place(x=115+self.xadd,y=600)

        self.sdrMaskUsuagePercentage = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueMaskUsuagePercentage)
        self.sdrMaskUsuagePercentage.set(self.conf.get_mask_usage_percentage())
        self.sdrMaskUsuagePercentage.place(x=300+self.xadd,y=600)

        self.lblMaskUsuagePercentageVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblMaskUsuagePercentageVal.place(x=450+self.xadd,y=600)

#------------------------- quarantine -------------------------
        self.lblQuarantineIntroducedTimeline = tk.Label(self, text = "Quarantine Timeline")
        self.lblQuarantineIntroducedTimeline.place(x=100+500+self.xadd,y=250)

        self.txtQuarantineIntroducedTimeline = tk.Text(self, height =1, width = 25)
        self.txtQuarantineIntroducedTimeline.insert("end",str(self.conf.get_quarantine_introduced_timeline()))
        self.txtQuarantineIntroducedTimeline.place(x=250+500+self.xadd,y=250)

        self.lblQuarantineEffectiveness = tk.Label(self, text="Quarantine Effectiveness")
        self.lblQuarantineEffectiveness.place(x=70+500+self.xadd,y=300)

        self.sdrQuarantineUsuageEffectiveness = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueQuarantineUsuageEffectiveness)
        self.sdrQuarantineUsuageEffectiveness.set(self.conf.get_qurantine_effectiveness())
        self.sdrQuarantineUsuageEffectiveness.place(x=250+500+self.xadd,y=300)

        self.lblQuarantineUsuageEffectivenessVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblQuarantineUsuageEffectivenessVal.place(x=400+500+self.xadd,y=300)

        self.lblQuarantinePercentage = tk.Label(self, text="Quarantining Percentage")
        self.lblQuarantinePercentage.place(x=70+500+self.xadd,y=350)

        self.sdrQuarantinePercentage = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueQuarantinePercentage)
        self.sdrQuarantinePercentage.set(self.conf.get_qurantine_usage_percentage())
        self.sdrQuarantinePercentage.place(x=250+500+self.xadd,y=350)

        self.lblQuarantinePercentageVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblQuarantinePercentageVal.place(x=400+500+self.xadd,y=350)

#------------------------- vaccine -------------------------
        self.lblVaccineIntroducedTimeline = tk.Label(self, text="Vaccine Timeline")
        self.lblVaccineIntroducedTimeline.place(x=115+500+self.xadd,y=400)

        self.txtVaccineIntroducedTimeline = tk.Text(self, height =1, width = 25)
        self.txtVaccineIntroducedTimeline.insert("end",str(self.conf.get_vaccine_introduced_timeline()))
        self.txtVaccineIntroducedTimeline.place(x=250+500+self.xadd,y=400)

        self.lblVaccineEffectiveness = tk.Label(self, text="Vaccine Effectiveness")
        self.lblVaccineEffectiveness.place(x=85+500+self.xadd,y=450)

        self.sdrVaccineEffectiveness = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueVaccineEffectiveness)
        self.sdrVaccineEffectiveness.set(self.conf.get_vaccine_effectiveness())
        self.sdrVaccineEffectiveness.place(x=250+500+self.xadd,y=450)

        self.lblVaccineEffectivenessVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblVaccineEffectivenessVal.place(x=400+500+self.xadd,y=450)

        self.lblVaccinePercentage = tk.Label(self, text="Vaccine Percentage")
        self.lblVaccinePercentage.place(x=100+500+self.xadd,y=500)

        self.sdrVaccinePercentage = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueVaccinePercentage)
        self.sdrVaccinePercentage.set(self.conf.get_vaccine_usage_percentage())
        self.sdrVaccinePercentage.place(x=250+500+self.xadd,y=500)

        self.lblVaccinePercentageVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblVaccinePercentageVal.place(x=400+500+self.xadd,y=500)

        self.btnSet = ttk.Button(self, text="Set",command = self.setButtonOnClick)
        self.btnSet.place(x=470+self.xadd,y=650)

    def on_change(self,index,value,op):
        self.conf.set_property_name(self.comboBoxVirus.get())
        self.conf.load_from_file(self.comboBoxVirus.get())
        self.set_virus_properties()
    
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

#---------------------- changing config values -----------------

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
            print(conf.get_initial_infected_percentage())
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
        self.lineCanvas2 = None
        self.lgCanvas = None
        self.time =0

 #---------------- lists to plot -------------------

        self.infected_log = list()
        self.total_log = list()
        self.healthy_log = list()
        self.recovered_log = list()
        self.deceased_log = list()
        self.super_log = list()
        self.mask_log = list()
        self.quarantine_log = list()
        self.vaccine_log = list()
        self.time_log = list()

        self.infected_lg_log = list()
        self.recovered_lg_log = list()
        self.deceased_lg_log = list()

        self.xlimit = 100
        self.ylimit = 0
        self.logYlimit = 0

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Simulation", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        self.timer_label = tk.Label(self, text="")
        self.timer_label.place(x=200,y=200)
        self.no_of_infected = tk.Label(self,text="")
        self.no_of_infected.place(x=100,y=250)

        #---------- legend labels ------------

        self.infected_legend = tk.Label(self, text="Total Cases:")
        self.infected_legend.place(x=870-200,y=580-80)

        self.infected_color = tk.Label(self, text="__________",fg='maroon')
        self.infected_color.place(x=960-200,y=575-80)

        self.healthy_legend = tk.Label(self, text="Active Cases:")
        self.healthy_legend.place(x=860-200,y=610-80)

        self.infected_color = tk.Label(self, text="__________",fg='red')
        self.infected_color.place(x=960-200,y=605-80)

        self.recovered_legend = tk.Label(self, text="Super Spreaders:")
        self.recovered_legend.place(x=835-200,y=640-80)

        self.recovered_color = tk.Label(self, text="__________",fg='orange')
        self.recovered_color.place(x=960-200,y=635-80)

        self.dead_legend = tk.Label(self, text="Recovered:")
        self.dead_legend.place(x=875-200,y=670-80)

        self.dead_color = tk.Label(self, text="__________",fg='green')
        self.dead_color.place(x=960-200,y=665-80)

        self.super_legend = tk.Label(self, text="Deceased:")
        self.super_legend.place(x=880-200,y=700-80)

        self.super_color = tk.Label(self, text="__________",fg='black')
        self.super_color.place(x=960-200,y=695-80)

        self.mask_legend = tk.Label(self, text="Healthy:")
        self.mask_legend.place(x=895-200,y=730-80)

        self.mask_color = tk.Label(self, text="__________",fg='blue')
        self.mask_color.place(x=960-200,y=725-80)

        self.quarantine_legend = tk.Label(self, text="Mask Usage:")
        self.quarantine_legend.place(x=865-200,y=760-80)

        self.quarantine_color = tk.Label(self, text="__________",fg='pink')
        self.quarantine_color.place(x=960-200,y=755-80)

        self.vaccine_legend = tk.Label(self, text="Quarantined:")
        self.vaccine_legend.place(x=865-200,y=790-80)

        self.vaccine_color = tk.Label(self, text="__________",fg='cyan')
        self.vaccine_color.place(x=960-200,y=785-80)

        self.vaccine_legend = tk.Label(self, text="Vaccinated:")
        self.vaccine_legend.place(x=870-200,y=820-80)

        self.vaccine_color = tk.Label(self, text="__________",fg='lime')
        self.vaccine_color.place(x=960-200,y=815-80)

        #---------- radio buttons ------------
        self.infected_box=tk.BooleanVar()
        self.infected_box.set(True)
        self.checkInfected = tk.Checkbutton(self,text='Infected', var=self.infected_box,onvalue=1,offvalue=0)
        # self.checkInfected.place(x=950,y=80)

        self.healthy_box=tk.BooleanVar()
        self.healthy_box.set(True)
        self.checkHealthy = tk.Checkbutton(self,text='Healthy', var=self.healthy_box,onvalue=1,offvalue=0)
        # self.checkHealthy.place(x=950,y=110)

        self.recovered_box=tk.BooleanVar()
        self.recovered_box.set(True)
        self.checkRecovered = tk.Checkbutton(self,text='Recovered', var=self.recovered_box,onvalue=1,offvalue=0)
        # self.checkRecovered.place(x=950,y=140)

        self.dead_box=tk.BooleanVar()
        self.dead_box.set(True)
        self.checkDead = tk.Checkbutton(self,text='Dead', var=self.dead_box,onvalue=1,offvalue=0)
        # self.checkDead.place(x=950,y=170)

        self.super_box=tk.BooleanVar()
        self.super_box.set(True)
        self.checkSuper = tk.Checkbutton(self,text='Super Spreader', var=self.super_box,onvalue=1,offvalue=0)
        # self.checkSuper.place(x=950,y=200)

        self.mask_box=tk.BooleanVar()
        self.mask_box.set(True)
        self.checkMask = tk.Checkbutton(self,text='Mask usage', var=self.mask_box,onvalue=1,offvalue=0)
        # self.checkMask.place(x=950,y=230)

        self.quarantine_box=tk.BooleanVar()
        self.quarantine_box.set(True)
        self.checkquarantine = tk.Checkbutton(self,text='Quarantine usage', var=self.quarantine_box,onvalue=1,offvalue=0)
        # self.checkquarantine.place(x=950,y=260)

        self.vaccine_box=tk.BooleanVar()
        self.vaccine_box.set(True)
        self.checkquarantine = tk.Checkbutton(self,text='Quarantine usage', var=self.vaccine_box,onvalue=1,offvalue=0)
        # self.checkquarantine.place(x=950,y=290)

        self.no_of_infected.config(text="Total Cases  :"+""+"\nNew Cases  :" +""+"\nActive Cases  :" +"" +"\nSuper Spreader : " + "" + "\nRecovered  :" +"" + "\nDeceased  :" +"" +"\nHealthy : " + "" + "\nMask Usage  :" +"" + "\nQuarantined  :" +"" +"\nVaccinated : " + "" +"\nPredicted more infection: " + "" )
        self.no_of_infected.place(x=700,y=200)
#---------------- back and simulate buttons ---------------
        btnBack = ttk.Button(self, text = "<< back", command=self.backOnClick)
        btnBack.place(x=20, y=10)

        btnSim = ttk.Button(self, text = "Click to Begin", command=self.startSim)
        btnSim.place(x=720, y=400)

        lblLegend_title = tk.Label(self, text ="Legend",font =MED_FONT)
        lblLegend_title.place(x=720,y=450)

#---------------- Simulation window  ----------------------

        #self.img = tk.PhotoImage(file =cwd+"/ui/img.png")
        self.canvass = tk.Canvas(self,height=350, width = 600, background ='white')
        self.canvass.place(x=50,y=70)

        # bg_img = tk.Label(self,image=self.img)
        # bg_img.place(x=50,y=70)
        # self.img = img = tk.PhotoImage(file =cwd+"/ui/img.png")
        # self.canvass.create_image(100,100,image =self.img, anchor ="nw")

#----------- time series graph ---------------------
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Time series graph')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('# People')
        self.ax.set_xlim(0,self.xlimit)
        self.ax.set_ylim(0,self.ylimit)
        self.lines_healthy=self.ax.plot([],[],'b')[0]
        self.lines_total = self.ax.plot([],[],'maroon')[0]
        self.lines_mask = self.ax.plot([],[],'pink')[0]
        self.lines_quarantine = self.ax.plot([],[],'cyan')[0]
        self.lines_vaccine = self.ax.plot([],[],'lime')[0]
        self.lines_recovered = self.ax.plot([],[],'g')[0]

        self.lineCanvas = po.FigureCanvasTkAgg(self.fig, master = self)
        self.lineCanvas.get_tk_widget().place(x=70,y=500-30, width = 500,height = 400-80)

#----------- 2nd graph --------------------
        self.fig2 = Figure()
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_title('Time series graph')
        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('# People')
        self.ax2.set_xlim(0,self.xlimit)
        self.ax2.set_ylim(0,50)

        self.lines_infected = self.ax2.plot([],[],'r')[0]
        self.lines_super = self.ax2.plot([],[],'orange')[0]
        self.lines_dead = self.ax2.plot([],[],'black')[0]

        self.lineCanvas2 = po.FigureCanvasTkAgg(self.fig2, master = self)
        self.lineCanvas2.get_tk_widget().place(x=900,y=500-30, width = 500,height = 400-80)

#------------- log graph ---------------------
        self.fig_lg = Figure()
        self.ax_lg = self.fig_lg.add_subplot(111)
        self.ax_lg.set_title('Logarithmic graph')
        self.ax_lg.set_xlabel('Time')
        self.ax_lg.set_ylabel('Rate of Infection')
        self.lines_infected_lg = self.ax_lg.plot([],[],'r')[0]
        self.lines_recovered_lg = self.ax_lg.plot([],[],'g')[0]
        self.lines_dead_lg = self.ax_lg.plot([],[],'black')[0]

        self.lgCanvas = po.FigureCanvasTkAgg(self.fig_lg, master = self)
        self.lgCanvas.get_tk_widget().place(x=900,y=70, width = 500,height = 350)
        self.lgCanvas.draw()


        self.canvass.delete('all')

 #---------------  back button ------------------

    def backOnClick(self):
        
        self.fig.clear(True)
        self.ax_lg.clear()
        self.cancel_oval()
        self.canvass.delete('all')
        
        if self.time>0:
            self.time=0
            self.time_log=list()

        self.no_of_infected.config(text="Total Cases  :"+""+"\nNew Cases  :" +""+"\nActive Cases  :" +"" +"\nSuper Spreader : " + "" + "\nRecovered  :" +"" + "\nDeceased  :" +"" +"\nHealthy : " + "" + "\nMask Usage  :" +"" + "\nQuarantined  :" +"" +"\nVaccinated : " + "" +"\nPredicted more infection: " + "" )
        self.no_of_infected.place(x=700,y=200)

# -------------- time series graph-------------
        
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
       
        self.ax.set_title('Time series graph')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('No of people')
        self.ax.set_xlim(0,self.xlimit)
        self.ax.set_ylim(0,self.ylimit)
        
        self.lines_healthy=self.ax.plot([],[],'b')[0] 
        self.lines_total = self.ax.plot([],[],'maroon')[0]
        self.lines_mask = self.ax.plot([],[],'pink')[0]
        self.lines_quarantine = self.ax.plot([],[],'cyan')[0]
        self.lines_vaccine = self.ax.plot([],[],'lime')[0]
        self.lines_recovered = self.ax.plot([],[],'g')[0]

        self.lineCanvas = po.FigureCanvasTkAgg(self.fig, master = self)
        self.lineCanvas.get_tk_widget().place(x=70,y=500-30, width = 500,height = 400-80)

#----------- 2nd graph --------------------
        self.fig2 = Figure()
        self.ax2 = self.fig2.add_subplot(111)
       
        self.ax2.set_title('Time series graph')
        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('# People')
        self.ax2.set_xlim(0,self.xlimit)
        self.ax2.set_ylim(0,self.logYlimit)

        self.lines_infected = self.ax2.plot([],[],'r')[0]
        self.lines_super = self.ax2.plot([],[],'orange')[0]
        self.lines_dead = self.ax2.plot([],[],'black')[0]

        self.lineCanvas2 = po.FigureCanvasTkAgg(self.fig2, master = self)
        self.lineCanvas2.get_tk_widget().place(x=900,y=500-30, width = 500,height = 400-80)

#------------- log graph ---------------------
        self.fig_lg = Figure()
        self.ax_lg = self.fig_lg.add_subplot(111)
        self.ax_lg.set_title('Logarithmic graph')
        self.ax_lg.set_xlabel('Time')
        self.ax_lg.set_ylabel('Growth Rate')
        
       
        self.lines_infected_lg = self.ax_lg.plot([],[],'r')[0]
        self.lines_recovered_lg = self.ax_lg.plot([],[],'g')[0]
        self.lines_dead_lg = self.ax_lg.plot([],[],'black')[0]

        self.lgCanvas = po.FigureCanvasTkAgg(self.fig_lg, master = self)
        self.lgCanvas.get_tk_widget().place(x=900,y=70, width = 500,height = 350)
        self.lgCanvas.draw()
        self.cont.show_frame(DefaultPanel)

    def startSim(self):

        self.canvass.delete('all')
        self.cancel_line()
        self.cancel_oval()
        self.cancel_lg()
        self.lineCanvas= None
        self.lineCanvas2=None
        self.lgCanvas=None

        self.pre_cou=None

        self.cu = Config.get_instance()
        
        self.sd = SimalationData()
        self.du = DataUtil()
        self.dataset = self.sd.getDataset()
        self.pu = PersonUtil()
        self.time = 0
        self.infected_location_dict = dict()
        self.ylimit = self.cu.get_population()
        self.logYlimit = self.cu.get_population()/2

        self.canvass = tk.Canvas(self,height=350, width = 600,background='white')
        self.canvass.place(x=50,y=70)
        #self.img = img = tk.PhotoImage(file =cwd+"/ui/img.png")
        #self.canvass.create_image(100,100,image =self.img, anchor ="nw")


        #--------- time series graph ------------
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
       
        self.ax.set_title('Time series graph')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('No of people')
        self.ax.set_xlim(0,self.xlimit)
        self.ax.set_ylim(0,self.ylimit)
        
       
        
        self.lines_healthy=self.ax.plot([],[],'b')[0] 
        self.lines_total = self.ax.plot([],[],'maroon')[0]
        self.lines_mask = self.ax.plot([],[],'pink')[0]
        self.lines_quarantine = self.ax.plot([],[],'cyan')[0]
        self.lines_vaccine = self.ax.plot([],[],'lime')[0]
        self.lines_recovered = self.ax.plot([],[],'g')[0]

        self.lineCanvas = po.FigureCanvasTkAgg(self.fig, master = self)
        self.lineCanvas.get_tk_widget().place(x=70,y=500-30, width = 500,height = 400-80)

    #----------- 2nd graph --------------------
        self.fig2 = Figure()
        self.ax2 = self.fig2.add_subplot(111)
       
        self.ax2.set_title('Time series graph')
        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('No of people')
        self.ax2.set_xlim(0,self.xlimit)
        self.ax2.set_ylim(0,self.logYlimit)

        self.lines_infected = self.ax2.plot([],[],'r')[0]
        self.lines_super = self.ax2.plot([],[],'orange')[0]
        self.lines_dead = self.ax2.plot([],[],'black')[0]

        self.lineCanvas2 = po.FigureCanvasTkAgg(self.fig2, master = self)
        self.lineCanvas2.get_tk_widget().place(x=900,y=500-30, width = 500,height = 400-80)

    #------------- log graph ---------------------
        
        self.fig_lg = Figure()
        self.ax_lg = self.fig_lg.add_subplot(111)
        self.ax_lg.set_title('Logarithmic graph')
        self.ax_lg.set_xlabel('Time')
        self.ax_lg.set_ylabel('Growth Rate Log Graph')
        self.ax_lg.set_xlim(0,self.xlimit)
        self.ax_lg.set_ylim(0,np.log2(self.ylimit*4))
       
        self.lines_infected_lg = self.ax_lg.plot([],[],'r')[0]
        self.lines_recovered_lg = self.ax_lg.plot([],[],'g')[0]
        self.lines_dead_lg = self.ax_lg.plot([],[],'black')[0]

        self.lgCanvas = po.FigureCanvasTkAgg(self.fig_lg, master = self)
        self.lgCanvas.get_tk_widget().place(x=900,y=70, width = 500,height = 350)


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
        if self.lineCanvas2 is not None:
            self.lineCanvas2.close_event()
        self.ax.plot([],[])
        self.infected_log = list()
        self.total_log = list()
        self.healthy_log = list()
        self.recovered_log = list()
        self.deceased_log = list()
        self.super_log = list()
        self.mask_log = list()
        self.quarantine_log = list()
        self.vaccine_log = list()
        self.time_log = list()

        self.infected_lg_log = list()
        self.recovered_lg_log = list()
        self.deceased_lg_log = list()
    
    def cancel_lg(self):
        if self.lgCanvas is not None:
            self.lgCanvas.close_event()

    def move_oval(self):
        # self.ax.get_legend().remove()
        self.new_infect = 0
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
                            self.new_infect+=1
                            got_infected_from = self.infected_location_dict[(x,y)]
                            self.dataset[got_infected_from].set_can_infect(self.dataset[got_infected_from].get_can_infect()-1)
                    else:
                         self.dataset[i] = self.pu.updatePerson(False,self.dataset[i],self.time)[0]
                else:
                    self.dataset[i] = self.pu.updatePerson(False, self.dataset[i],self.time)[0]

        counts  = self.du.getTotalCountAll(self.dataset)
        
        self.timer_label.config(text="Days : " + str(int(self.time)))
        self.timer_label.place(x=750,y=180)
        Total_cases = counts["Infected"] + counts["Recover"] + counts["Dead"]
        self.no_of_infected.config(text="Total Cases  :"+str(Total_cases)+"\nNew Cases  :" +str(self.new_infect)+"\nActive Cases  :" +str(counts["Infected"]) +"\nSuper Spreader : " + str(counts["Super"]) + "\nRecovered  :" +str(counts["Recover"]) + "\nDeceased  :" +str(counts["Dead"]) +"\nHealthy : " + str(counts["Healthy"]) + "\nMask Usage  :" +str(counts["Mask"]) + "\nQuarantined  :" +str(counts["Quarantine"]) +"\nVaccinated : " + str(counts["Vaccinate"]) +"\nPredicted more infection: " + str(int(self.cu.get_total_to_infect())) )
        self.no_of_infected.place(x=700,y=200)
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
            
            if c=='orange':
                self.canvass.create_oval(self.dataset[i].get_x()*(3/5)-5,self.dataset[i].get_y()*(350/1000)-5,self.dataset[i].get_x()*(3/5)+5,self.dataset[i].get_y()*(350/1000)+5, fill = c)
            else:
                self.canvass.create_oval(self.dataset[i].get_x()*(3/5)-2.5,self.dataset[i].get_y()*(350/1000)-2.5,self.dataset[i].get_x()*(3/5)+2.5,self.dataset[i].get_y()*(350/1000)+2.5, fill = c)
        
        if self.time == self.xlimit:
            self.xlimit *=2
            self.ax_lg.set_xlim(0, self.xlimit)
            self.ax.set_xlim(0,self.xlimit)
            self.ax2.set_xlim(0,self.xlimit)
        
        if counts["Infected"] > self.logYlimit:
            self.logYlimit= counts["Infected"]+100
            self.ax2.set_ylim(0,self.logYlimit)

        if counts["Super"] > self.logYlimit:
            self.logYlimit= counts["Super"]+100
            self.ax2.set_ylim(0,self.logYlimit)

        if counts["Dead"] > self.logYlimit:
            self.logYlimit= counts["Dead"]+100
            self.ax2.set_ylim(0,self.logYlimit)            
        
        self.infected_log.append(counts["Infected"])
        self.healthy_log.append(counts["Healthy"])
        self.recovered_log.append(counts["Recover"])
        self.deceased_log.append(counts["Dead"])
        self.super_log.append(counts["Super"])
        self.mask_log.append(counts["Mask"])
        self.quarantine_log.append(counts["Quarantine"])
        self.vaccine_log.append(counts["Vaccinate"])
        self.total_log.append(counts["Infected"] + counts["Recover"] + counts["Dead"])
        if counts["Infected"]!=0:
            self.infected_lg_log.append(np.log2(counts["Infected"]))
        else:
            self.infected_lg_log.append(0)
        if counts["Recover"]!=0:
            self.recovered_lg_log.append(np.log2(counts["Recover"]))
        else:
            self.recovered_lg_log.append(0)
        if counts["Dead"]!=0:
            self.deceased_lg_log.append(np.log2(counts["Dead"]))
        else:
            self.deceased_lg_log.append(0)
        
        self.time_log.append(self.time)

        if self.infected_box.get() ==1:
            self.lines_infected.set_xdata(self.time_log)
            self.lines_infected.set_ydata(self.infected_log)
        if self.healthy_box.get() ==1:
            self.lines_healthy.set_xdata(self.time_log)
            self.lines_healthy.set_ydata(self.healthy_log)
        if self.recovered_box.get() ==1:
            self.lines_recovered.set_xdata(self.time_log)
            self.lines_recovered.set_ydata(self.recovered_log)
        if self.dead_box.get() ==1:
            self.lines_dead.set_xdata(self.time_log)
            self.lines_dead.set_ydata(self.deceased_log)
        if self.super_box.get() ==1:
            self.lines_super.set_xdata(self.time_log)
            self.lines_super.set_ydata(self.super_log)
        if self.mask_box.get() ==1:
            self.lines_mask.set_xdata(self.time_log)
            self.lines_mask.set_ydata(self.mask_log)
        if self.quarantine_box.get() ==1:
            self.lines_quarantine.set_xdata(self.time_log)
            self.lines_quarantine.set_ydata(self.quarantine_log)
        if self.vaccine_box.get() ==1:
            self.lines_vaccine.set_xdata(self.time_log)
            self.lines_vaccine.set_ydata(self.vaccine_log)
        self.lines_total.set_xdata(self.time_log)
        self.lines_total.set_ydata(self.total_log)

        self.lines_infected_lg.set_xdata(self.time_log)
        self.lines_infected_lg.set_ydata(self.infected_lg_log)

        self.lines_recovered_lg.set_xdata(self.time_log)
        self.lines_recovered_lg.set_ydata(self.recovered_lg_log)

        self.lines_dead_lg.set_xdata(self.time_log)
        self.lines_dead_lg.set_ydata(self.deceased_lg_log)
        
        
        self.lineCanvas.draw()
        self.lineCanvas2.draw()
        #Comment or uncomment for output in print terminal
        if(self.time==30):
            print(self.time,Total_cases)
        elif(self.time==50):
            print(self.time,Total_cases)
        elif(self.time==100):
            print(self.time,Total_cases)
        elif(self.time==150):
            print(self.time,Total_cases)
        elif(self.time==200):
            print(self.time,Total_cases)
        elif(self.time==250):
            print(self.time,Total_cases)
        elif(self.time==300):
            print(self.time,Total_cases)
        
        
        self.lgCanvas.draw()
        self.dots_graph=self.canvass.after(100,self.move_oval)
        

    

window = DefaultFrame()
window.geometry('1450x1200')
window.resizable(True,True)
window.mainloop()
