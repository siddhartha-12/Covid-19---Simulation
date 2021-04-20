COVID-19 Simulation
Prepared for: 
PSA Final Project – INFO 6205 Spring 2021

 
Prepared by:
Siddhartha Raju (001084614)
Gautham Rajsimha Pulipati (001572432)
Naveen Kumar Buddhala (001582394)
 
Table of Contents
Introduction	3
Aim	3
Project Details	4
File Structure:	4
1.	Config.cfg	4
2.	Config.py	4
3.	ConfigUtil.py	4
4.	Person.py	4
5.	PersonUtil.py	5
6.	DataUtil.py	5
7.	SimulationData.py	5
8.	Main.py	5
9.	MainFrame.py	5
Factors:	5
1.	K factor	5
2.	Mask	5
3.	Quarantine	6
4.	Vaccine	6
5.	Days contagious	6
6.	Initial infected percentage	6
Implementation	6
R factor	6
Output	9
Analysis	10
Conclusion	10
Unit Testing	11
1)	Test_Config.py	11
2)	Test_ConfigUtil.py	11
3)	Test_DataUtil.py	12
4)	Test_person.py	12
5)	Test_PersonUtil.py	13
6)	Test_SimulationData.py	13



 
INTRODUCTION

Simulation model of a disease projects how infectious diseases progress i.e how its components like transmission, spread and control of any infection grows over time and how it may strongly or weakly effect the dynamics of an epidemic. It also helps to inform public health interventions. 
Simulation model gives a pictoral or graphical way and it involves many factors, actors and components.
This is a new method of understanding and teaching about any disease outbreaks.  
This can save money,lives and time by allowing us to test it without even applying it to real world.
Our simulation model fits for a particular pattern which is a general method involving R and K factor of the disease and several other factors of its spread.

AIM

Simulate the spread of a virus with respect to several factors and introducing various control measures later during the simulation and finally analysing the virus.   
Simulations will take into account:
•	The R factor and k factor of the disease 
•	The usage and effectiveness of masks
•	The prevalence of testing and contact tracing
•	The availability and efficacy of the vaccine
•	Any barriers to entry (including quarantining) into the subject area.
Building a User Interface to set several configuration values involved for respective diseases and simulating over a population and finally analysing through various graphs.
 
PROJECT DETAILS

This disease simulation model is implemented in Python using TkInter and numpy library for probability association and matplotlib library for plotting the graph. The project consists of the following things

File Structure: 
1.	Config.cfg
a.	The configuration file for the project can be found at the following location ~/config/config.cfg. The config file is used to set the default values for various diseases.
b.	In case no values are provided through the interface, the application will self-feed the values from this configuration file.
2.	Config.py
a.	This is a Singleton class, and it contains all the configuration values required to simulate the disease
b.	It has the following properties:
c.	property-name
d.	population
e.	initial-infected
f.	r-factor
g.	k-factor
h.	days-contagious
i.	mask introduction timelines
j.	mask effectiveness
k.	mask usage percentage
l.	quarantine introduction timelines
m.	quarantine effectiveness
n.	quarantine usage percentage
o.	vaccine introduction timelines
p.	vaccine effectiveness
q.	vaccine usage percentage

3.	ConfigUtil.py
a.	This is a Singleton class, and it contains the methods to load config file and get config values based on section and key passed.

4.	Person.py
This Class contains all the person related information. 
a.	It contains the following properties along with all their respective getters and setters:
b.	id
c.	age
d.	gender
e.	x-coordinate
f.	y-coordinate
g.	vaccinated
h.	quarantined
i.	mask-usage
j.	infected
k.	recovered
l.	deceased
m.	recovery-days
n.	can-infect-others
5.	PersonUtil.py
a.	The class contains method to perform update operations of the Person object like updating location and status quo about mask, quarantine and infection. The class is used for updating various parameters of a person object during simulation. 

6.	DataUtil.py
a.	The class contains methods to perform data related operations like counting infected people, recovered people.

7.	SimulationData.py
a.	This class is used to setup the initial environment for simulation. It generates the initial dataset which is consumed during simulation for further processing.

8.	Main.py
a.	This is the main class which is executed at the program execution

9.	MainFrame.py
a.	This class consumes the data provided from Simulation Data and use it to visualize UI which contains Tkinter screens and graph for the user interface.

Factors:
The following factors have been considered while designing the disease simulation
1.	K factor
a.	The dispersion parameter, it tells exactly how many are infected by each person i.e. in case of COVID-19 10-15 % of the population is responsible for 80% of the infections.
b.	These people are called super-spreaders. Whereas others, may be quarantined and infect none.

