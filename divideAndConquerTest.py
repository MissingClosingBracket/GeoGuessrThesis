import osmnx as ox
import geopandas as gpd
from helperFunctions import getDistance, makeGrid, placeInBoxes
from shapely.geometry import Point
import statistics
import networkx as nx
from osmnx.utils_geo import sample_points
from helperFunctions import pointsToListOfLatAndLongs, getDistance, generate_random_point_within_convex_hull


#start here by defining area and grid size:
gridSize = (35,35)
guesses = 3
place = 'malta'
diagonalDirection = 'B'
iter = 100_000

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

#calculate the centroids (midpoints)
centroids = []
for x in range(0, len(convexHullsForGuessAreas)):
    centroids.append(convexHullsForGuessAreas[x].centroid)

#List of all guesses (dist to goal)
allGuessesDist = []
bestGuessesDist = []

#Run through i iterations and fill array
n_guesses = guesses
i = iter
calculatedGuesses = [[point.x for point in centroids],[point.y for point in centroids]]
randomGoal = pointsToListOfLatAndLongs(sample_points(graph,i))

for elem in range(0,i*n_guesses,n_guesses):
    dist = []
    goalI = int(elem / n_guesses)
    for x in range(0, n_guesses):
         dist.append(getDistance((calculatedGuesses[0][x], calculatedGuesses[1][x]), (randomGoal[0][goalI], randomGoal[1][goalI])))
    dist.sort()
    bestGuessesDist.append(dist[0])
    for d in dist:
        allGuessesDist.append(d)

#Get statistics
print("All guesses mean:                " + str(statistics.mean(allGuessesDist)))
print("All guesses standard deviation:  " + str(statistics.stdev(allGuessesDist)))
print("Best guesses mean:               " + str(statistics.mean(bestGuessesDist)))
print("Best guesses standard deviation: " + str(statistics.stdev(bestGuessesDist)))



