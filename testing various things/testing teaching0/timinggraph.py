import matplotlib.pyplot as plt
import os
import numpy as np
print(os.getcwd())

#Takes output from teaching0 timings, averages & plots

#For 10 runs per number of cores
Nruns = 10


with open(r"./summary.txt") as file:
    data = [line.rstrip() for line in file.readlines()]
    data = np.delete(data, 0)
    data = np.array_split(data,(len(data)/(Nruns+2)))
    N = []
    meant = []
    for i in range(0,len(data)):
        data[i] = np.delete(data[i],(Nruns+1))
        N = np.append(N,float(data[i][0]))
        tempsum = 0
        for j in range(1,len(data[i])):
            tempsum = tempsum + float(data[i][j])
        meant = np.append(meant,tempsum/Nruns)

plt.plot(N,meant)
plt.xlabel("Number of Cores")
plt.ylabel("Average Time")
plt.savefig("timings.png")
