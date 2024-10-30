import numpy as np
import iDEA as idea
import matplotlib.pyplot as plt


xtestspace = np.linspace(25,500,20).astype(int)

energies=[]
for xnumber in xtestspace:
    x = np.linspace(-30,30,xnumber)
    v_int = idea.interactions.softened_interaction(x)
    v_ext = -2*np.exp(-((x-10)**2)/10) - 2.005*np.exp(-((x+10)**2)/10) #gaussians
    
    system = idea.system.System(x,v_ext,v_int,electrons="uu")
    system_firststate = idea.methods.interacting.solve(system, k=1)
                                                      
    charge_density = idea.observables.density(system, state=system_firststate)
    hartree_potential = idea.observables.hartree_potential(system, charge_density)
    energies.append(idea.observables.hartree_energy(system, charge_density, hartree_potential))


plt.plot(xtestspace,energies, "m-")
plt.xlabel("Number of x grid points")
plt.ylabel("Hartree energy")
plt.savefig("energies10.png")
plt.close()

plt.plot(xtestspace, np.log10(energies-energies[-1]), "m-")
plt.xlabel("Number of x grid points")
plt.ylabel("Log (energy difference)")
plt.savefig("logenergies10.png")