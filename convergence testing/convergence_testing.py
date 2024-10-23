import numpy as np
import iDEA as idea
import matplotlib.pyplot as plt
import time


xtestspace = np.linspace(25,500,20).astype(int)

times=[]
for xnumber in xtestspace:
    x = np.linspace(-30,30,xnumber)
    v_int = idea.interactions.softened_interaction(x)
    v_ext = -2*np.exp(-((x-20)**2)/10) - 2.005*np.exp(-((x+20)**2)/10) #gaussians
    
    system = idea.system.System(x,v_ext,v_int,electrons="uu")
    start = time.time()
    system_firststate = idea.methods.interacting.solve(system, k=1)
    end = time.time()
    print("Tested", xnumber)
    times.append(end-start)




plt.plot(xtestspace,times, "m-")
plt.xlabel("Number of x grid points")
plt.ylabel("Time (seconds)")
plt.savefig("times.png")
plt.close()

plt.plot(xtestspace, np.log10(times), "m-")
plt.xlabel("Number of x grid points")
plt.ylabel("Log (time)")
plt.savefig("logtimes.png")