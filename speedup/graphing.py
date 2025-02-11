import numpy as np
import matplotlib.pyplot as plt
import collections
from collections.abc import Iterable




filelist = [1,2,4,6,8,12,16,20,24,28,32,40,48,56,64,72,88,96]

data = []
excitationdata = np.zeros((11,2,18))

for i in range(0,len(filelist)):
    arr = ""
    with open(f"log{filelist[i]}.txt","r") as file:
        for line in file.readlines():
            arr = (arr +" " +line.strip().strip("[").strip("]"))
        data=np.array(arr[6463:6958].split(),dtype=np.float64)
        #print(arr[6463:6958])
       
    for j in range(0,10):
        excitationdata[j][0][i] = data[(j*3)+1]
        excitationdata[j][1][i] = data[(j*3)+2]

print(excitationdata[9][0])