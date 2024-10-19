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

#This program is used to find an excited state for a specific potential, then move the excited state closer to form a many body excited state

#----Parameters----
#options for potential: gaussian, 
#sensitivity is how sensitive the double excitation finder is.
#limit is how many excited states are searched before it gives up.
#distancelist defines the x space
#predictiondatapoints is the number of previous datapoints used to predict the next energy
#fitfunc is the function used for the energy prediction
#-------------------
potentialchoice = "gaussian"
sensitivity = 20
limit = 50
predictiondatapoints = 4
distancelist = np.concatenate((np.linspace(7,0,29), np.zeros(5)))
tolerance = 0.1
def fitfunc(x,a,b):
    return ((a*x)+b) #linear

output_filename = "output.txt"    

#--------------------------------------------------------------------------------------------
#Writing to output file
def writetooutput(message):
    with open(output_filename,"a") as file:
        file.write(f"{message}\n")

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
        x = np.linspace(-30,30,300)
        v_ext=-4*np.exp(-((x-distance)**2)/10) - 4.005*np.exp(-((x+distance)**2)/10)
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
    writetooutput("Finding double excitation")
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
            writetooutput(f"Searched k={i}, continuing...")
            i = i + 1
        
    if found == 1:  
        writetooutput(f"Double excitation found in the {i}th excited state.")
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
#------------------------------------------------------------------------------------------------
#predicting the next energy
""""
def energy_prediction(distancelist,energies):
    #make arrays the same size
    pred_distancelist = distancelist[len(energies)-predictiondatapoints:len(energies)]
    pred_energies = energies[len(energies)-predictiondatapoints:len(energies)]

    #apply curve fit
    fit, useless = sp.optimize.curve_fit(fitfunc, pred_distancelist, pred_energies)
    
    #return prediction for the next distance value
    return (fitfunc(distancelist[len(pred_distancelist)+1],*fit))
"""
#--------------------------------------------------------------------------------------------------
#are the states the same? Using inner product
def same_state(state1,state2,system):
    innerproduct = np.sum(abs(state1.space.real)*abs(state2.space.real))*system.dx**system.count
    writetooutput(f"inner product: {innerproduct}")
    if (abs(innerproduct-1) < tolerance):
        return True
    else:
        return False

#-----------------------------------------------------------------------------------------------
def findenergy(system, solvedsystem):
    charge_density = idea.observables.density(system, state=solvedsystem)
    hartree_potential = idea.observables.hartree_potential(system, charge_density)
    energy = idea.observables.hartree_energy(system, charge_density, hartree_potential)
    return energy,charge_density



#--------------------------------------------------------------------------------------------------
#Moves the electrons closer to eachother
def moveelectrons(distancelist):
    print("generating movement")
    energies = []
    #excitation = finddoubleexcitation()
    excitation = 7
    #cycle through distances
    for distance in distancelist:
        #define system
        x = getpotential(potentialchoice,distance)[0]
        v_ext = getpotential(potentialchoice,distance)[1]
        v_int = idea.interactions.softened_interaction(x)
        system = idea.system.System(x,v_ext,v_int,electrons="uu")
        

        
        
        #solve system
        blockPrint()
        newstate = idea.methods.interacting.solve(system,k=excitation)
        enablePrint()

        #check if the new state is the same as the old state
        samestate = False
        if (np.where(distancelist==distance)[0][0]>0):
            samestate = same_state(newstate,laststate,system)
            
        else:
            samestate = True

        #if they are not the same, check the states around it
        n = 1
        while samestate == False:
            writetooutput("Double excitation not found, checking surrounding states")
            blockPrint()
            plusstate = idea.methods.interacting.solve(system,k=excitation+n)
            plusstatus = same_state(plusstate, laststate,system)
            writetooutput(f"plus state: {plusstatus}")
            minusstate = idea.methods.interacting.solve(system,k=excitation-n)
            minusstatus = same_state(minusstate, laststate,system)
            writetooutput(f"minus state: {minusstatus}")
            enablePrint()
            if plusstatus == True:
                excitation = excitation + n
                newstate = plusstate
            elif minusstatus == True:
                excitation = excitation - n
                newstate = minusstate
            else:
                if (n<3):
                    n = n + 1
                else:
                    writetooutput(f"No correct states found in the 6 surrounding excitations, distance = {distance}")
                    raise Exception("No correct states found in the 6 surrounding excitations")

        laststate=newstate
        energies.append(findenergy(system,newstate)[0])

        writetooutput(f"{datetime.datetime.now()}:      {round((float(np.where(distancelist==distance)[0][0]+1)/float((len(distancelist))))*100,2)} %, k={excitation}, distance={distance}")
        #create and save density plots
        plt.plot(system.x, findenergy(system,newstate)[1], "m-", label="Prob. Density")
        plt.plot(system.x, v_ext, "g--", label="Potential")
        plt.xlabel("x")
        plt.ylabel("v_ext / prob. density")
        plt.ylim(-2,0.75)
        plt.legend()
        plt.savefig(f"a{str(np.where(distancelist==distance)[0][0]).zfill(3)}.png")
        plt.close()

        #create and save wavefunction plots
        plt.imshow(newstate.space.real, cmap="seismic", vmax=0.75, vmin=-0.75)
        plt.xlabel("x")
        plt.ylabel("x'")
        plt.gca().invert_yaxis()
        plt.savefig(f"b{str(np.where(distancelist==distance)[0][0]).zfill(3)}.png")
        plt.close()

        #create and save energy plots
        plt.plot(distancelist[0:len(energies)], energies)
        plt.xlabel("Distance")
        plt.ylabel("Hartree Energy")
        plt.xlim(max(distancelist),0)
        plt.savefig(f"c{str(np.where(distancelist==distance)[0][0]).zfill(3)}.png")
        plt.close()

    #create gifs from saved plots
    fp_in = "a*.png"
    fp_out = "density.gif"
    with contextlib.ExitStack() as stack:
        # lazily load images
        imgs = (stack.enter_context(Image.open(f))
                for f in sorted(glob.glob(fp_in)))
        # extract  first image from iterator
        img = next(imgs)
        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
        img.save(fp=fp_out, format='GIF', append_images=imgs,
                save_all=True, duration=100, loop=0)

    fp_in = "b*.png"
    fp_out = "wavefunction.gif"
    with contextlib.ExitStack() as stack:
        # lazily load images
        imgs = (stack.enter_context(Image.open(f))
                for f in sorted(glob.glob(fp_in)))
        # extract  first image from iterator
        img = next(imgs)
        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
        img.save(fp=fp_out, format='GIF', append_images=imgs,
                save_all=True, duration=100, loop=0)
    
    fp_in = "c*.png"
    fp_out = "energy.gif"
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
writetooutput("-----------------------------------------------------------")
writetooutput(f"===BEGIN PROGRAM {datetime.datetime.now()}===")
energies = moveelectrons(distancelist)
plt.plot(distancelist, energies)
plt.xlabel("Distance")
plt.ylabel("Hartree Energy")
plt.xlim(max(distancelist),0)
plt.savefig("energyplot.png")
writetooutput("Done! :D")


#-----------------------------------------------------------------------------------------------
