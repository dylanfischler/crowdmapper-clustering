import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import statsmodels.nonparametric.smoothers_lowess as ls
import scipy.interpolate as interpolate

class Cluster():
    def __init__(self, locations, min_cluster_size):
        self.data_set = self.generateDataSet(locations)
        self.cluster = None
        self.min_cluster_size = min_cluster_size

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

    # def getClusterHull(self, clusterPoints):
    #     data = [self.data_set[i] for i in clusterPoints]
    #     hull = ConvexHull(data)
    #     points = [data[coord].tolist() for coord in hull.vertices]
    #     return points

    def getClusterDetails(self):
        clusterDict = self.getClusterLists()
        detailedClusterDict = {}

        for cluster in clusterDict:
            if(len(clusterDict[cluster]) >= self.min_cluster_size):
                detailedClusterDict[cluster] = {}
                detailedClusterDict[cluster]["points"] = [self.getPoint(ind) for ind in clusterDict[cluster]]
                # detailedClusterDict[cluster]["hull"] = self.getClusterHull(clusterDict[cluster])

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

    def showClusterPoints(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        details = self.getClusterDetails()

        for cluster in details:
            points = np.array(details[cluster]['points'])
            plt.plot(points[:, 0], points[:, 1], 'o')
            for i, j in zip(points[:, 0], points[:, 1]):
                ax.annotate(cluster, xy=(i, j), xytext=(30, 0), textcoords="offset points")
        plt.show(block=True)

    # def showClusterHull(self):
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111)
    #     details = self.getClusterDetails()
    #
    #     for cluster in details:
    #         points = np.array(details[cluster]['hull'])
    #         plt.plot(points[:, 0], points[:, 1], 'o')
    #         for i, j in zip(points[:,0], points[:,1]):
    #             ax.annotate(cluster, xy=(i, j), xytext=(30, 0), textcoords="offset points")
    #     plt.show(block=True)
