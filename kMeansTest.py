import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point
import statistics
import networkx as nx
from osmnx.utils_geo import sample_points
from helperFunctions import pointsToListOfLatAndLongs, getDistance


#start here by defining area and grid size:
guesses = 3
place = 'malta'
iter = 100_000

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

#Guesses retrieved from /kMeansDisplay
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
lats = []
lons = []

if place == 'bornholm':
    lats = [14.76468147,14.92302334,15.07548271]
    lons = [55.15867943,55.1232714,55.06935343]
else:
    lats = [14.40612363,14.25970596,14.49667782]
    lons = [35.90931744,36.04257726,35.8727472]

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