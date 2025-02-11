import iDEA as idea
import numpy as np
import time

x = np.linspace(-30,30,300)
v_ext = -2*np.exp(-((x-10)**2)/10) - 2.005*np.exp(-((x+10)**2)/10)
v_int = idea.interactions.softened_interaction(x)
system = idea.system.System(x,v_ext,v_int,electrons="uu")
excitations = [0,1,2,3,4,5,6,7,8,9,10]
data = []

state = idea.methods.interacting.solve(system,k=3)

for excitation in excitations:
	result = []
	for i in range(0,5):
		start=time.time()
		#print(f"excitation {excitation}, attempt {i+1}")
		state = idea.methods.interacting.solve(system,k=excitation)
		end=time.time()
		result=np.append(result,(end-start))		
		print(f"finished excitation {excitation}, attempt {i+1}, time {end-start}")
	data = np.append(data,[excitation,np.sum(result),np.std(result)/np.sqrt(5)])

print(data)	
