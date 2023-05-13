import osmnx as ox
import geopandas as gpd
from helperFunctions import getDistance, makeGrid, placeInBoxes
from shapely.geometry import Point,mapping
import matplotlib.lines as lines
import matplotlib.pyplot as plt
import networkx as nx

#start here by defining area and grid size:

place = 'bornholm'
simplifier = 5

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

print(len(centerPoints))
#make a grid of gridSize boxes that span the rectangle of the convex hull of the networks center points
#each grid box has a bounding box and will contain the total of weights and the points (points = edge representations)
node_points = [Point((data[0][0], data[0][1])) for data in centerPoints]

def sortLat(elem):
    return elem[0][0]
def sortLon(elem):
    return elem[0][1]

centerPoints.sort(key=sortLat)
centerPoints.sort(key=sortLon)

#Use simplifier for Malta due to comp. complexity.
points = []
for j in range(0, len(centerPoints), simplifier):
                to = j+simplifier
                islast=0
                if to > (len(centerPoints) - 1):
                    to = (len(centerPoints) - 1)
                    simplifier = to-j #last 
                collectedPoints = [centerPoints[k] for k in range(j, to)]
                lat = sum(elem[0][0] for elem in collectedPoints)/(simplifier)
                lon = sum(elem[0][1] for elem in collectedPoints)/(simplifier)
                points.append((lat,lon))

print(len(points))

max_dist = 0 #km
nodes = ()

for x in points:
      for y in points:
            if (getDistance(x,y) > max_dist):
                  max_dist = getDistance(x,y)
                  nodes = (x,y)

print(max_dist)
print(nodes)

fig, ax = ox.plot_graph(graph, show=False, close=False, node_size=4, figsize=(13,12))

ax.scatter([x[0] for x in nodes], [y[1] for y in nodes], color='purple',s=100,zorder=1000)
ax.add_line(lines.Line2D(xdata=[x[0] for x in nodes],ydata=[y[1] for y in nodes],color="pink",linewidth=2,label='Distance: ' + str(round(max_dist,2)) + 'km'))

#draw and show
ax.legend(loc="upper right")
plt.draw()
plt.show()

#Bornholm:((15.12845159375, 55.06021289375), (14.71319220625, 55.222993624999994)) -> 49.39168946948267km
#Malta: ((14.531639379999998, 35.809913025), (14.202205349999996, 36.070482760000004)) -> 46.16277106066941