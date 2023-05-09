import osmnx as ox
from osmnx.plot import get_edge_colors_by_attr
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as nx

#Bornholm or malta?
#place = 'bornholm'
place = 'grenada'

graph = nx.MultiGraph

#Get graph
if place == 'bornholm':
    graph :nx.MultiDiGraph = ox.load_graphml("./savedGraphs/" + place + ".graphml")
if place == 'grenada':
    graph :nx.MultiDiGraph = ox.load_graphml("./savedGraphs/" + place + ".graphml")
else:
    graph1 = ox.load_graphml("./savedGraphs/" + place + "1.graphml")
    graph2 = ox.load_graphml("./savedGraphs/" + place + "2.graphml")
    graph3 = ox.load_graphml("./savedGraphs/" + place + "3.graphml")
    graph = nx.compose_all([graph1, graph2, graph3])

#get edges and map with color dep. on length
edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)
edges_series = edges['length']
edges[['osmid','length']]
ec = get_edge_colors_by_attr(graph, attr='length')

#plot graph, leave open
fig, ax = ox.plot_graph(graph, edge_color=ec, show=False, close=False, node_size=4, figsize=(20,20))

#make color map label
norm=plt.Normalize(vmin=edges['length'].min(), vmax=edges['length'].max())
cmap = plt.cm.get_cmap('viridis')
cb = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap,), ax=ax, orientation='horizontal',fraction=0.026, pad=0.02)
cb.set_label('edge length [m]', fontsize = 10)

#show plot
fm = plt.get_current_fig_manager()
fm.window.wm_geometry("+0+0")
fm.set_window_title(place)
plt.show()