2.	Mask 
a.	3 factors for mask are considered: introduction timeline, effectiveness, and percentage usage 
b.	Introduction timeline specifies number of days after which the masks were introduced i.e. after certain time of start of simulation
c.	Effectiveness specifies how much does mask help us to protect from getting infected on a scale of 100, 0 signifies mask has no impact on in the virus to be infected
d.	Percentage Usage specifies how many from the current population are using the masks

3.	Quarantine 
a.	3 factors for quarantine are considered: introduction timeline, effectiveness, and percentage usage 
b.	Introduction timeline specifies number of days after which the people started to get quarantined i.e. after certain time of start of simulation
c.	Effectiveness specifies how much does quarantine help us to protect from getting infected on a scale of 100, 100 signifies if a person is quarantined, he cannot get infected
d.	Percentage Usage specifies how many from the current population are quarantining after getting infected

4.	Vaccine 
a.	3 factors for vaccine are considered: introduction timeline, effectiveness, and percentage usage 
b.	Introduction timeline specifies number of days after which the people started to get vaccinated i.e. after certain time of start of simulation
c.	Effectiveness specifies how much does vaccination help us to protect from getting infected on a scale of 100, 100 signifies if a person is vaccinated, he cannot get infected
d.	Percentage Usage specifies how many from the current population are vaccinated

5.	Days contagious
a.	No. of days the person is infected, after catching the infection

6.	Initial infected percentage
a.	Percentage of total population to be infected at the beginning of simulation

IMPLEMENTATION

Factors considered: 
R factor
The average number of infections by one infected person.

GUI
There is a main panel which has 2 buttons: Set configuration and Start Simulation
These 2 buttons when clicked opens 2 other panels, one has all the default set configuration details which can be reset as per the user, while the other starts the simulation process, shows the space where the population is and how the infections take place. The panel also shows the graphs to understand how the virus is being spread as per the factors set. 



For every cycle-time, for the complete dataset of persons, the below function is being called which is the main algorithm.
 
This function does the complete work of updating a person for the current cycle-time.
Its computational order:

If the person is alive 
	If the person is in close contact of any other infected person 
		If yes : checking their infection status whether the person will get infected
			If yes: infecting and updating how many others the person can infect (K factor)
			           Setting randomly for how many days the person will remain infected
	If the person is not quarantined
		Updating the person’s movement
	If the person is infected and not yet recovered: Updating the person’s recovery day’s left
		If recovery days are completed: checking if the person will come under the probability of dead
	If mask has been introduced: checking if the person will wear it
	If quarantine has been introduced: checking if the person will quarantine
	If vaccine has been introduced: checking if the person has taken the vaccination

Below are the various functions where we compute all the above-mentioned operations.
Every value required is taken from the config, set by the user, and randomizing the values in its surroundings.
For movement: we are randomly moving the person in the space in between -5 to 5 for both the coordinates
For checking if the person dies of covid, we considered the health scale, how immune the person is at the time of infection, together with the fatality rate of the virus specified in the config.

 

For getting the infection status, we consider all the factors responsible, such as checking if the person has good immunity levels and is healthy, the mask factor, quarantine factor, vaccination factor, all the three separately as well as combination of them.
For checking if the person will spread, we considered the K-factor, the main factor that is responsible for the COVID-19 infection rate, i.e. the super spreaders, which is about 0.1, which says 10% of the infected people are responsible for the overall 90% of the infections.
 

OUTPUT
 
1- Entry Screen

 
2 - Configuration Screen
 
3- Simulation Screen


ANALYSIS

Performance:
Time Complexity : The alogorithm worst case complexity is O(N*T) where N is the number of people and T is the time the simulation is run. 
Space Complexity : The algorithm complexity is O(N+T) where N is the number people to simulate and T is time the simulation is run. Additional T value is needed to store the state of N at time T for plotting graphs
Simulation:






CONCLUSION 



 
UNIT TESTING
1)	Test_Config.py

 
2)	Test_ConfigUtil.py

 
3)	Test_DataUtil.py

 

4)	Test_person.py

 



5)	Test_PersonUtil.py

 

6)	Test_SimulationData.py

 

REREFENCES
1) https://www.doh.wa.gov/Portals/1/Documents/1600/coronavirus/WearAClothFaceCovering.pdf
2) https://royalsociety.org/-/media/policy/projects/set-c/set-covid-19-R-estimates.pdf
3) https://www.healthline.com/health/r-nought-reproduction-number#covid-19-r-0
4) https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2851497/
5) https://www.cdc.gov/sars/clinical/respirators.html
6) https://jbiomedsci.biomedcentral.com/articles/10.1186/s12929-020-00695-2
7) https://sph.umich.edu/pursuit/2020posts/how-scientists-quantify-outbreaks.html
