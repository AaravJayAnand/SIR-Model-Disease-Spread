import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

PUBLIC_CONTACT_RATE = 0.4
SI_RATE = 0.5
IR_RATE = 0.071
POPULATION = 20000000
INITIAL_INFECTED = 2000

class Simulation:
    def __init__(self):
        self.individuals = np.zeros(POPULATION)
        self.individuals[0:INITIAL_INFECTED] = 1
        self.recovered = 0
        self.tick = 0
        self.data = {"day": [], "S": [], "I": [], "R": []}

    def update(self):
        SI_mask = (self.individuals == 0) & (np.random.random(POPULATION) < PUBLIC_CONTACT_RATE * SI_RATE * np.sum(self.individuals == 1) / POPULATION)
        IR_mask = (self.individuals == 1) & (np.random.random(POPULATION) < IR_RATE)
        
        self.individuals[SI_mask] = 1
        self.individuals[IR_mask] = 2
        
        self.recovered = int(np.sum(self.individuals == 2))
        self.data["day"].append(self.tick)
        self.data["S"].append(int(np.sum(self.individuals == 0)))
        self.data["I"].append(int(np.sum(self.individuals == 1)))
        self.data["R"].append(self.recovered)
        self.tick += 1

simulation = Simulation()
simulation.update()
while simulation.data["I"][-1] > 0:
    simulation.update()
data = simulation.data

plt.style.use("dark_background")
plt.plot(data["day"], data["S"], color=(1, 1, 0), label="Susceptible", lw=2)
plt.plot(data["day"], data["I"], color=(1, 0, 0), label="Infected", lw=2)
plt.plot(data["day"], data["R"], color=(0, 1, 0), label="Recovered", lw=2)
plt.legend()
plt.title(f"SIR model of COVID-19 given a population of {POPULATION} with {INITIAL_INFECTED} initially infected")
plt.xlabel(f"Days ({data['day']})")
plt.ylabel(f"Number of Individuals (S: {data["S"]}, I: {data["I"]}, R: {data["R"]})")

df = pd.DataFrame(data)
print(df.tail(100))

plt.show(block=True)