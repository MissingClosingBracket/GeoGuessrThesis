import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point,LineString,mapping
import matplotlib.lines as lines
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.cluster import KMeans
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.colors as mcolors
from osmnx.utils_geo import sample_points
from helperFunctions import pointsToListOfLatAndLongs

#start here by defining area and grid size:
guesses = 3
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
        centerPoint = (
            (coords[x][0] + coords[x+1][0])/2.0, 
            (coords[x][1] + coords[x+1][1])/2.0
            )
        centerPoints.append([centerPoint, 0.1])

#place 10 parcel lockers and 10 companies randomly
parcelLockers = pointsToListOfLatAndLongs(sample_points(graph, 10))
companies = pointsToListOfLatAndLongs(sample_points(graph, 10))

for x in range(0, 10):
    #parcelLocker, weight 1000
    centerPoints.append(((parcelLockers[0][x], parcelLockers[1][x]), 1000))
    #company weight 500
    centerPoints.append(((companies[0][x], companies[1][x]), 500))

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
    kmeans_clusters[c].append(centerPoints[x])

#display graph
cMap = plt.cm.get_cmap('inferno')

fig = plt.figure(figsize=(11,10))
ax = fig.add_subplot(111)
ax.axes.set_facecolor('black')

for c in range(0, len(kmeans_clusters)):
    color = cMap(0.9-(c*0.1))
    cluster = kmeans.cluster_centers_[c]
    print(cluster)
    lats = [x[0][0] for x in kmeans_clusters[c]]
    lons = [x[0][1] for x in kmeans_clusters[c]]
    weights = [x[1] for x in kmeans_clusters[c]]
    ax.scatter(lats, lons, s=0.8, color=color)
    ax.scatter(cluster[0], cluster[1], s=50, color='blue')
ax.scatter(kmeans.cluster_centers_[0][0], kmeans.cluster_centers_[0][1], s=50, color='blue', label="Warehouse")

#plot companies and parcel lockers
ax.scatter(parcelLockers[0], parcelLockers[1], s=30, color='white', label="Parcel locker/shop")
ax.scatter(companies[0], companies[1], s=30, color='red', label="Company")

plt.legend(loc="upper right")
plt.show()
