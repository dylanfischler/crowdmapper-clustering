import numpy as np
import os, json
from Cluster import Cluster

DATA_FILE = 'data/locations.json'

def processDataFile():
    global DATA_FILE
    print("Processing data file...")
    data_file = open(DATA_FILE, 'r')
    return json.loads(data_file.read())

locations = processDataFile()
clusterInstance = Cluster(locations)
clusters = clusterInstance.dbscan()
