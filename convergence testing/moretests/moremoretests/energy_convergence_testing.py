import numpy as np
import iDEA as idea
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys,os

def writetooutput(message):
    with open(output_filename,"a") as file:
        file.write(f"{message}\n")


xtestspace = np.concatenate(([25,50,75],np.linspace(100,1000,10))).astype(int)
distances = [20,10,5,0]
excitation = 9
output_filename = f"excitation0convergence.txt"   




for distance in tqdm(distances,desc="Total Progress",smoothing=0):
    for xnumber in tqdm(xtestspace,desc=f"Distance {distance}",smoothing=0):
        x = np.linspace(-30,30,xnumber)
        v_int = idea.interactions.softened_interaction(x)
        v_ext = -2*np.exp(-((x-distance)**2)/10) - 2.005*np.exp(-((x+distance)**2)/10) #gaussians      
        system = idea.system.System(x, v_ext, v_int, electrons="uu")
        system_state = idea.methods.interacting.solve(system, k=excitation, stopprint=True, allstates=True)
        idea.state.save_many_body_state(system_state,f"d{"distance".zfill(2)}.state")
                                                   
        

