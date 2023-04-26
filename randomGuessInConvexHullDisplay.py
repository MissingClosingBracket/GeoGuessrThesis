import osmnx as ox
from osmnx.plot import get_edge_colors_by_attr
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from osmnx.utils_geo import sample_points
import matplotlib.lines as lines
import networkx as nx
import geopandas as gpd
from helperFunctions import pointsToListOfLatAndLongs, getNearestNode, FakeDoubleClickEvent, generate_random_point_within_convex_hull
import matplotlib.lines as lines
from shapely.geometry import Point,mapping

place = 'malta'

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

#get edges and map with color dep. on length
edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)
edges_series = edges['length']
edges[['osmid','length']]
ec = get_edge_colors_by_attr(graph, attr='length')

#get bounding_poly for convex hull
node_points = [Point((data["x"], data["y"])) for node, data in graph.nodes(data=True)]
convexHull = gpd.GeoSeries(node_points).unary_union.convex_hull
convexX = [elem[0] for elem in mapping(convexHull)['coordinates'][0]]
convexY = [elem[1] for elem in mapping(convexHull)['coordinates'][0]]
convexHullLines = lines.Line2D(xdata=convexX,ydata=convexY,color="pink",linewidth=2,label='convex hull')

#plot graph, leave open
fig, ax = ox.plot_graph(graph, edge_color=ec, show=False, close=False, node_size=4, figsize=(14,13))

#make color map label
norm=plt.Normalize(vmin=edges['length'].min(), vmax=edges['length'].max())
cmap = plt.cm.get_cmap('viridis')
cb = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap,), ax=ax, orientation='horizontal',fraction=0.026, pad=0.02)
cb.set_label('edge length [m]', fontsize = 10)

#define list of displayObjects
displayObjects = []

#remove old displayObjects
def removeTemp():
    for displayObject in displayObjects:
        displayObject.remove()
    displayObjects.clear()    

def onclick(event):
    if event.dblclick==True:
        graph.graph['crs'] = "epsg:3857"
        randomGuesses = pointsToListOfLatAndLongs(generate_random_point_within_convex_hull(3, convexHull))
        randomGoal = pointsToListOfLatAndLongs(sample_points(graph,1))
        nearestDist, nearestNode = getNearestNode(randomGuesses,randomGoal)
        graph.graph['crs'] = "epsg:4326"

        removeTemp()
        displayObjects.append(ax.scatter(randomGuesses[0], randomGuesses[1], color="white",s=100,zorder=10))
        displayObjects.append(ax.scatter(randomGuesses[0], randomGuesses[1], color="blue", label="random guess",s=50,zorder=11))
        displayObjects.append(ax.scatter(randomGuesses[0], randomGuesses[1], color="black",s=10,zorder=12))
        displayObjects.append(ax.scatter(randomGoal[0], randomGoal[1], color="white",s=100,zorder=10))
        displayObjects.append(ax.scatter(randomGoal[0], randomGoal[1], color="yellow", label="target",s=50,zorder=11))
        displayObjects.append(ax.scatter(randomGoal[0], randomGoal[1], color="black",s=10,zorder=12))
        displayObjects.append(ax.scatter(nearestNode[0], nearestNode[1], color="white",s=100,zorder=10))
        displayObjects.append(ax.scatter(nearestNode[0], nearestNode[1], color="lightgreen", label="closest random guess",s=50,zorder=11))
        displayObjects.append(ax.scatter(nearestNode[0], nearestNode[1], color="black",s=10,zorder=12))
        displayObjects.append(ax.add_line(lines.Line2D(xdata=[nearestNode[0], randomGoal[0][0]],ydata=[nearestNode[1],randomGoal[1][0]],color="white",linewidth=2,label='distance: ' + str(round(nearestDist,2)) + 'km')))
        displayObjects.append(ax.add_line(convexHullLines))
        ax.legend(loc="upper left")
        plt.draw()

#show plot and bind + simulate  doubleclick
ax.figure.canvas.mpl_connect('button_press_event',onclick) 
fm = plt.get_current_fig_manager()
fm.window.wm_geometry("+0+0")
fm.set_window_title("Bornholm")
onclick(FakeDoubleClickEvent())
plt.show()
