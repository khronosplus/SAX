from multiprocessing import Pool

import numpy as np


class normalize(object):
    """
    perform a parallel (MapReduce) z-normalization
    """
    def __init__(self, data=None, nworkers=2, chunksize=10):
        self.pool = Pool(nworkers)
        self.chunksize = chunksize
        if data is not None:
            self.read(data)

    def read(self, data):
        self.data = data
        self.nchunks = np.ceil( len(self.data) // self.chunksize )

    def getParams(self):
        with self.pool as p:
            p.map(self.getMeans, self.getChunks())

    def norm(self):
        pass

    def chunk(self, i):
        #return self.data[]
        pass

    def getChunks(self, nchunks=10):
        pass

    def getMeans(self):
        pass


