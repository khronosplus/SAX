import numpy as np
from scipy.stats import zscore
from partition import partition

from multiprocessing import Pool, freeze_support
NWORKERS = 1

class PAA(object):
    """
    calculates the piecewise aggregate approximation

    """
    def __init__(self, data=None, width=5, normalize=True):
        """
        :param data: numpy array that contains the time series
        :param width: size of the aggregate pieces
        :param normalize: if True time series will be z-normalized
        """
        self.result = None
        self.data = None
        self.setWidth(width)
        if data is not None:
            self.read(data, normalize=normalize)

    def setWidth(self, width):
        self.width = width
        if self.data is not None:
            self.partitions = partition(self.data, partitionsize=self.width)

    def read(self, data, normalize=True):
        if normalize:
            data = zscore(data)
        self.data = data
        self.partitions = partition(self.data, partitionsize=self.width)

    def calculate(self, nworkers=2):
        #with Pool(NWORKERS) as p:
        #    self.result = p.map(np.mean, self.pieces())
        self.result = list(map(np.mean, self.partitions))
        return self


class SAX(object):
    breakpointLookup = [
        [0.],
        [-0.43, 0.43],
        [-0.67, 0., 0.67],
        [-0.84, -0.25, 0.25, 0.87],
        [-0.97, -0.43, 0, 0.43, 0.97],
        [-1.07, -0.57, -0.18, 0.18, 0.57, 1.07],
        [-1.15, -0.67, -0.32, 0., 0.32, 0.67, 1.15],
    ]

    letters = 'abcdefgh'

    def __init__(self, paa, cardinality=4):
        self.result = None
        self.paa = paa
        self.setCardinality(cardinality)

    def setCardinality(self, c):
        if c < 2:
            c = 2
        if c > 8:
            raise Exception('Cardinality > 8 not implemented yet.')
        self.card = c

    def lookup(self, x):
        breakpoints = self.breakpointLookup[self.card - 2]
        for i, b in enumerate(breakpoints):
            if x < b:
                return self.letters[i]
        return self.letters[self.card-1]

    def calculate(self):
        #with Pool(NWORKERS) as p:
        #    self.result = p.map(self.lookup, self.paa.result)
        self.result = list(map(self.lookup, self.paa.result))
        return self