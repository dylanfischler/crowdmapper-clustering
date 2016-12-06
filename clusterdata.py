import numpy as np
import os, json
from Cluster import Cluster
import matplotlib.pyplot as plt

DATA_FILE = 'data/locations.json'

def processDataFile():
    global DATA_FILE
    print("Processing data file...")
    data_file = open(DATA_FILE, 'r')
    return json.loads(data_file.read())

locations = processDataFile()
clusterInstance = Cluster(locations)
print("Running DBSCAN on data set...")
dbscanClusters = clusterInstance.dbscan(eps=0.000006, min_samples=5)
clusters = set(dbscanClusters.labels_)
print("{} clusters found".format(len(clusters)))
print(clusters)

clusterFile = open('clusters', 'w')
clusterFile.write(json.dumps(dbscanClusters.labels_.tolist()))

# display all points on a plot
plt.scatter(clusterInstance.data_set[:,0], clusterInstance.data_set[:,1])
plt.show()