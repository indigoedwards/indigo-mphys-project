import iDEA as idea
import matplotlib.pyplot as plt
import numpy as np
import time

threadlist = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
xpointlist = np.linspace(25,500,20).astype(int)

timelist = []
for thread in threadlist:
    for xpoint in xpointlist:
        x = np.linspace(-30,30,xpoint)
        v_int = idea.interactions.softened_interaction(x)
        v_ext = -2*np.exp(-((x-20)**2)/10) - 2.005*np.exp(-((x+20)**2)/10) #gaussians
        system = idea.system.System(x,v_ext,v_int,electrons="uu")

        start = time.time()
        system_firststate = idea.methods.interacting.solve(system, k=1)
        end = time.time()

        timelist.append(end-start)

with open("3dgraphdata.txt","a") as file:
    file.write([threadlist,xpointlist,timelist])


