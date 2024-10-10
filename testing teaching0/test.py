import numpy as np
import iDEA as idea

atom = idea.system.systems.atom
groundstate = idea.methods.interacting.solve(atom, k=0)
print(groundstate.space.shape)
