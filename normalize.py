import numpy as np
from partition import partition
from multiprocessing import Pool


class normalize(object):
    """
    perform a parallel (MapReduce) z-normalization
    """
    def __init__(self, data=None, nworkers=2, partitionsize=10):
        self.nworkers = nworkers
        self.partitionsize = partitionsize
        self.params = None
        if data is not None:
            self.read(data)

    def read(self, data):
        self.data = data
        self.partition = partition(data, self.partitionsize)

    def getParams(self):
        res = (0, 0, 0)
        with Pool(self.nworkers) as p:
            for m in p.imap_unordered(self.getMeans, self.partition):
                res = self.addMeans(m, res)
        #means = list(map(self.getMeans, self.partition))

        self.params = (res[1], np.sqrt(res[2] - res[1]**2))
        return self.params

    def getMeans(self, data):
        return (len(data), np.mean(data), np.mean(data*data))

    @staticmethod
    def addMeans(a, b):
        # https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Parallel_algorithm
        m1 = (a[0] * a[1] + b[0] * b[1]) / (a[0] + b[0])
        m2 = (a[0] * a[2] + b[0] * b[2]) / (a[0] + b[0])
        return (a[0] + b[0], m1, m2)

    def calculate(self):
        if self.params is None:
            self.getParams()
        mean, std = self.params
        for i in range(len(self.partition)):
            self.partition[i] = (self.partition[i] - mean) / std
        return self


if __name__ == "__main__":
    dat = np.array(range(100))
    part = normalize(dat.astype(np.float64)).calculate()
    from scipy.stats import zscore
    assert( sum(zscore(dat) - part.data) == 0 )

