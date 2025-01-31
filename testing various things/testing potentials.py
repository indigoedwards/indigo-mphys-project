import numpy as np
import matplotlib.pyplot as plt
import iDEA as idea


def equation(x, d):
    # First part of the equation (involving x - d)
    term1_1 = 2 * np.exp(-((x - d) / 2.551) ** 2) / np.sqrt((x - d) ** 2 + 0.5)
    term1_2 = (1 - np.exp(-((x - d) / 2) ** 2)) / np.sqrt((x - d) ** 2 + 1/16)
    first_part = -0.5001 * (term1_1 + term1_2)
    
    # Second part of the equation (involving x + d)
    term2_1 = 2 * np.exp(-((x + d) / 2.551) ** 2) / np.sqrt((x + d) ** 2 + 0.5)
    term2_2 = (1 - np.exp(-((x + d) / 2) ** 2)) / np.sqrt((x + d) ** 2 + 1/16)
    second_part = -0.4999 * (term2_1 + term2_2)
    
    # Final result is the sum of both parts
    return first_part + second_part

x = np.linspace(-20,20,300)
potential = equation(x,0)
v_int = idea.interactions.softened_interaction(x)
system = idea.system.System(x,potential,v_int,electrons="uu")
#state = idea.methods.interacting.solve(system,k=0)


#plt.plot(x,idea.observables.density(system,state=state))
plt.plot(x,potential, label="potential")
plt.show()