import numpy as np
from sax import *
from matplotlib import pyplot as plt
from multiprocessing import Pool

# generate random time series
np.random.seed(1)
npoints = 100
x = list(range(npoints))
data = np.random.randn(npoints)
data = data.cumsum()

w = 10

paa = PAA(data, width=w, normalize=True).calculate()
paa_data = paa.result

sax = SAX(paa).calculate()
print(sax.result)

plt.plot(x, paa.data, 'b-')

for i, d in enumerate(paa_data):
    low  = i*w
    high = min(npoints-1, (i+1)*w)
    plt.plot([x[low], x[high]], [d, d], 'r-')

plt.show()
