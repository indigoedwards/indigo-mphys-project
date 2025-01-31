import iDEA as idea
import glob
import numpy as np
import matplotlib.pyplot as plt 
import contextlib
from PIL import Image
import pickle


outputpath = "."
xgrid = np.linspace(-5,5,300)

def potential(distance):
    xgrid = np.linspace(-5,5,300)
    return (-4*np.exp(-((xgrid-distance)**2)/10) - 4.005*np.exp(-((xgrid+distance)**2)/10))

def yaxes_rerange(row_count, new_y_range):
    scale = (new_y_range[1] - new_y_range[0]) / row_count
    y_range = np.array([1, row_count - 1]) * scale

    dy = (y_range[1] - y_range[0]) / 2 - (new_y_range[1] - new_y_range[0])
    ext_y_range = y_range + new_y_range[0] + np.array([-dy, dy])
    extent = [-30, 30, 30, -30]

    aspect = 1

    return extent, aspect

def gif_wavefunctions(outputpath):
    #create gifs from saved plots
    fp_in = f"{outputpath}/wavefunctions/*.png"
    fp_out = f"{outputpath}/wavefunctions.gif"
    with contextlib.ExitStack() as stack:
        # lazily load images
        imgs = (stack.enter_context(Image.open(f))
                for f in sorted(glob.glob(fp_in)))
        # extract  first image from iterator
        img = next(imgs)
        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
        img.save(fp=fp_out, format='GIF', append_images=imgs,
                save_all=True, duration=300, loop=0)
    return
        
def gif_densities(outputpath):
    #create gifs from saved plots
    fp_in = f"{outputpath}/densities/*.png"
    fp_out = f"{outputpath}/densities.gif"
    with contextlib.ExitStack() as stack:
        # lazily load images
        imgs = (stack.enter_context(Image.open(f))
                for f in sorted(glob.glob(fp_in)))
        # extract  first image from iterator
        img = next(imgs)
        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
        img.save(fp=fp_out, format='GIF', append_images=imgs,
                save_all=True, duration=300, loop=0)
    return

def gif_innerproducts(outputpath):
    #create gifs from saved plots
    fp_in = f"{outputpath}/innerprods/*.png"
    fp_out = f"{outputpath}/innerproduct.gif"
    with contextlib.ExitStack() as stack:
        # lazily load images
        imgs = (stack.enter_context(Image.open(f))
                for f in sorted(glob.glob(fp_in)))
        # extract  first image from iterator
        img = next(imgs)
        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
        img.save(fp=fp_out, format='GIF', append_images=imgs,
                save_all=True, duration=300, loop=0)
    return

"""
gif_wavefunctions(outputpath)
gif_densities(outputpath)
gif_innerproducts(outputpath)


state = idea.state.load_many_body_state("doublestate")
data = state[:,0,:,0]

row_count = data.shape[0]
new_range = [-30,30]

extent, aspect = yaxes_rerange(row_count, new_range)

plt.imshow(data, cmap="seismic", vmax=0.75, vmin=-0.75, extent=extent, aspect=aspect)
plt.xlabel("x, position of electron 1 (Bohrs)")
plt.ylabel("x', poisition of electron 2 (Bohrs)")
plt.xlim([-10,10])
plt.ylim([-10,10])
plt.title(f"Doubly Excited State")

plt.show()
plt.close()

data = []
with open(f"energies.txt","r") as file:
        arr = [line.strip().split(",") for line in file.readlines()]
        data.append(np.array(arr,dtype=np.float64))
        data = data[0]

data = data.transpose()

plt.plot(data[0],data[2])
plt.gca().invert_xaxis()
plt.xlabel("Distance from origin (Bohrs)")
plt.ylabel("Energy of double excitation (Hartrees)")
plt.show()
"""


with open('potential.pkl', 'wb') as f:  # open a text file
    pickle.dump(potential(0), f) # serialize the list

plt.plot(xgrid,potential(0),linewidth=10)
plt.show()
