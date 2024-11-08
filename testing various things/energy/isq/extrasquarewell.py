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



excitationlist = [0,1,2,3,4,5,6,7,8,9]
distancelist = np.linspace(9.9,0.1,50)
output_filename = f"ISQ-energylevel-output-extra.txt"   
x = np.linspace(-30,30,300)

def writetooutput(message):
    with open(output_filename,"a") as file:
        file.write(f"{message}\n")

# Disable printing
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore printing
def enablePrint():
    sys.stdout = sys.__stdout__

def getpotential(separation):
    well_depth = 300
    well_width = 10
    xpoints = len(x)
    #create full array
    v_full = np.ones(xpoints)*well_depth
    #remove elements around the wells
    separation_x = separation*(xpoints/60)
    well_width_x = well_width*(xpoints/60)
    v_full[int((xpoints/2)-separation_x-(well_width_x/2)):int((xpoints/2)-separation_x+(well_width_x/2))] = 0
    v_full[int((xpoints/2)+separation_x-(well_width_x/2)):int((xpoints/2)+separation_x+(well_width_x/2))] = 0.01

    v_ext = v_full
    return(v_ext)



energylist = []
for excitation in tqdm(excitationlist,desc=f"Overall Progress"):
    energylist.append([])
    for distance in tqdm(distancelist,desc=f"Progress for excitation {excitation}"):
  
        v_ext = getpotential(distance)
        v_int = idea.interactions.softened_interaction(x)
        system = idea.system.System(x,v_ext,v_int,electrons="uu")

        blockPrint()
        state = idea.methods.interacting.solve(system,k=excitation)
        enablePrint()
        idea.state.save_many_body_state(state, f"./extra/e{excitation}d{str(round(distance,2)).replace('.','-')}.state")
        energylist[excitation-min(excitationlist)].append(state.energy)

        #writetooutput(f"{datetime.datetime.now()}:      {round((float(np.where(distancelist==distance)[0][0]+1)/float((len(distancelist)*len(excitationlist))))*100,2)} %, k={excitation}, distance={distance}")
        
    #plt.plot(distancelist,energylist[excitation-min(excitationlist)])

#writetooutput("")
#writetooutput(energylist)