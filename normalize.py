import numpy as np
from multiprocessing import Pool

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
        return self.data[]

    def getChunks(self, nchunks=10):
        pass


class chunk(object):
    def __init__(self, data, chunksize = 10):
        self.data = data
        self.chunksize = chunksize
        self.nchunks = np.ceil(len(self.data) / self.chunksize)

