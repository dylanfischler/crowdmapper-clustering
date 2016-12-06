import numpy as np
import os, json
from Cluster import Cluster
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

DATA_FILE = 'data/locations.json'

def processDataFile():
    global DATA_FILE
    print("Processing data file...")
    data_file = open(DATA_FILE, 'r')
    return json.loads(data_file.read())

locations = processDataFile()
dbscluster = Cluster(locations)
data = dbscluster.data_set

print("Running DBSCAN on data set...")
dbscluster.dbscan(eps=0.000006, min_samples=5)
dbscanClusters = dbscluster.cluster
clusterLists = dbscluster.getClusterLists()

num_clusters = len(set(dbscanClusters.labels_))
print("{} clusters found".format(num_clusters))

clusterDetails = dbscluster.getClusterDetails()

# plt.scatter(clusterInstance.data_set[:,0], clusterInstance.data_set[:,1])
# hull = ConvexHull(clusterInstance.data_set)
# clusters = [data[dbscanClusters.labels_ == i] for i in xrange(len(dbscanClusters.labels_))]
# print(clusters)
#
# plt.plot(data[:,0], data[:,1], 'o')
# for simplex in hull.simplices:
#     plt.plot(data[simplex, 0], data[simplex, 1], 'k-')
# plt.show()
#
clusterFile = open('clusters', 'w')
clusterFile.write(json.dumps(clusterDetails))