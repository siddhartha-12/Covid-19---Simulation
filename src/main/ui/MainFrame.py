import matplotlib
matplotlib.use("TkAgg")
import matplotlib.backends.backend_tkagg as po
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import ttk

LARGE_FONT= ("Verdana", 25)
style.use("ggplot")


class DefaultFrame(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Covid 19 simulation")

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

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
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Configuration", font=LARGE_FONT)
        self.label.pack(pady=10,padx=10)
        
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
        self.txtPopulation.insert("end","1000")
        self.txtPopulation.place(x=300,y=250)

        self.lblInitialInfectedPer = tk.Label(self, text="Initial Infected Percentage")
        self.lblInitialInfectedPer.place(x=105,y=300)

        self.txtInitialInfectedPer = tk.Text(self, height =1, width = 25)
        self.txtInitialInfectedPer.insert("end","10")
        self.txtInitialInfectedPer.place(x=300,y=300)

        self.lblRFactor = tk.Label(self, text="R factor")
        self.lblRFactor.place(x=215,y=350)

        self.sdrRFactor = tk.Scale(self, from_=0, to=10, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=1,command=self.set_valueRFactor)
        self.sdrRFactor.set(5)
        self.sdrRFactor.place(x=300,y=350)

        self.lblRFactorVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =3)
        self.lblRFactorVal.place(x=450,y=350)

        self.lblKFactor = tk.Label(self, text="K factor")
        self.lblKFactor.place(x=215,y=400)

        self.sdrKFactor = tk.Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.01,command=self.set_valueKFactor)
        self.sdrKFactor.set(0.2)
        self.sdrKFactor.place(x=300,y=400)

        self.lblKFactorVal = tk.Label(self,text=self.sdrKFactor.get(), height =1, width =3)
        self.lblKFactorVal.place(x=450,y=400)

        self.lblDaysContagious = tk.Label(self, text="Days Contagious")
        self.lblDaysContagious.place(x=160,y=450)

        self.txtDaysContagious = tk.Text(self, height =1, width = 25)
        self.txtDaysContagious.insert("end","14")
        self.txtDaysContagious.place(x=300,y=450)

        #mask

        self.lblMaskIntroducedTimeline = tk.Label(self, text="Mask Timeline")
        self.lblMaskIntroducedTimeline.place(x=180,y=500)

        self.txtMaskIntroducedTimeline = tk.Text(self, height =1, width = 25)
        self.txtMaskIntroducedTimeline.insert("end","20")
        self.txtMaskIntroducedTimeline.place(x=300,y=500)

        self.lblMaskUsuageEffectiveness = tk.Label(self, text="Mask Usuage Effectiveness")
        self.lblMaskUsuageEffectiveness.place(x=95,y=550)

        self.sdrMaskUsuageEffectiveness = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueMaskUsuageEffectiveness)
        self.sdrMaskUsuageEffectiveness.set(80)
        self.sdrMaskUsuageEffectiveness.place(x=300,y=550)

        self.lblMaskUsuageEffectivenessVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblMaskUsuageEffectivenessVal.place(x=450,y=550)

        self.lblMaskUsuagePercentage = tk.Label(self, text="Mask Usage Percentage")
        self.lblMaskUsuagePercentage.place(x=115,y=600)

        self.sdrMaskUsuagePercentage = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueMaskUsuagePercentage)
        self.sdrMaskUsuagePercentage.set(60)
        self.sdrMaskUsuagePercentage.place(x=300,y=600)

        self.lblMaskUsuagePercentageVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblMaskUsuagePercentageVal.place(x=450,y=600)

        #quarantine

        self.lblQuarantineIntroducedTimeline = tk.Label(self, text = "Quarantine Timeline")
        self.lblQuarantineIntroducedTimeline.place(x=100+500,y=250)

        self.txtQuarantineIntroducedTimeline = tk.Text(self, height =1, width = 25)
        self.txtQuarantineIntroducedTimeline.insert("end","30")
        self.txtQuarantineIntroducedTimeline.place(x=250+500,y=250)

        self.lblQuarantineEffectiveness = tk.Label(self, text="Quarantine Effectiveness")
        self.lblQuarantineEffectiveness.place(x=70+500,y=300)

        self.sdrQuarantineUsuageEffectiveness = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueQuarantineUsuageEffectiveness)
        self.sdrQuarantineUsuageEffectiveness.set(90)
        self.sdrQuarantineUsuageEffectiveness.place(x=250+500,y=300)

        self.lblQuarantineUsuageEffectivenessVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblQuarantineUsuageEffectivenessVal.place(x=400+500,y=300)

        self.lblQuarantinePercentage = tk.Label(self, text="Quarantining Percentage")
        self.lblQuarantinePercentage.place(x=70+500,y=350)

        self.sdrQuarantinePercentage = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueQuarantinePercentage)
        self.sdrQuarantinePercentage.set(40)
        self.sdrQuarantinePercentage.place(x=250+500,y=350)

        self.lblQuarantinePercentageVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblQuarantinePercentageVal.place(x=400+500,y=350)

        #vaccine

        self.lblVaccineIntroducedTimeline = tk.Label(self, text="Vaccine Timeline")
        self.lblVaccineIntroducedTimeline.place(x=115+500,y=400)

        self.txtVaccineIntroducedTimeline = tk.Text(self, height =1, width = 25)
        self.txtVaccineIntroducedTimeline.insert("end","50")
        self.txtVaccineIntroducedTimeline.place(x=250+500,y=400)

        self.lblVaccineEffectiveness = tk.Label(self, text="Vaccine Effectiveness")
        self.lblVaccineEffectiveness.place(x=85+500,y=450)

        self.sdrVaccineEffectiveness = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueVaccineEffectiveness)
        self.sdrVaccineEffectiveness.set(99.9)
        self.sdrVaccineEffectiveness.place(x=250+500,y=450)

        self.lblVaccineEffectivenessVal = tk.Label(self,text=self.sdrRFactor.get(), height =1, width =4)
        self.lblVaccineEffectivenessVal.place(x=400+500,y=450)

        self.lblVaccinePercentage = tk.Label(self, text="Vaccine Percentage")
        self.lblVaccinePercentage.place(x=100+500,y=500)

        self.sdrVaccinePercentage = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=130, showvalue=0, resolution=0.1,command=self.set_valueVaccinePercentage)
        self.sdrVaccinePercentage.set(10)
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
        errorMessage =""
        flag =0

        try:
            population = int(self.txtPopulation.get(1.0,"end-1c"))
            print(population)
        except:
            flag=1
            errorMessage+="Population\n"

        try:
            daysContagious = int(self.txtDaysContagious.get(1.0,"end-1c"))
            print(daysContagious)
        except:
            flag=1
            errorMessage+="No of days contagious\n"

        try:
            initialInfectedPer = int(self.txtInitialInfectedPer.get(1.0,"end-1c"))
            print(initialInfectedPer)
        except:
            flag=1
            errorMessage+="Initial infected percentage\n"

        try:
            maskIntroducedTimeline = int(self.txtMaskIntroducedTimeline.get(1.0,"end-1c"))
            print(maskIntroducedTimeline)
        except:
            flag=1
            errorMessage+="Mask introduced timeline\n"

        try:
            quarantineIntroducedTimeline = int(self.txtQuarantineIntroducedTimeline.get(1.0,"end-1c"))
            print(quarantineIntroducedTimeline)
        except:
            flag=1
            errorMessage+="Quarantine introduced timeline\n"

        try:
            vaccineIntroducedTimeline = int(self.txtVaccineIntroducedTimeline.get(1.0,"end-1c"))
            print(vaccineIntroducedTimeline)
        except:
            flag=1
            errorMessage+="Vaccine Introduced Timeline\n"
        if flag==1:
            tk.messagebox.showinfo("Error",errorMessage+" should be numbers")
        

        



class StartPanel(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Simulation", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        btnBack = ttk.Button(self, text = "<< back", command=lambda: controller.show_frame(DefaultPanel))
        btnBack.place(x=20, y=80)






window = DefaultFrame()
window.geometry('1000x1000')
window.mainloop()
