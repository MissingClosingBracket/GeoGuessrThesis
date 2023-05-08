import osmnx as ox
import geopandas as gpd
from helperFunctions import getDistance, makeGrid, placeInBoxes
from shapely.geometry import Point,mapping
import matplotlib.lines as lines
import matplotlib.pyplot as plt
import networkx as nx

#start here by defining area and grid size:
gridSize = (35,35)
guesses = 4
place = 'bornholm'
showGrid = False
showCenterPoints = False
showRegionBoxes = False
showConvexHullOfRegions = True
diagonalDirection = 'B'
simplifier = 2

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
            index = 0
            if diagonalDirection == 'A':
                index = j * width + i
            else:
                index = height + j * width - i - 1
            b = gridWithBoxes[index]
            #if b.totalWeight > 0:
            if b.inside:
                currWeight += b.totalWeight
                biggerBoxes[currBigBox].append(b)
                boxX = [[b.min_lat, b.max_lat, b.max_lat, b.min_lat,b.min_lat]]
                boxY = [[b.max_lon, b.max_lon, b.min_lon, b.min_lon,b.max_lon]]
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

fig, ax = ox.plot_graph(graph, show=False, close=False, node_size=4, figsize=(14,13))

#fetch the n subnetworks given by the convex hulls and find the node with the highest centrality score
for x in range(0, len(convexHullsForGuessAreas)):
    #show convex hull of the guess areas:
    if showConvexHullOfRegions:
        for x in range(0, len(convexHullsForGuessAreas)):
            x_data = [elem[0] for elem in mapping(convexHullsForGuessAreas[x])['coordinates'][0]]
            y_data = [elem[1] for elem in mapping(convexHullsForGuessAreas[x])['coordinates'][0]]
            ax.add_line(lines.Line2D(xdata=x_data,ydata=y_data,color=colors[x],linewidth=2, zorder=10000))

def sortLat(elem):
    return elem[0][0]
def sortLon(elem):
    return elem[0][1]

#can't use the nx.closeness_centrality, as it uses dijkstra's shortest path. 
#So, the Closeness Score is calculated manually. This manual approach has complexity N^2
#Besides, the points have to be weighted, so a manual approach with weighted haversine distance as dist is the only correct approach
#Bornholm:
    #(4485.555036377326, (14.75867745, 55.1797539))
    #(5419.95747443702, (14.89183065, 55.119337200000004))
    #(4311.480444962821, (15.06827895, 55.061246249999996))
#Malta:
    #(27498.939631886613, (14.3519672375, 35.9657817))
    #(11145.199262151133, (14.45627495, 35.8945337375))
    #(14340.606536047286, (14.510572087500002, 35.862443375))

finalGuesses = []

#Use simplifier for Malta due to comp. complexity.
for x in range(0, guesses):
    points = []

    for box in biggerBoxes[x]:
        if box.points != []:
            boxPoints = box.points
            boxPoints.sort(key=sortLat)
            boxPoints.sort(key=sortLon)
            for j in range(0, len(boxPoints), simplifier):
                to = j+simplifier
                if to > (len(boxPoints) - 1):
                    to = (len(boxPoints) - 1)
                collectedPoints = [boxPoints[k] for k in range(j, to)]
                weight = sum(elem[1] for elem in collectedPoints)
                lat = sum(elem[0][0] for elem in collectedPoints)/simplifier
                lon = sum(elem[0][1] for elem in collectedPoints)/simplifier
                points.append([(lat,lon),weight])

    centralityOfNodes = {}
    print(len(points))

    for i in range(len(points)):
        temp = 0
        for n in range(len(points)):
            temp += getDistance(points[i][0],(points[n][0])) * points[n][1]
        centralityOfNodes[temp] = points[i][0]

    sortedByTotalDist = dict(sorted(centralityOfNodes.items()))
    point = next(iter( sortedByTotalDist.items() ))
    finalGuesses.append(point[1])
    print(next(iter( sortedByTotalDist.items() )))



#Bornholm:
#lats = [14.75867745,14.89183065,15.06827895]
#lons = [55.1797539,55.119337200000004,55.061246249999996]

#Malta:
#lats = [14.3519672375,14.45627495,14.510572087500002]
#lons = [35.9657817,35.8945337375,35.862443375]

for x in range(0, len(finalGuesses)):
    ax.scatter(finalGuesses[x][0], finalGuesses[x][1], color=colors[x],s=100,zorder=1000)


#draw and show
plt.draw()
plt.show()

#1497329554
#5028013987
#4604043807