import numpy as np
import iDEA as idea
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys,os

# Disable printing
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore printing
def enablePrint():
    sys.stdout = sys.__stdout__

def writetooutput(message):
    with open(output_filename,"a") as file:
        file.write(f"{message}\n")


xtestspace = np.concatenate(([25],np.linspace(100,1000,10))).astype(int)
distances = [20,10,5,0]
excitation = 0
output_filename = f"excitation0convergence.txt"   




for distance in tqdm(distances,desc="Total Progress",smoothing=0):
    for xnumber in (pbar := (tqdm(xtestspace,desc=f"Distance {distance}",smoothing=0))):
        pbar.set_postfix_str(f"x number: {xnumber}")
        x = np.linspace(-30,30,xnumber)
        v_int = idea.interactions.softened_interaction(x)
        v_ext = -2*np.exp(-((x-distance)**2)/10) - 2.005*np.exp(-((x+distance)**2)/10) #gaussians
        
        system = idea.system.System(x,v_ext,v_int,electrons="uu")
        blockPrint()
        system_state = idea.methods.interacting.solve(system, k=excitation)
        enablePrint()                                                        
        writetooutput(f"{excitation},{distance},{xtestspace},{system_state.energy}")

