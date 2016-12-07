import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial import ConvexHull

class Cluster():
    def __init__(self, locations):
        self.data_set = self.generateDataSet(locations)
        self.cluster = None

    def generateDataSet(self, locations):
        data = []
        for i, location in enumerate(locations):
            lat = location.get('lat')
            long = location.get('long')
            if lat is None or long is None:
                raise LookupError('Location item at index {} invalid'.format(i))
            data.append([
                float("{0:.7f}".format(lat)),
                float("{0:.7f}".format(long))
            ])
        data = np.array(data)
        uniqueData = {arr.tostring(): arr for arr in data}.values()
        return np.array(uniqueData)

    def dbscan(self, eps=0.3, min_samples=None):
        # TODO: implement
        db = DBSCAN(eps, min_samples, n_jobs=2, algorithm='ball_tree', metric='haversine').fit(np.radians(self.data_set))
        self.cluster = db

    def getClusterLists(self):
        clusterDict = {}
        for i, cluster in enumerate(self.cluster.labels_):
            if cluster != -1:
                if cluster not in clusterDict:
                    clusterDict[cluster] = []
                clusterDict[cluster].append(i)
        return clusterDict

    def getPoint(self, index):
        return self.data_set[index].tolist()

    def getClusterHull(self, clusterPoints):
        data = [self.data_set[i] for i in clusterPoints]
        points = [self.getPoint(coord) for coord in ConvexHull(data).vertices]
        return points

    def getClusterDetails(self):
        clusterDict = self.getClusterLists()
        detailedClusterDict = {}

        for cluster in clusterDict:
            detailedClusterDict[cluster] = {}
            detailedClusterDict[cluster]["points"] = [self.getPoint(ind) for ind in clusterDict[cluster]]
            detailedClusterDict[cluster]["hull"] = self.getClusterHull(clusterDict[cluster])

        for key in detailedClusterDict.keys():
            if type(key) is not str:
                try:
                    detailedClusterDict[str(key)] = detailedClusterDict[key]
                except:
                    try:
                        detailedClusterDict[repr(key)] = detailedClusterDict[key]
                    except:
                        pass
            del detailedClusterDict[key]

        return detailedClusterDict
