import numpy as np
import os, json, requests
from Cluster import Cluster
from scipy.spatial import ConvexHull
import boto3
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.nonparametric.smoothers_lowess as smoothlowess
import subprocess

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

dbscluster = Cluster(locations, min_cluster_size=3)
data = dbscluster.data_set

print("Running DBSCAN on data set...")
dbscluster.dbscan(eps=1.0e-06, min_samples=5)
dbscanClusters = dbscluster.cluster
clusterLists = dbscluster.getClusterLists()

num_clusters = len(set(dbscanClusters.labels_))
print("{} clusters found".format(num_clusters))

clusterDetails = dbscluster.getClusterDetails()

csv = open('clusters-csv', 'w')
csv.write('lat,long,cluster\n')
for cluster in clusterDetails:
    points = clusterDetails[cluster]['points']
    for point in points:
        if cluster is not None and point is not None:
            csv.write("{},{},{}\n".format(point[0], point[1], cluster))


clusterFile = open('clusters', 'w')

jDump = json.dumps(clusterDetails)
clusterFile.write(jDump)
s3ClusterResp = S3.Bucket('crowdmapper').put_object(Key='clusters', Body=jDump)

# dbscluster.showClusterPoints()
# dbscluster.showClusterHull()
# dbscluster.fitLineToCluster('8')

x = subprocess.check_output('rscript principal_curve.R', shell=True)
curvesFile = open('curves.csv', 'r')

# Upload curves data to S3
s3CurvesResp = S3.Bucket('crowdmapper').put_object(Key='curves.csv', Body=curvesFile.read())
