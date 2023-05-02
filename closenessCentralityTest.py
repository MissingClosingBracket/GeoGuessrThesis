import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point
import statistics
import networkx as nx
from osmnx.utils_geo import sample_points
from helperFunctions import pointsToListOfLatAndLongs, getDistance


#start here by defining area and grid size:
gridSize = (35,35)
guesses = 3
place = 'malta'
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

#Guesses retrieved from /closenessCentralityDisplay
lats = []
lons = []
if place == 'bornholm':
    lats = [14.75867745,14.89183065,15.06827895]
    lons = [55.1797539,55.119337200000004,55.061246249999996]
else:
    lats = [14.3519672375,14.45627495,14.510572087500002]
    lons = [35.9657817,35.8945337375,35.862443375]

#List of all guesses (dist to goal)
allGuessesDist = []
bestGuessesDist = []

#Run through i iterations and fill array
n_guesses = guesses
i = iter
calculatedGuesses = [lats,lons]
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



