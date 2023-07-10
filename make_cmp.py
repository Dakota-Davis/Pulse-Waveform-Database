import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

def plot_examples(colormaps):
    """
    Helper function to plot data with associated colormap.
    """
    np.random.seed(19680801)
    data = np.random.randn(30, 30)
    n = len(colormaps)
    fig, axs = plt.subplots(1, n, figsize=(n * 2 + 2, 3),
                            constrained_layout=True, squeeze=False)
    for [ax, cmap] in zip(axs.flat, colormaps):
        psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmin=-4, vmax=4)
        fig.colorbar(psm, ax=ax)
    #plt.show()
    


path = 'colormap.txt'

f = open(path)
N = f.readline()
#print(N)

colors = []
for line in f.readlines():
    l = line.rstrip()
    #print(l)
    line_arr = l.split(' ')  #makes array of strings
    #print(line_arr)
    
    del line_arr[0]
    colors.append(line_arr)  #makes color array
#print(colors)  
for color in colors:
    for c in range(len(color)):
        color[c] = float(color[c])      #makes rgb pixel intensity values floats
    color.append(1.)                    #adds in the opacity value for the Nx4 color matrix
#print(colors)
newcmp = ListedColormap(colors)
plot_examples([newcmp])