import pickle
import matplotlib.pyplot as plt
import numpy as np

file = open("doublestate.state", "rb")
state = pickle.load(file)

plt.imshow(state.real[:,0,:,0], cmap="seismic", vmax=0.75, vmin=-0.75, extent=[-20, 20, 20, -20], aspect=1)
plt.xlabel("x, position of electron 1 (Bohrs)")
plt.ylabel("x', poisition of electron 2 (Bohrs)")
plt.colorbar()
plt.title("Gaussian1 Double Excitation, Zoomed, Excitation 7")
plt.xlim([-5,5])
plt.ylim([-5,5])
plt.show()
plt.close()
