import osmnx as ox
import matplotlib.pyplot as plt

# Load the saved graph
G = ox.load_graphml("sofia_street_network.graphml")

# Define the bounding box (latitude, longitude) - Adjust to your needs
north, south, east, west = 42.7, 42.65, 23.35, 23.30

# Get a subgraph within the bounding box
G_sub = ox.truncate.truncate_graph_bbox(G, (north, south, east, west))

# Plot only this smaller region
fig, ax = ox.plot_graph(G_sub, node_size=5, edge_linewidth=0.5, bgcolor="white")
plt.show()
