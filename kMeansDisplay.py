import osmnx as ox
import geopandas as gpd
from helperFunctions import getDistance, makeGrid, placeInBoxes, Box
from shapely.geometry import Point,LineString,mapping
import matplotlib.lines as lines
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.cluster import KMeans
import seaborn as sns
import numpy as np
import pandas as pd

#start here by defining area and grid size:
gridSize = (35,35)
guesses = 3
place = 'bornholm'
showGrid = False
showCenterPoints = False
showRegionBoxes = False
showConvexHullOfRegions = True
diagonalDirection = 'B'

graph = nx.MultiGraph

#Get graph
if place != 'malta':
    graph :nx.MultiDiGraph = ox.load_graphml("./savedGraphs/" + place + ".graphml")
else:
    graph1 = ox.load_graphml("./savedGraphs/" + place + "1.graphml")
    graph2 = ox.load_graphml("./savedGraphs/" + place + "2.graphml")
    graph3 = ox.load_graphml("./savedGraphs/" + place + "3.graphml")
    graph :nx.MultiGraph = nx.compose_all([graph1, graph2, graph3])

graph = graph.to_undirected()

#get edges and their length
edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)

#define empty array that will contain centerpoint, distance (weight) for every edge
centerPoints = []

#iterate through edges
for index, row in edges.iterrows():

    #get the points for each edge
    coords = [(coords) for coords in (row['geometry'].coords)]

    #get pairs of points for each edge (in many cases an edge is a collection of points)
        #possible "optimization": just use first and last node -> however, this will lead to a bigger uncertainty... 
        #for i.e. an entire big country using all edges is maybe not viable. Easily implement code-change here.
    #after that, calculate the distance (km) and get the center of the two points
    length = len(coords)
    for x in range(0, length-1):
        distance = getDistance(coords[x], coords[x+1])
        centerPoint = (
            (coords[x][0] + coords[x+1][0])/2.0, 
            (coords[x][1] + coords[x+1][1])/2.0
            )
        centerPoints.append([centerPoint, distance])

#define the number of clusers and number of initial centroid placements (n_init)
kmeans = KMeans(n_clusters=guesses, n_init=10, random_state=1234, max_iter=1000)

#make the weighted kmeans fit
weightedClusterFit = kmeans.fit([x[0] for x in centerPoints],sample_weight = [x[1] for x in centerPoints])
predicted_kmeans = kmeans.predict([x[0] for x in centerPoints],sample_weight = [x[1] for x in centerPoints])

#append the center points of each cluster into array
kmeans_clusters = []
for x in range(0, guesses):
    kmeans_clusters.append([])

for x in range (0, len(predicted_kmeans)):
    c = predicted_kmeans[x]
    if c == 0:
        kmeans_clusters[0].append(centerPoints[x])
    if c == 1:
        kmeans_clusters[1].append(centerPoints[x])
    if c == 2:
        kmeans_clusters[2].append(centerPoints[x])

#display graph
fig = plt.figure()
ax = fig.add_subplot(111)


for cluster in kmeans_clusters:
    lats = [x[0][0] for x in cluster]
    lons = [x[0][1] for x in cluster]
    weights = [x[1] for x in cluster]
    ax.scatter(lats, lons, s=[x*10 for x in weights], cmap='viridis')

plt.show()