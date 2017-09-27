import numpy as np
import matplotlib as plt
import ephem

np.random.seed(0)    # To make reproducible the plot
nrand = np.random.rand(100,2)    # Array (100,2) of random values in [0,1)
nrand *= np.array([360.,180.]) # array in [0,360) x[0,180) range
nrand -= np.array([0,90.]) # array in [0,360)x[-90,90) range
nrand = nrand[(-86 < nrand[:,1]) & (nrand[:,1] < 86)] # To avoid Matplotlib Runtime Warning,
# staying far from the singularities at -90º and 90º
RA = nrand[:,0]
Dec = nrand[:,1]
plot_mwd(RA,Dec)