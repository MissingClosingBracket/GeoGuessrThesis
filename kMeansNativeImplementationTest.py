import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point
import statistics
import networkx as nx
from osmnx.utils_geo import sample_points
from helperFunctions import pointsToListOfLatAndLongs, getDistance


#start here by defining area and grid size:
guesses = 3
place = 'bornholm'
iter = 100_000
figure = 4

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

#Guesses retrieved from /kMeansNativeImplementationDisplay
lats = []
lons = []
if figure == 1:
    lats = [15.09326399,14.75630571,14.93193358]
    lons = [55.069379  ,55.16436464,55.12544893]
if figure == 2:
    lats = [14.87214877,14.73385731,15.07445816]
    lons = [55.17642594,55.13536979,55.0730405]
if figure == 3:
    lats = [15.03892314,14.74238445,14.82660274]
    lons = [55.08498103,55.11902821,55.22584935]
if figure == 4: 
    lats = [15.04753265,14.84824166,14.74098452]
    lons = [55.07499334,55.21754682,55.12120944]

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

'''
1tl)[array([15.09326399, 55.069379  ]), array([14.75630571, 55.16436464]), array([14.93193358, 55.12544893])]
	All guesses mean:                20.056736322549238
	All guesses standard deviation:  12.082757382260755
	Best guesses mean:               7.51676611842859
	Best guesses standard deviation: 2.963992984026723

2tr)[array([14.87214877, 55.17642594]), array([14.73385731, 55.13536979]), array([15.07445816, 55.0730405 ])]
	All guesses mean:                20.192327090811684
	All guesses standard deviation:  12.096187262974663
	Best guesses mean:               7.782659836657344
	Best guesses standard deviation: 3.4782923793631597

3bl)[array([15.03892314, 55.08498103]), array([14.74238445, 55.11902821]), array([14.82660274, 55.22584935])]
	All guesses mean:                20.213539189054654
	All guesses standard deviation:  11.695105667720426
	Best guesses mean:               8.069971808569976
	Best guesses standard deviation: 3.6290515811390716

4br)[array([15.04753265, 55.07499334]), array([14.84824166, 55.21754682]), array([14.74098452, 55.12120944])]
	All guesses mean:                20.14228788278985
	All guesses standard deviation:  11.656526868474101
	Best guesses mean:               7.988933225318553
	Best guesses standard deviation: 3.588523922786146
'''