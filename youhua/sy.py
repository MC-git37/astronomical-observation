import numpy as np
import matplotlib.pyplot as plt
import os
from os.path import join
import imageio

fp = open(r'C:\Users\18234\Desktop\pendulum.txt')
dfile = fp.readlines()
data = []
for line in dfile:
    data.append(list(map(eval,line.split())))

fp.close()
data = np.array(data)
thetas = data[:,1]

def point(theta):
    r = 1.0
    fig = plt.figure()
    ax = fig.gca(projection='polar')
    ax.set_theta_zero_location('S')
    ax.set_rlim(0, 1.1)
    ax.plot((0, theta), (0, r), c='r')
    ax.scatter(theta, r, c='k', s=60)
    return fig

figpath ='./temp'
try:
    os.mkdir(figpath)
except FileExistsError:
    pass
for i,  theta in enumerate(thetas):
    fig = point(theta)
    figname = 'fig' + "%03d"%i + '.png'
    fig.savefig(join(figpath, figname), dpi=60)
    plt.close()

from imageio import imread
imagefiles = os.listdir(figpath)
images = []
for fig in imagefiles:
    im = imageio.imread(join(figpath, fig))
    images.append(im)
imageio.mimsave("images.gif", images, duration=0.1)