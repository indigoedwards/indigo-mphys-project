import numpy as np
import matplotlib.pyplot as plt
import iDEA as idea
import scipy as sp
import pickle

def potentialsingle(x):
    arr1 = np.zeros_like(x)

    # First condition: -4 <= (x - d) <= 4
    condition1 = (-4 <= (x)) & (x <= 4)

    # Apply the first formula where the first condition is true
    arr1[condition1] = 0.25 * (x[condition1])**2 - 4

    return arr1


def potential(x,d,potential_name):

    if potential_name == "triangular":
        potential1 = np.zeros(300)
        potential2 = np.zeros(300)
        for xindex in range(0,len(x)):
            if x[xindex]<=-d-2:
                potential1[xindex] = 0
            if -d-2<x[xindex]<=-d:
                potential1[xindex] = -2*(x[xindex]+d)-8
            if -d<x[xindex]<=-d+2:
                potential1[xindex] = 2*(x[xindex]+d)-8
            if -d+2<x[xindex]:
                potential1[xindex] = 0
        for xindex in range(0,len(x)):
            if x[xindex]<=d-2:
                potential2[xindex] = 0
            if d-2<x[xindex]<=d:
                potential2[xindex] = -2*(x[xindex]-d)-8.001
            if d<x[xindex]<=d+2:
                potential2[xindex] = 2*(x[xindex]-d)-8.001
            if d+2<x[xindex]:
                potential2[xindex] = 0

        return potential1 + potential2
    
    if potential_name == "gaussian1":
        return (-4*np.exp(-((x-d)**2)/10) - 4.005*np.exp(-((x+d)**2)/10))

    if potential_name == "square1":
        well_depth = 4
        well_width = 5
        xpoints = len(x)
        xpoint_range = abs(max(x))+abs(min(x))
        #create full array
        v_full = np.ones(xpoints)*well_depth
        #remove elements around the wells
        separation_x = d*(xpoints/xpoint_range)
        well_width_x = well_width*(xpoints/xpoint_range)
        v_full[int((xpoints/2)-separation_x-(well_width_x/2)):int((xpoints/2)-separation_x+(well_width_x/2))] = 0
        v_full[int((xpoints/2)+separation_x-(well_width_x/2)):int((xpoints/2)+separation_x+(well_width_x/2))] = 0.01

        v_ext = v_full-4
        return(v_ext)
            
    if potential_name == "square2":
        well_depth = 4
        well_width = 10
        xpoints = len(x)
        xpoint_range = abs(max(x))+abs(min(x))
        #create full array
        v_full = np.ones(xpoints)*well_depth
        #remove elements around the wells
        separation_x = d*(xpoints/xpoint_range)
        well_width_x = well_width*(xpoints/xpoint_range)
        v_full[int((xpoints/2)-separation_x-(well_width_x/2)):int((xpoints/2)-separation_x+(well_width_x/2))] = 0
        v_full[int((xpoints/2)+separation_x-(well_width_x/2)):int((xpoints/2)+separation_x+(well_width_x/2))] = 0.1

        v_ext = v_full-4
        return(v_ext)
    
    if potential_name == "square3":
        well_depth = 4
        well_width = 2
        xpoints = len(x)
        xpoint_range = abs(max(x))+abs(min(x))
        #create full array
        v_full = np.ones(xpoints)*well_depth
        #remove elements around the wells
        separation_x = d*(xpoints/xpoint_range)
        well_width_x = well_width*(xpoints/xpoint_range)
        v_full[int((xpoints/2)-separation_x-(well_width_x/2)):int((xpoints/2)-separation_x+(well_width_x/2))] = 0
        v_full[int((xpoints/2)+separation_x-(well_width_x/2)):int((xpoints/2)+separation_x+(well_width_x/2))] = 0.01

        v_ext = v_full-4
        return(v_ext)
    
    if potential_name == "hookes":
        # Initialize result array with zeros
        arr1 = np.zeros_like(x)
        arr2 = np.zeros_like(x)

        # First condition: -4 <= (x - d) <= 4
        condition1 = (-4 <= (x - d)) & (x - d <= 4)
        
        # Second condition: -4 <= (x + d) <= 4
        condition2 = (-4 <= (x + d)) & (x + d <= 4)

        # Apply the first formula where the first condition is true
        arr1[condition1] = 0.25 * (x[condition1] - d)**2 - 4
        
        # Apply the second formula where the second condition is true
        arr2[condition2] = 0.25 * (x[condition2] + d)**2 - 4

        return arr1+arr2
    
    if potential_name == "trapezoid":
        arr1 = np.zeros_like(x)
        arr2 = np.zeros_like(x)

        condition1= ((d - 1) <= x )& ((d+1) >= x)
        condition2= ((d - 2) <= x) & ((d-1) >= x)
        condition3= ((d + 1) <= x) & ((d+2) >= x)

        arr1[condition1] = -4
        arr1[condition2] = -4*(x[condition2]-d+2)
        arr1[condition3] = 4*(x[condition3]-d-2)

        condition1= ((-d - 1) <= x) & ((-d+1) >= x)
        condition2= ((-d - 2) <= x) & ((-d-1) >= x)
        condition3= ((-d + 1) <= x) & ((-d+2) >= x)

        arr2[condition1] = -4
        arr2[condition2] = -4*(x[condition2]+d+2)
        arr2[condition3] = 4*(x[condition3]+d-2)

        return arr1+arr2
    
    if potential_name == "cosine":
        # Initialize result array with zeros
        arr1 = np.zeros_like(x)
        arr2 = np.zeros_like(x)

        # First condition: -pi <= (x - d) <= pi
        condition1 = (-np.pi <= (x - d)) & (x - d <= np.pi)
        
        # Second condition: -pi <= (x + d) <= pi
        condition2 = (-np.pi <= (x + d)) & (x + d <= np.pi)

        # Apply the first formula where the first condition is true
        arr1[condition1] = -2 * np.cos(x[condition1] - d) - 2
        
        # Apply the second formula where the second condition is true
        arr2[condition2] = -2 * np.cos(x[condition2] + d) - 2

        return arr1+arr2
    
    if potential_name == "snake":
        return
    
    if potential_name == "circular":
        arr1 = np.zeros_like(x)
        arr2 = np.zeros_like(x)

        condition1= (d-4<=x) & (d+4>=x)
        condition2= (-d-4<=x) & (-d+4>=x)

        arr1[condition1] = -np.abs(np.sqrt((16-(x[condition1]-d)**2)))
        arr2[condition2] = -np.abs(np.sqrt((16-(x[condition2]+d)**2)))
        return arr1+arr2
    
    if potential_name == "house":
        arr1 = np.zeros_like(x)
        arr2 = np.zeros_like(x)

        condition1 = (d<=x) & (x<=d+2)
        condition2 = (d-2<=x) & (x<=d)

        arr1[condition1] = (x[condition1]-d-2)-4
        arr1[condition2] = -(x[condition2]-d+2)-4

        condition1 = (-d<=x) & (x<=-d+2)
        condition2 = (-d-2<=x) & (x<=-d)

        arr2[condition1] = (x[condition1]+d-2)-4
        arr2[condition2] = -(x[condition2]+d+2)-4

        return arr1+arr2
    
    if potential_name == "r-triangle":
        arr1 = np.zeros_like(x)
        arr2 = np.zeros_like(x)

        condition1 = (d-2<=x) & (x<=d+2)
        condition2 = (-d-2<=x) & (x <= -d+2)

        arr1[condition1] = (2/3)*(x[condition1]-d-2)
        arr2[condition2] = (2/3)*(x[condition2]+d-2)

        return arr1 + arr2
    
    if potential_name == "psuedo":
        return
    
    if potential_name == "gaussian2":
        return (-8*np.exp(-((x-d)**2)/10) - 8.005*np.exp(-((x+d)**2)/10))
        
    
    if potential_name == "gaussian3":
        return (-2*np.exp(-((x-d)**2)/10) - 2.005*np.exp(-((x+d)**2)/10))
    
    if potential_name == "gaussian4":
        return
    
    if potential_name == "gaussian5":
        return
    
    if potential_name == "mypotential":
        return






