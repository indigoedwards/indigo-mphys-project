import numpy as np
import matplotlib.pyplot as plt
import iDEA as idea
import scipy as sp
import sys, os
import glob
import contextlib
from PIL import Image
import scipy as sp
import datetime
from tqdm import tqdm




distancelist = np.linspace(10,0,51)



output_filename = "energylevel-output23.txt"   
potentialchoice = "gaussian"
sensitivity = 20
limit = 50
predictiondatapoints = 4
tolerance = 0.1


def writetooutput(message):
    with open(output_filename,"a") as file:
        file.write(f"{message}\n")


# Disable printing
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore printing
def enablePrint():
    sys.stdout = sys.__stdout__

def getpotential(potential, distance):
    if potential == "testpotential":
        x = np.linspace(-60,60,150)
        v_ext = -0.49*np.exp(-1e-3*(x+40)**4) -0.5*np.exp(-1e-3*(x-40)**4)
    elif potential == "gaussian":
        x = np.linspace(-30,30,300)
        v_ext=-4*np.exp(-((x-distance)**2)/10) - 4.005*np.exp(-((x+distance)**2)/10)
    elif potential == "ISW":
        x = np.linspace(-30, 30, 180)
        v_ext = np.concatenate((np.full(16,100),np.full(29,0.01),np.full(90,100),np.full(30,0),np.full(15,100)))
    else:
        raise Exception("Invalid potential")
    return x,v_ext


excitationlist = [2,3]
energylist = []
for excitation in excitationlist:
    energylist.append([])
    for distance in distancelist:
        x = getpotential(potentialchoice,distance)[0]
        v_ext = getpotential(potentialchoice,distance)[1]
        v_int = idea.interactions.softened_interaction(x)
        system = idea.system.System(x,v_ext,v_int,electrons="uu")

        blockPrint()
        solvedstate = idea.methods.interacting.solve(system,k=excitation)
        enablePrint()
        idea.state.save_many_body_state(solvedstate,f"./23/e{excitation}d{str(distance).replace('.','-')}.state")
        energylist[excitation-2].append(solvedstate.energy)

        writetooutput(f"{datetime.datetime.now()}:      {round((float(np.where(distancelist==distance)[0][0]+1)/float((len(distancelist)*len(excitationlist))))*100,2)} %, k={excitation}, distance={distance}")
        
    plt.plot(distancelist,energylist[excitation-2])

writetooutput("")
writetooutput(energylist)
