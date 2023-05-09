import osmnx as ox
from osmnx.plot import get_edge_colors_by_attr
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as nx
from helperFunctions import getDistance
import matplotlib.lines as lines

#Bornholm or malta?
#place = 'bornholm'
place = 'bornholm'

graph = nx.MultiGraph

#Get graph
if place != 'malta':
    graph :nx.MultiDiGraph = ox.load_graphml("./savedGraphs/" + place + ".graphml")
else:
    graph1 = ox.load_graphml("./savedGraphs/" + place + "1.graphml")
    graph2 = ox.load_graphml("./savedGraphs/" + place + "2.graphml")
    graph3 = ox.load_graphml("./savedGraphs/" + place + "3.graphml")
    graph = nx.compose_all([graph1, graph2, graph3])

#plot graph, leave open
fig, ax = ox.plot_graph(graph, show=False, close=False, node_size=4, figsize=(15,14))

latsDivAndConqB = []
lonsDivAndConqB = []

latsCC = []
lonsCC = []

if place == 'malta':
    latsDivAndConqB = [14.32273060014064,14.440365324283668,14.506093554225357]
    lonsDivAndConqB = [35.97752858544781,35.887654647406485,35.85191980177062]
    latsCC = [14.3519672375,14.45627495,14.510572087500002]
    lonsCC = [35.9657817,35.8945337375,35.862443375] 
else:
    latsDivAndConqB = [14.783184264343811,14.898766746598643,15.042076258215547]
    lonsDivAndConqB = [55.199481481214676,55.126100151650164,55.066863078283674]
    latsCC = [14.758691275,14.89146645,15.068693199999998]
    lonsCC = [55.168647375,55.116143,55.057020775]    

cMap = plt.cm.get_cmap('inferno')

for x in range(0, len(latsCC)):

    color1 = cMap(1-(x*0.1))
    color2 = cMap(0.95-(x*0.15))
    color3 = cMap(0.9-(x*0.2))

    guessDivAndConqB = (latsDivAndConqB[x], lonsDivAndConqB[x])
    guessCC = (latsCC[x], lonsCC[x])

    ax.scatter(guessDivAndConqB[0], guessDivAndConqB[1], color=color2,s=100,zorder=1000, label='Guess by Divide and Conquer B')
    ax.scatter(guessCC[0], guessCC[1], color=color3,s=100,zorder=1000,label='Guess by Closeness Centrality')

    dist = getDistance(guessDivAndConqB, guessCC)
    ax.add_line(lines.Line2D(xdata=[guessDivAndConqB[0],guessCC[0]],ydata=[guessDivAndConqB[1],guessCC[1]],color=color1,linewidth=2, zorder=100, label='Distance: ' + str(round(dist,3)) + 'km'))

#draw and show
ax.legend(loc="upper right")
plt.draw()
plt.show()
