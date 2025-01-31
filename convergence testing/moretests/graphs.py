import numpy as np
import iDEA as idea
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys,os

def getdata(excitation):
    data = []

    with open(f"excitation{excitation}convergence.txt","r") as file:
        arr = [line.strip().split(",") for line in file.readlines()]
        data.append(arr)
    data = data[0]

    data = np.array(data, dtype=np.float64)

    distance0 = [0,0,0,0]
    distance5 = [0,0,0,0]
    distance10 = [0,0,0,0]
    distance20 = [0,0,0,0]

    for i in data:
        if i[1] == 0.0:
            distance0 = np.vstack([distance0,i])
        if i[1] == 5:
            distance5 = np.vstack([distance5,i])
        if i[1] == 10:
            distance10 = np.vstack([distance10,i])
        if i[1] == 20:
            distance20 = np.vstack([distance20,i])

    distance0 = distance0[1:].transpose()
    distance5 = distance5[1:].transpose()
    distance10 = distance10[1:].transpose()
    distance20 = distance20[1:].transpose()
    return [distance20,distance10,distance5,distance0]

bigdata = np.zeros((3,4,4,11))
excitations = [0,7,9]
distances = [20,10,5,0]

for excitationindex in range(0,len(excitations)):
    bigdata[excitationindex] = getdata(excitations[excitationindex])

#energy = [excitation][distance][xpoint][energy]

for i in range(0,len(bigdata[0])):
    for j in range(0,len(bigdata)):
        plt.plot(bigdata[j][i][2],np.log10(abs(bigdata[j][i][3]-bigdata[j][i][3][-1])),label=f"Excitation {excitations[j]}")
    plt.title(f"Distance from 0 = {distances[i]}")
    plt.legend()
    plt.xlabel("Number of x-points")
    plt.ylabel("log(Energy difference)")
    plt.savefig(f"d{distances[i]}.png")
    plt.close()
