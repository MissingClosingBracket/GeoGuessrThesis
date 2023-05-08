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
import matplotlib.colors as mcolors

#start here by defining area and grid size:
guesses = 4
place = 'bornholm'

graph = nx.MultiGraph

#Get graph
if place != 'malta':
    graph :nx.MultiDiGraph = ox.load_graphml("GeoGuessrThesis/savedGraphs/bornholm.graphml")# + place + ".graphml")
else:
    graph1 = ox.load_graphml("GeoGuessrThesis/savedGraphs/" + place + "1.graphml")
    graph2 = ox.load_graphml("GeoGuessrThesis/savedGraphs/" + place + "2.graphml")
    graph3 = ox.load_graphml("GeoGuessrThesis/savedGraphs/" + place + "3.graphml")
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
kmeans = KMeans(n_clusters=guesses, init='k-means++', max_iter=1000)

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
    if c == 3:
        kmeans_clusters[3].append(centerPoints[x])
#display graph
cMap = plt.cm.get_cmap('inferno')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.axes.set_facecolor('black')

for c in range(0, len(kmeans_clusters)):
    color = cMap(0.3 + c*(1/guesses))
    cluster = kmeans.cluster_centers_[c]
    print(cluster)
    lats = [x[0][0] for x in kmeans_clusters[c]]
    lons = [x[0][1] for x in kmeans_clusters[c]]
    weights = [x[1] for x in kmeans_clusters[c]]
    ax.scatter(lats, lons, s=[x*1 for x in weights], color=color)
    ax.scatter(cluster[0], cluster[1], s=50, color='white')
    ax.scatter(cluster[0], cluster[1], s=25, color='blue')
    ax.scatter(cluster[0], cluster[1], s=5, color='black')

plt.show()

'''
Bornholm:
[14.76468147 55.15867943]
[14.92302334 55.1232714 ]
[15.07548271 55.06935343]

Malta:
[14.40612363 35.90931744]
[14.25970596 36.04257726]
[14.49667782 35.8727472 ]
'''