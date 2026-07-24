import random as rd
import numpy as np
from constants import *
import matplotlib.pyplot as plt
import json
import scipy.sparse


# for _ in range(100):
    # plt.hist(np.random.lognormal(LOGN_MU, LOGN_STDEV, POPULATION), 100, color=(0.3, 0, 0.8, 0.1))

# generate network

degrees = list(map(int, np.random.lognormal(LOGN_MU, LOGN_STDEV, POPULATION)))
plt.hist(degrees, 100, color=(0.3, 0, 0.8))
plt.show(block=False)
prep = []

network = {}

for i in range(POPULATION):
    for _ in range(degrees[i]):
        prep.append(i)
    network[i] = [[]]

np.random.shuffle(prep)

while len(prep) > 1:
    while prep[0] == prep[1]:
        np.random.shuffle(prep)
    network[prep[0]][0].append(prep[1])
    network[prep[1]][0].append(prep[0])
    del prep[0:2]
    print("tie generation:", len(prep) // 2, "left.")

for n in network:
    try:
        network[n].append(round(1/len(network[n][0]), 3))
    except ZeroDivisionError:
        network[n].append(0)
    print("weight generation:", len(network) - n, "left.")

json.dump(network, open("network.json", "w"), indent=4)