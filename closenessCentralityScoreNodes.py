import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.cm as cm
import matplotlib.colors as colors
import pandas as pd

#Thank you: https://github.com/gboeing/osmnx-examples/blob/v0.11/notebooks/08-example-line-graph.ipynb


print("Initializing")

#get graph from description
print("Fetching graph")
G = ox.load_graphml("./savedGraphs/bornholm.graphml")
G = ox.project_graph(G)

node_centrality = nx.closeness_centrality(G)

#869914855   0.040789
#1548511365  0.041006
#32835162    0.041029

df = pd.DataFrame(data=pd.Series(node_centrality).sort_values(), columns=['cc'])
df['colors'] = ox.plot.get_colors(n=len(df), cmap='inferno', start=0.2)
df = df.reindex(G.nodes())
nc = df['colors'].tolist()
fig, ax = ox.plot_graph(G, bgcolor='k', node_size=10, node_color=nc, node_edgecolor='none',
                        edge_color='#555555', edge_linewidth=1.5, edge_alpha=1, close=False,show=False)

node1 = G.nodes[32835162]
node2 = G.nodes[1548511365]
node3 = G.nodes[869914855]
print(node1['lat'], node1['lon'])
ax.scatter(node1['x'], node1['y'], color="red",s=100,zorder=1000, label="Closeness centrality score = 0.041029")
ax.scatter(node2['x'], node2['y'], color="blue",s=100,zorder=1000, label="Closeness centrality score = 0.041006")
ax.scatter(node3['x'], node3['y'], color="green",s=100,zorder=1000, label="Closeness centrality score = 0.040789")

#make color map label
norm=plt.Normalize(vmin=0.0, vmax=0.041029)
cmap = plt.cm.get_cmap('inferno')
cb = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap,), ax=ax, orientation='horizontal',fraction=0.026, pad=0.02)
cb.set_label('Closeness centrality score', fontsize = 10)

plt.legend(loc="upper left")
plt.draw()
plt.show()

