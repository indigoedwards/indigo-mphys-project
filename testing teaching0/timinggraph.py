import matplotlib.pyplot as plt
import os
import numpy as np


with open(r"C:/Users/Iansyst Loan/indigo-mphys-project/testing teaching0/summary.txt") as file:
    data = [line.rstrip() for line in file.readlines()]
    data = [line.split(" ") for line in data]
    data = np.transpose(data)
    N = np.delete(data[0],0)
    t = np.delete(data[1],0)
    N1 = []
    t1 = []
    for i in range(0,len(N)-1):
        N1 = np.append(N1, float(N[i]))
    for i in range(0,len(t)-1):
        t1 = np.append(t1, float(t[i]))





plt.plot(N1,t1)
plt.savefig("timings.png")
