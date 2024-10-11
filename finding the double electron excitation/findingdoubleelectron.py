
import numpy as np
import matplotlib.pyplot as plt
import iDEA as idea
import scipy as sp
import sys, os

#This program will iterate through excited states till it finds a state where both electrons are in their first excited state.

#Parameters
potential = "testpotential"
sensitivity = 20
limit = 50


#------------------------------------------------------------------------------------------------------------------------------------------
#function to determine if a density contains two electons, each in their first state.
def isdoubleexcitation (density, sensitivity):

    #find peaks in the density which are more than half the height of the maximum.
    density_peaks = sp.signal.find_peaks(density, height = 0.01)
    #print(density_peaks[0])
    #if there are 4 peaks then continue, otherwise return false
    if len(density_peaks[0]) != 4:
        return False
    else:
        #if the peaks are grouped into sets of 2 then return true, otherwise return false
        if abs(x[density_peaks[0][1]]-x[density_peaks[0][0]]) < 10 and abs(x[density_peaks[0][3]]-x[density_peaks[0][2]]) < sensitivity:
            return True
        else:
            return False

# Disable printing
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore printing
def enablePrint():
    sys.stdout = sys.__stdout__


#----------------------------------------------------------------------------------
#Define the system
if potential == "testpotential":
    x = np.linspace(-60,60,150)
    v_ext = -0.49*np.exp(-1e-3*(x+40)**4) -0.5*np.exp(-1e-3*(x-40)**4)
elif potential == "gaussian":
    x = np.linspace(-30,30,150)
    v_ext = -2*np.exp(-((x-20)**2)/10) - 2.005*np.exp(-((x+20)**2)/10)
elif potential == "ISW":
    x = np.linspace(-30, 30, 180)
    v_ext = np.concatenate((np.full(16,100),np.full(29,0.01),np.full(90,100),np.full(30,0),np.full(15,100)))
else:
    raise Exception("Invalid potential")

v_int = idea.interactions.softened_interaction(x)
system = idea.system.System(x,v_ext,v_int,electrons="uu")

#solve
found = 0
i = 0
while found == 0:
    blockPrint()
    teststate = idea.methods.interacting.solve(system, k=i)
    enablePrint()
    density = idea.observables.density(system, state=teststate)
    if i > limit:
        found = 2
    elif isdoubleexcitation(density,sensitivity) == True:
        found = 1
    elif isdoubleexcitation(density,sensitivity) == False:
        print(f"Searched k={i}, continuing...")
        i = i + 1
    
if found == 1:  
    print(f"Double excitation found in the {i}th excited state.")
    plt.plot(system.x, density, "m-", label="density")
    plt.plot(system.x, v_ext, "g--", label="potential")
    plt.xlabel("x")
    plt.ylim(-0.5,1)
    plt.ylabel("v_ext / prob. density")
    plt.title(f"Potential: {potential}, Excitation number: {i}")
    plt.legend()
    plt.savefig(f"doubleexcitation{potential}")
elif found == 2:
    print("No double excitations found up to the 50th excited state")
