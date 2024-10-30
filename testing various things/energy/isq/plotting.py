import matplotlib.pyplot as plt
import numpy as np

filelist = ["01","23","45","67"]
distancelist = np.linspace(10,0,51)

data = []
for i in filelist:
    with open(f"ISQ-energylevel-output{i}.txt","r") as file:
        arr = [line.strip() for line in file.readlines()][-1]
        data.append(arr)

for i in range(0,len(data)):
    data[i] = data[i].replace("[","")
    data[i] = data[i].replace("]","")
    data[i] = data[i].replace("np.float64(","")
    data[i] = data[i].replace(")","")
    data[i] = data[i].split(",")


data = np.array(data, dtype=np.float64)

energylist = []
for i in data:
    temp1 = []
    temp2 = []
    for j in range(0,int(len(i)/2)):
        temp1.append(i[j])
        temp2.append(i[j+51])
    energylist.append(temp1)
    energylist.append(temp2)

for i in range(0,8):
    if i==3:
        plt.plot(distancelist,energylist[i],"o-",label=f"{i}th Excited State")
    else:
        plt.plot(distancelist,energylist[i],"o",label=f"{i}th Excited State")

plt.xlabel("Seperation")
plt.ylabel("Energy")
plt.legend()
plt.xlim(max(distancelist),0)
plt.show()
