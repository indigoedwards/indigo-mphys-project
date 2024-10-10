import numpy as np
import iDEA as idea
import matplotlib.pyplot as plt

atom = idea.system.systems.atom
groundstate = idea.methods.interacting.solve(atom, k=0)
print(groundstate.space.shape)

plt.plot(atom.x, groundstate.space.real)
plt.savefig("test.png")

