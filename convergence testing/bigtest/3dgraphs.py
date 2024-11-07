import numpy as np
import matplotlib.pyplot as plt

data = []

with open(f"3ddata20.txt","r") as file:
    arr = [line.strip().split()[-1].split(",")[1:] for line in file.readlines()]
    data.append(np.array(arr).astype(float))

exictations = []
xpoints = []
energy = []



for line in data[0]:
    exictations.append(line[1])
    xpoints.append(line[2])
    energy.append(line[4])



x = np.reshape(exictations, (11,20))
y = np.reshape(xpoints, (11,20))
z = np.reshape(energy, (11,20))

for i in range(0,len(z)):
    z[i] = z[i]-z[i][-1]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.contour3D(np.log10(x),y,z, 50, cmap='viridis')
ax.set_xlabel("Excitation number")
ax.set_ylabel("Points on the x-grid")
ax.set_zlabel("Energy difference")

plt.show()
