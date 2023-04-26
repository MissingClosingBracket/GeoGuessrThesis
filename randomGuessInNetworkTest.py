import osmnx as ox
from osmnx.utils_geo import sample_points
from helperFunctions import pointsToListOfLatAndLongs, getDistance
import networkx as nx
import statistics

place = 'malta'

graph = nx.MultiGraph

#Get graph
if place != 'malta':
    graph = ox.load_graphml("./savedGraphs/" + place + ".graphml")
else:
    graph1 = ox.load_graphml("./savedGraphs/" + place + "1.graphml")
    graph2 = ox.load_graphml("./savedGraphs/" + place + "2.graphml")
    graph3 = ox.load_graphml("./savedGraphs/" + place + "3.graphml")
    graph = nx.compose_all([graph1, graph2, graph3])

graph = graph.to_undirected()
graph.graph['crs'] = "epsg:3857"

#List of best guesses (dist to goal)
bestGuessesDist = []

#List of all guesses (dist to goal)
allGuessesDist = []
bestGuessesDist = []

#Run through i iterations and fill array
i = 100_000
n_guesses = 3
randomGuesses = pointsToListOfLatAndLongs(sample_points(graph,n_guesses*i))
randomGoal = pointsToListOfLatAndLongs(sample_points(graph,i))

for elem in range(0,i*n_guesses,n_guesses):
    dist = []
    goalI = int(elem / n_guesses)
    for x in range(0, n_guesses):
        dist.append(getDistance((randomGuesses[0][elem+x], randomGuesses[1][elem+x]), (randomGoal[0][goalI], randomGoal[1][goalI])))
    dist.sort()
    bestGuessesDist.append(dist[0])
    for d in dist:
        allGuessesDist.append(d)

#Get statistics
print("All guesses mean:                " + str(statistics.mean(allGuessesDist)))
print("All guesses standard deviation:  " + str(statistics.stdev(allGuessesDist)))
print("Best guesses mean:               " + str(statistics.mean(bestGuessesDist)))
print("Best guesses standard deviation: " + str(statistics.stdev(bestGuessesDist)))