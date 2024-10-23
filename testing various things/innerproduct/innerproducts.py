import iDEA as idea
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

x = np.linspace(-30,30,300)
v_int = idea.interactions.softened_interaction(x)

distancelist = np.concatenate((np.linspace(7,0,71), np.zeros(5)))
v_extb10 = -2*np.exp(-((x-distancelist[10])**2)/10) - 2.005*np.exp(-((x+distancelist[10])**2)/10)
v_extb11 = -2*np.exp(-((x-distancelist[11])**2)/10) - 2.005*np.exp(-((x+distancelist[11])**2)/10)
v_extb12 = -2*np.exp(-((x-distancelist[12])**2)/10) - 2.005*np.exp(-((x+distancelist[12])**2)/10)
b10 = idea.system.System(x,v_extb10, v_int, electrons="uu")
b11 = idea.system.System(x,v_extb11, v_int, electrons="uu")
b12 = idea.system.System(x,v_extb12, v_int, electrons="uu")
b10_7 = idea.methods.interacting.solve(b10, k=7)
b11_7 = idea.methods.interacting.solve(b11, k=7)
b12_7 = idea.methods.interacting.solve(b12, k=7)


idea.system.save_system(b10_7,"b10_7.system")
idea.system.save_system(b10_7,"b11_7.system")
idea.system.save_system(b10_7,"b12_7.system")
print("done")