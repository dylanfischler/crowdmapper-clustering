import numpy as np
import os, json, requests
from Cluster import Cluster
from scipy.spatial import ConvexHull
import boto3

S3 = boto3.resource('s3')

# DATA_FILE = 'data/locations.json'
#
# def processDataFile():
#     global DATA_FILE
#     print("Processing data file...")
#     data_file = open(DATA_FILE, 'r')
#     return json.loads(data_file.read())
#
# locations = processDataFile()

api = requests.get("http://crowdmapper.dylanfischler.com:8080/api/location")
locations = json.loads(api.content)

dbscluster = Cluster(locations)
data = dbscluster.data_set

print("Running DBSCAN on data set...")
dbscluster.dbscan(eps=5.0e-08, min_samples=5)
dbscanClusters = dbscluster.cluster
clusterLists = dbscluster.getClusterLists()

num_clusters = len(set(dbscanClusters.labels_))
print("{} clusters found".format(num_clusters))

clusterDetails = dbscluster.getClusterDetails()


clusterFile = open('clusters', 'w')

jDump = json.dumps(clusterDetails)
clusterFile.write(jDump)
s3Response = S3.Bucket('crowdmapper').put_object(Key='clusters', Body=jDump)