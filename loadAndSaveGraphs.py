import osmnx as ox

#example, malta
G = ox.graph_from_place('Republic of Malta', network_type='drive')
ox.save_graphml(G, filepath="./savedGraphs/malta.graphml")

#example, bornholm
G = ox.graph_from_place('Bornholm', network_type='drive')
ox.save_graphml(G, filepath="./savedGraphs/bornholm.graphml")