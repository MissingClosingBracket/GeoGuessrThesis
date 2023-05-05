import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_blobs
import seaborn as sns
import random
import osmnx as ox
from helperFunctions import getDistance
import networkx as nx
from sklearn.cluster import KMeans
import numpy as np

#start here by defining area and grid size:
guesses = 3
place = 'bornholm'
showGrid = False
showCenterPoints = False
showRegionBoxes = False
showConvexHullOfRegions = True

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


def weightedHaversine(point, data, reverseWeight = False):
    sumList = []
    if not reverseWeight:
        for d in data: 
            sumList.append(getDistance(point, d[0]) * d[1] ) 
    else:
        for d in data: 
            sumList.append(getDistance(point[0], d) * point[1]) 
    return sumList

#Thank you https://github.com/turnerluke/ML-algos/blob/main/k_means/k_means.py for inspiration.

class KMeans:

    def __init__(self, n_clusters=3, max_iter=100):
        self.n_clusters = n_clusters
        self.max_iter = max_iter

    def fit(self, weightedCenterPoints):
        centerPoints = [x[0] for x in nodes]
        self.centroids = [random.choice(centerPoints)]

        for _ in range(self.n_clusters-1):
            # Calculate distances from nodes to the centroids
            dists = np.sum([weightedHaversine(centroid, nodes) for centroid in self.centroids], axis=0)
            dists /= np.sum(dists)
            # Choose remaining nodes based on their distances
            new_centroid_index = np.random.choice(range(len(centerPoints)), size=1, p=dists)[0]
            self.centroids += [centerPoints[new_centroid_index]]

        iteration = 0
        while iteration < self.max_iter:
            # Sort each node, assigning to nearest centroid
            sorted_points = [[] for _ in range(self.n_clusters)]
            for x in nodes:
                dists = weightedHaversine(x, self.centroids, True)
                centroid_index = np.argmin(dists)
                sorted_points[centroid_index].append(x[0])

            # Push current centroids to previous, reassign centroids as mean of the nodes belonging to them
            prev_centroids = self.centroids
            self.centroids = [np.mean(cluster, axis=0) for cluster in sorted_points]
            for i, centroid in enumerate(self.centroids):
                if np.isnan(centroid).any():  # Catch any np.nans, resulting from a centroid having no nodes
                    self.centroids[i] = prev_centroids[i]
            iteration += 1

    def evaluate(self, X):
        centroids = []
        centroid_indexes = []
        for x in X:
            dists = weightedHaversine(x, self.centroids, True)
            centroid_index = np.argmin(dists)
            centroids.append(self.centroids[centroid_index])
            centroid_indexes.append(centroid_index)

        return centroids, centroid_indexes


# Create a dataset of 2D distributions
centers = 3
nodes = centerPoints

# Fit centroids to dataset
kmeans = KMeans(n_clusters=centers)
kmeans.fit(nodes)

# View results
centroidForNodeIndex, centroidIndexForNode = kmeans.evaluate(nodes)

#append the center points of each cluster into array
kmeans_clusters = []
kmeans_cluster_centroids = []
for x in range(0, guesses):
    kmeans_clusters.append([])
    kmeans_cluster_centroids.append([])

for x in range (0, len(centroidIndexForNode)):
    c = centroidIndexForNode[x]
    if c == 0:
        kmeans_clusters[0].append(centerPoints[x])
        kmeans_cluster_centroids[0] = centroidForNodeIndex[x]
    if c == 1:
        kmeans_clusters[1].append(centerPoints[x])
        kmeans_cluster_centroids[1] = centroidForNodeIndex[x]
    if c == 2:
        kmeans_clusters[2].append(centerPoints[x])
        kmeans_cluster_centroids[2] = centroidForNodeIndex[x]

#display graph
cMap = plt.cm.get_cmap('inferno')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.axes.set_facecolor('black')
for c in range(0, len(kmeans_clusters)):
    color = cMap(0.3 + c*(1/3))
    cluster_centroid = kmeans_cluster_centroids[c]
    lats = [x[0][0] for x in kmeans_clusters[c]]
    lons = [x[0][1] for x in kmeans_clusters[c]]
    weights = [x[1] for x in kmeans_clusters[c]]
    ax.scatter(lats, lons, s=[x*5 for x in weights], color=color)
    ax.scatter(cluster_centroid[0], cluster_centroid[1], s=50, color='white')
    ax.scatter(cluster_centroid[0], cluster_centroid[1], s=25, color='blue')
    ax.scatter(cluster_centroid[0], cluster_centroid[1], s=5, color='black')

plt.show()