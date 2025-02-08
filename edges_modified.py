import osmnx as ox
from shapely.geometry import Polygon
import os

def load_graph():
    graph_file = 'sofia_street_network.graphml'
    
    # Check if the file exists before loading
    if os.path.exists(graph_file):
        G = ox.load_graphml(graph_file)
        print(f"Graph loaded from {graph_file}")
        return G
    else:
        print(f"{graph_file} does not exist. Please download the data first.")
        return None

G = load_graph()

coordinates = [(23.3111298, 42.7061677), (23.3101698, 42.6998497), (23.3139859, 42.6894673), (23.3289143, 42.6881327), (23.3326267, 42.7047627)]
restricted_zone = Polygon(coordinates)

import itertools
edges = G.edges(keys=True, data=True)
for _, _, _, edge_data in itertools.islice(edges,1000):
    edge_geometry = edge_data.get("geometry")

    if edge_geometry:
        if edge_geometry.intersects(restricted_zone):
            original_length = edge_data.get("length")
            edge_data["length"] = original_length * 20