import numpy as np

class partition(object):
    def __init__(self, data, partitionsize = 10):
        self.data = data
        self.partitionsize = partitionsize
        self.npartitions = np.ceil(len(self.data) / self.partitionsize).astype(np.int32)

    def __getitem__(self, i):
        if i >= self.npartitions:
            raise IndexError("index out of range")
        return self.data[slice(i * self.partitionsize, (i + 1) * self.partitionsize)]

    def __setitem__(self, i, values):
        self.data[slice(i * self.partitionsize, (i + 1) * self.partitionsize)] = values

    def __len__(self):
        return self.npartitions