x = np.linspace(-20,20,300)
v_int = idea.interactions.softened_interaction(x)

def single():
    v_ext = potentialsingle(x)
    
    system = idea.system.System(x,v_ext,v_int,electrons="u")
    state = idea.methods.interacting.solve(system,k=7)
    plt.plot(system.x, idea.observables.density(system, state=state), "m-", label="Charge Density")
    plt.plot(system.x, system.v_ext, "g--", label="Potential")
    plt.xlabel("x (Bohrs)")
    plt.ylabel("v_ext / charge density")
    plt.legend()
    plt.show()
    plt.close()

def double(e): 
    v_ext = potential(x,10,"square3")
    system = idea.system.System(x,v_ext,v_int,electrons="uu")
    state = idea.methods.interacting.solve(system,k=e)

   
    plt.imshow(state.full[...][:,0,:,0], cmap="seismic", vmax=0.75, vmin=-0.75, extent=[-20, 20, 20, -20], aspect=1)
    plt.xlabel("x, position of electron 1 (Bohrs)")
    plt.ylabel("x', poisition of electron 2 (Bohrs)")
    plt.colorbar()
    plt.xlim([-20,20])
    plt.ylim([-20,20])
    plt.show()
    plt.close()
 
    plt.plot(system.x, idea.observables.density(system, state=state), "m-", label="Charge Density")
    plt.plot(system.x, system.v_ext, "g--", label="Potential")
    plt.xlabel("x (Bohrs)")
    plt.ylabel("v_ext / charge density")
    plt.legend()
    plt.show()
    plt.close()

double(5)