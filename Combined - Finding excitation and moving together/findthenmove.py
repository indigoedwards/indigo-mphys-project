import numpy as np
import matplotlib.pyplot as plt
import iDEA as idea
import scipy as sp
import sys, os
import glob
import contextlib
from PIL import Image

#This program is used to find an excited state for a specific potential, then move the excited state closer to form a many body excited state

#----Parameters----
#options for potential: gaussian, 
#sensitivity is how sensitive the double excitation finder is.
#limit is how many excited states are searched before it gives up.
#-------------------
potentialchoice = "gaussian"
sensitivity = 20
limit = 50

figure, axis = plt.subplots(1,3)

distancelist = np.concatenate((np.linspace(20,5,61), np.linspace(4.9,0,99), np.zeros(5)))



#------------------------------------------------------------------------------------------------------------------------------------------
#function to determine if a density contains two electons, each in their first state.
def isdoubleexcitation (density, sensitivity):
    x = getpotential(potentialchoice,20)[0]
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

#--------------------------------------------------------------------------------------------------------
# Disable printing
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore printing
def enablePrint():
    sys.stdout = sys.__stdout__
#--------------------------------------------------------------------------------------------------------
#find the potential (distance is from origin)
def getpotential(potential, distance):
    if potential == "testpotential":
        x = np.linspace(-60,60,150)
        v_ext = -0.49*np.exp(-1e-3*(x+40)**4) -0.5*np.exp(-1e-3*(x-40)**4)
    elif potential == "gaussian":
        x = np.linspace(-30,30,150)
        v_ext=-2*np.exp(-((x-distance)**2)/10) - 2.005*np.exp(-((x+distance)**2)/10)
    elif potential == "ISW":
        x = np.linspace(-30, 30, 180)
        v_ext = np.concatenate((np.full(16,100),np.full(29,0.01),np.full(90,100),np.full(30,0),np.full(15,100)))
    else:
        raise Exception("Invalid potential")
    return x,v_ext
#------------------------------------------------------------------------------------------------------------
#cycle through excitation states to find the double excitation
def finddoubleexcitation():
    #solve
    print("Finding double excitation")
    distance = 20
    v_int = idea.interactions.softened_interaction(getpotential(potentialchoice,distance)[0])
    system = idea.system.System(getpotential(potentialchoice,distance)[0],getpotential(potentialchoice,distance)[1],v_int,electrons="uu")
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
        #plt.plot(system.x, density, "m-", label="density")
        #plt.plot(system.x, v_ext, "g--", label="potential")
        #plt.xlabel("x")
        #plt.ylim(-0.5,1)
        #plt.ylabel("v_ext / prob. density")
        #plt.title(f"Potential: {potential}, Excitation number: {i}")
        #plt.legend()
        #plt.savefig(f"doubleexcitation{potential}")
        return i
    elif found == 2:
        raise Exception("No double excitations found up to the 50th excited state")
#-----------------------------------------------------------------------------------------------
#Moves the electrons closer to eachother
def moveelectrons(distancelist):
    energies = []
    excitation = finddoubleexcitation()
    print("Generating movement")
    #cycle through distances
    for distance in distancelist:
        #define and solve system
        x = getpotential(potentialchoice,distance)[0]
        v_ext = getpotential(potentialchoice,distance)[1]
        v_int = idea.interactions.softened_interaction(x)
        system = idea.system.System(x,v_ext,v_int,electrons="uu")
        blockPrint()           
        solvedsystem = idea.methods.interacting.solve(system, k=excitation)
        enablePrint()
        print(f"{round((float(np.where(distancelist==distance)[0][0]+1)/float((len(distancelist))))*100,2)} percent done")

        #calculate observables
        charge_density = idea.observables.density(system, state=solvedsystem)
        hartree_potential = idea.observables.hartree_potential(system, charge_density)
        energies.append(idea.observables.hartree_energy(system, charge_density, hartree_potential))
        
        #create and save density plots
        axis[0].plot(system.x, charge_density, "m-", label="Prob. Density")
        axis[0].plot(system.x, v_ext, "g--", label="Potential")
        axis[0].set_xlabel("x")
        axis[0].set_ylabel("v_ext / prob. density")
        axis[0].set_ylim(-2,0.75)
        axis[0].legend()
        #axis[0].savefig(f"a{str(np.where(distancelist==distance)[0][0]).zfill(3)}.png")
        #plt.close()

        #create and save wavefunction plots
        axis[1].imshow(solvedsystem.space.real, cmap="seismic", vmax=0.75, vmin=-0.75)
        axis[1].set_xlabel("x")
        axis[1].set_ylabel("x'")
        axis[1].set_ylim(0,140)
        #axis[1].savefig(f"b{str(np.where(distancelist==distance)[0][0]).zfill(3)}.png")
        #plt.close()

        #create and save energy plots
        axis[2].plot(distancelist[0:len(energies)], energies)
        axis[2].set_xlabel("Distance")
        axis[2].set_ylabel("Hartree Energy")
        axis[2].set_xlim(max(distancelist),0)
        #axis[2].savefig(f"c{str(np.where(distancelist==distance)[0][0]).zfill(3)}.png")
        #plt.close()
        plt.savefig(f"{str(np.where(distancelist==distance)[0][0]).zfill(3)}.png")
        plt.close()
        
    #create gifs from saved plots
    fp_in = "*.png"
    fp_out = "plots.gif"
    with contextlib.ExitStack() as stack:
        # lazily load images
        imgs = (stack.enter_context(Image.open(f))
                for f in sorted(glob.glob(fp_in)))
        # extract  first image from iterator
        img = next(imgs)
        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
        img.save(fp=fp_out, format='GIF', append_images=imgs,
                save_all=True, duration=100, loop=0)

    return energies


#-------------------------------------------------------------------------------------------------------
#Run program

energies = moveelectrons(distancelist)
plt.plot(distancelist, energies)
plt.xlabel("Distance")
plt.ylabel("Hartree Energy")
plt.xlim(max(distancelist),0)
plt.savefig("energyplot.png")
print("Done! :D")


#-----------------------------------------------------------------------------------------------
