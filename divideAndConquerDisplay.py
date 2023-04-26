import osmnx as ox
import geopandas as gpd
from helperFunctions import getDistance, makeGrid, placeInBoxes
from shapely.geometry import Point,LineString,mapping
import matplotlib.lines as lines
import matplotlib.pyplot as plt
import statistics
import networkx as nx

#start here by defining area and grid size:
gridSize = (35,35)
guesses = 3
place = 'Bornholm'
showGrid = True
showCenterPoints = False
showMidpoints = False
showRegionBoxes = False
showConvexHullOfRegions = True

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

#make a grid of gridSize boxes that span the rectangle of the convex hull of the networks center points
#each grid box has a bounding box and will contain the total of weights and the points (points = edge representations)
node_points = [Point((data[0][0], data[0][1])) for data in centerPoints]
convexHull = gpd.GeoSeries(node_points).unary_union.convex_hull
grid = makeGrid(gridSize[0], gridSize[1], convexHull)

#run through the centerPoints and place them in the boxes
gridWithBoxes, totalWeight = placeInBoxes(centerPoints, grid, gridSize)

#plot graph, leave open
fig, ax = ox.plot_graph(graph, show=False, close=False, node_size=4, figsize=(14,13))

#show grid
if showGrid:
    for x in range(0, len(grid)):
        b = grid[x]
        boxX = [[b.min_lat, b.max_lat, b.max_lat, b.min_lat,b.min_lat]]
        boxY = [[b.max_lon, b.max_lon, b.min_lon, b.min_lon,b.max_lon]]
        ax.add_line(lines.Line2D(xdata=boxX,ydata=boxY,color='orange',linewidth=2,zorder=1000))

#run through the grid and collect boxes into n (n = number of guesses) bigger areas
queue = []
width = gridSize[0]
height = gridSize[1]

biggerBoxes = []

for x in range(0, guesses):
    biggerBoxes.append([])
currWeight = 0
currBigBox = 0
colors = ['yellow', 'purple', 'green', 'blue', 'orange']
for k in range (0, width + height - 1):
    for j in range(0, k+1):
        i = k-j
        if (i < height and j < width):
            index = height + j * width - i - 1
            if k < 5:
                print(index)
            b = gridWithBoxes[index]
            #if b.totalWeight > 0:
            if b.inside:
                currWeight += b.totalWeight
                biggerBoxes[currBigBox].append(b)
                boxX = [[b.min_lat, b.max_lat, b.max_lat, b.min_lat,b.min_lat]]
                boxY = [[b.max_lon, b.max_lon, b.min_lon, b.min_lon,b.max_lon]]
                if showRegionBoxes:
                    ax.add_line(lines.Line2D(xdata=boxX,ydata=boxY,color=colors[currBigBox],linewidth=2,zorder=1000))
                if currWeight >= totalWeight/guesses:
                    currWeight = 0
                    currBigBox += 1

#for n bigger box (n = # of guesses), make the convex hulls
convexHullsForGuessAreas = []
for x in range(0, guesses):
    points = []
    for box in biggerBoxes[x]:
        points.append(Point(box.min_lat,box.max_lon))
        points.append(Point(box.max_lat,box.max_lon))
        points.append(Point(box.max_lat,box.min_lon))
        points.append(Point(box.min_lat,box.min_lon))
    convexHullsForGuessAreas.append(gpd.GeoSeries(points).unary_union.convex_hull)

#show convex hull of the guess areas:
if showConvexHullOfRegions:
    for x in range(0, len(convexHullsForGuessAreas)):
        x_data = [elem[0] for elem in mapping(convexHullsForGuessAreas[x])['coordinates'][0]]
        y_data = [elem[1] for elem in mapping(convexHullsForGuessAreas[x])['coordinates'][0]]
        ax.add_line(lines.Line2D(xdata=x_data,ydata=y_data,color=colors[x],linewidth=2, zorder=10000))

#calculate the centroids (midpoints)
centroids = []
for x in range(0, len(convexHullsForGuessAreas)):
    centroids.append(convexHullsForGuessAreas[x].centroid)

#show centroids(midpoint) for the convex hulls of the areas
if showMidpoints:
    for x in range(0, len(centroids)):
        centroid = centroids[x]
        ax.scatter(centroid.x, centroid.y, color=colors[x],s=100,zorder=1000)

#show centerPoints
if showCenterPoints:
    centerPointsLat = [elem[0][0] for elem in centerPoints]
    centerPointsLon = [elem[0][1] for elem in centerPoints]
    ax.scatter(centerPointsLat, centerPointsLon, color="red",s=0.1,zorder=100)

#draw and show
plt.draw()
plt.show()