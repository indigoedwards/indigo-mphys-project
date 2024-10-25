import iDEA as idea
import matplotlib.pyplot as plt
import numpy as np
import time
import sys,os
import datetime

def blockprint():
    sys.stdout = open(os.devnull,"w")

def enableprint():
    sys.stdout = sys.__stdout__

def writetooutput(message):
    with open("3ddata00.txt","a") as file:
        file.write(f"{message}\n")

excitationlist = [0,1,2,3,4,5,6,7,8,9,10]
xpointlist = np.linspace(25,500,20).astype(int)

distancelist = [0]
for distance in distancelist:
    timelist = []
    for excitation in excitationlist:
        for xpoint in xpointlist:
            x = np.linspace(-30,30,xpoint)
            v_int = idea.interactions.softened_interaction(x)
            v_ext = -2*np.exp(-((x-distance)**2)/10) - 2.005*np.exp(-((x+distance)**2)/10) #gaussians
            system = idea.system.System(x,v_ext,v_int,electrons="uu")
            blockprint()
            start = time.time()
            state = idea.methods.interacting.solve(system, k=excitation)
            end = time.time()
            enableprint()
            writetooutput(f"{datetime.datetime.now()},{distance},{excitation},{xpoint},{end-start},{state.energy}")
        



