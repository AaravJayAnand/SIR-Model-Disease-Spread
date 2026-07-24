import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from constants import *

class Simulation:
    def __init__(self):
        self.individuals = np.zeros(POPULATION) # State 0: Susceptible
        self.individuals[0:INITIAL_INFECTED] = 1 # State 1: Infected, set INITIAL_INFECTED people to state 1
        self.recovered = 0 # State 2: Recovered, 0 are recovered initially
        self.tick = 0 # Day of Simulation
        self.data = {"day": [], "S": [], "I": [], "R": [], "probSI": []} # DATA

    def update(self):
        # For all the people that are susceptible: (self.individuals == 0)
        # Apply a CONTACT_RATE * SI_RATE * [percent of population that is infected] chance of getting infected
        SI_mask = (self.individuals == 0) & (np.random.random(POPULATION) < CONTACT_RATE * SI_RATE * np.sum(self.individuals == 1) / POPULATION)

        # For all the people that are infected: (self.individuals == 1)
        # Apply an IR_RATE chance of recovering
        IR_mask = (self.individuals == 1) & (np.random.random(POPULATION) < IR_RATE)

        # Individuals that need to be updated will be updated
        self.individuals[SI_mask] = 1
        self.individuals[IR_mask] = 2

        # Store the data as a 'table'
        self.recovered = int(np.sum(self.individuals == 2)) # self.individuals == 2 (recovered) returns an array of 1s and 0s (1 is recovered, 2 is not) and summing that gives number of people that are immune at any given moment
        self.data["day"].append(self.tick) # add the day to the data
        self.data["S"].append(int(np.sum(self.individuals == 0))) # similar logic to self.recovered, store data
        self.data["I"].append(int(np.sum(self.individuals == 1))) # similar logic to self.recovered, store data
        self.data["R"].append(self.recovered) # store recovered data
        self.data["probSI"].append(CONTACT_RATE * SI_RATE * np.sum(self.individuals == 1) * POPULATION / 10000) # idk if this is accurate, somewhat of a representation of infection probability at each tick
        self.tick += 1

simulation = Simulation()
simulation.update()
while simulation.data["I"][-1] > 0:
    simulation.update()
data = simulation.data


### GRAPH ###
plt.style.use("dark_background")
plt.plot(data["day"], data["S"], color=(1, 1, 0), label="Susceptible", lw=2)
plt.plot(data["day"], data["I"], color=(1, 0, 0), label="Infected", lw=2)
plt.plot(data["day"], data["R"], color=(0, 1, 0), label="Recovered", lw=2)
plt.plot(data["day"], data["probSI"], color=(0, 0, 1), label="Transmission Probability (normalized)", lw=2, linestyle="dashed")
plt.legend()
plt.title(f"SIR model of COVID-19 given a population of {POPULATION} with {INITIAL_INFECTED} initially infected")
plt.xlabel(f"Days ({data['day'][-1]})")
plt.ylabel(f"Number of Individuals (S: {data["S"][-1]}, R: {data["R"][-1]})")
# plt.xticks([])
# plt.yticks([])

# print data as a dataframe (table), can be used to store dataframes in files for future reference, etc.

df = pd.DataFrame(data)
print(df.tail(100))

### DISPLAY GRAPH ###

plt.show()