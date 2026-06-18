import random as rd
import matplotlib.pyplot as plt
import pandas as pd

PUBLIC_CONTACT_RATE = 0.4
SI_RATE = 0.5
IR_RATE = 0.071
POPULATION = 20000
INITIAL_INFECTED = 200

class Individual:
    def __init__(self, simulation, initial_state=0):
        self.state = initial_state
        self.simulation = simulation
    
    def update(self):
        if self.state == 0:
            if rd.random() < PUBLIC_CONTACT_RATE * SI_RATE * self.simulation.I / POPULATION:
                self.state += 1
        elif self.state == 1:
            if rd.random() < IR_RATE:
                self.state += 1

class Simulation:
    def __init__(self, individuals: int):
        self.S = POPULATION - INITIAL_INFECTED
        self.I = INITIAL_INFECTED
        self.R = 0
        self.population = []
        for _ in range(self.I):
            self.population.append(Individual(self, 1))
        for _ in range(individuals - self.I):
            self.population.append(Individual(self))
    
    def update(self):
        new_S = 0
        new_I = 0
        new_R = 0
        for individual in self.population:
            individual.update()
            if individual.state == 0:
                new_S += 1
            if individual.state == 1:
                new_I += 1
            if individual.state == 2:
                new_R += 1
        self.S = new_S
        self.I = new_I
        self.R = new_R

simulation = Simulation(POPULATION)
data = {"day": [], "S": [], "I": [], "R": []}

tick = 0
print("...")
while simulation.I > 0:
    simulation.update()
    data["day"].append(tick)
    data["S"].append(simulation.S)
    data["I"].append(simulation.I)
    data["R"].append(simulation.R)
    tick += 1

plt.style.use("dark_background")
plt.plot(data["day"], data["S"], color=(1, 1, 0), label="Susceptible", lw=2)
plt.plot(data["day"], data["I"], color=(1, 0, 0), label="Infected", lw=2)
plt.plot(data["day"], data["R"], color=(0, 1, 0), label="Recovered", lw=2)
plt.legend()
plt.title(f"SIR model of COVID-19 given a population of {POPULATION} with {INITIAL_INFECTED} initially infected")
plt.xlabel(f"Days ({tick})")
plt.ylabel(f"Number of Individuals (S: {simulation.S}, I: {simulation.I}, R: {simulation.R})")

df = pd.DataFrame(data)
print(df.tail(100))

plt.show(block=True)