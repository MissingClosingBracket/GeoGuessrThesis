import osmnx as ox
from osmnx.plot import get_edge_colors_by_attr
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#Bornholm or malta?
#place = 'bornholm'
place = 'malta'

#Get graph from bbox
graph = ox.load_graphml("./savedGraphs/" + place + ".graphml")

#get edges and map with color dep. on length
edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)
edges_series = edges['length']
edges[['osmid','length']]
ec = get_edge_colors_by_attr(graph, attr='length')

#plot graph, leave open
fig, ax = ox.plot_graph(graph, edge_color=ec, show=False, close=False, node_size=4, figsize=(14,13))

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