# plot all sources in ATNF PSR catalogue


import matplotlib.pyplot as plt
import numpy as np
import psrcat as pc

cat = pc.PSRCAT('data/psrcat.db')
raj, decj = zip(*[x['JCOORD_RAD'] for x in cat.blocks])

plt.figure()
plt.title('ANTF Catalogue')
plt.plot(raj, decj, '.')
plt.xlabel('Right Ascension (rad)')
plt.ylabel('Declination (rad)')
plt.show()