import osmnx as ox
'''
#example, malta
G1 = ox.graph_from_bbox(north=36.0831,south=36.0036,east=14.3523, west=14.1825, network_type='drive')
ox.save_graphml(G1, filepath="./savedGraphs/malta1.graphml")
G2 = ox.graph_from_bbox(north=36.0002,south=35.8039,east=14.5782, west=14.3183, network_type='drive')
ox.save_graphml(G2, filepath="./savedGraphs/malta2.graphml")
G3 = ox.graph_from_bbox(north=36.0209,south=36.0036,east=14.3513, west=14.3162, network_type='drive')
ox.save_graphml(G3, filepath="./savedGraphs/malta3.graphml")
#example, bornholm
G4 = ox.graph_from_place('Bornholm', network_type='drive')
ox.save_graphml(G4, filepath="./savedGraphs/bornholm.graphml")
'''
#Grenada
G = ox.graph_from_bbox(north=12.2363,south=11.9836,east=-61.5979, west=-61.8101, network_type='drive')
ox.save_graphml(G, filepath="./savedGraphs/grenada.graphml")