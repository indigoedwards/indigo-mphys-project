#testfile

import iDEA as idea
import numpy as np

x = np.linspace(-30,30,300)
v_ext = np.ones(300)
v_int = idea.interactions.softened_interaction(x)

system = idea.system.System(x,v_ext,v_int,electrons="uu")

print(system.dx)
