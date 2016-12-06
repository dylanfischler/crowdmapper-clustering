import numpy as np
from sklearn.cluster import DBSCAN


class Cluster():
    def __init__(self, locations):
        self.data_set = self.generateDataSet(locations)

    def generateDataSet(self, locations):
        data = []
        for i, location in enumerate(locations):
            lat = location.get('lat')
            long = location.get('long')
            if lat is None or long is None:
                raise LookupError('Location item at index {} invalid'.format(i))
            data.append([lat, long])
        return np.array(data)

    def dbscan(self, eps=0.3, min_samples=None):
        # TODO: implement
        db = DBSCAN(eps, min_samples, n_jobs=2, algorithm='ball_tree', metric='haversine').fit(np.radians(self.data_set))
        return db
