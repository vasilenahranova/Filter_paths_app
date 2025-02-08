import osmnx as ox
import networkx as nx
import os

def download_and_save_graph():
    # Define the location for Sofia
    location = "Sofia, Bulgaria"
    
    # Download the drivable street network of Sofia
    G = ox.graph_from_place(location, network_type='drive')

    # Save the graph to a GraphML file
    graph_file = 'sofia_street_network.graphml'
    ox.save_graphml(G, graph_file)
    print(f"Graph saved to {graph_file}")

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

# Example usage
# First, download and save the graph
#download_and_save_graph()

# Later, load the saved graph for use
G = load_graph()

roundabout_coords = (42.705083, 23.332920)

# Function to find the closest ne tood a given set of coordinates
def closest_node(graph, point):
    return ox.distance.nearest_nodes(graph, X=point[1], Y=point[0])

# Get the closest node for the roundabout
roundabout_node = closest_node(G, roundabout_coords)

# Print the node ID
print(f"Roundabout Node: {roundabout_node}")


# import matplotlib.pyplot as plt
# from shapely.geometry import LineString

# # Example edge (replace with actual node IDs from your graph)
# u, v, data = list(G.edges(data=True))[0]
# u, v = 93528622, 418753021  

# # Get the edge data from your graph
# edge_data = G[u][v][0]  # The [0] is needed because edges can have multiple attributes

# # Extract geometry (this should be a LineString object)
# if "geometry" in edge_data:
#     road_geom = edge_data["geometry"]  # This is a LineString
#     x, y = road_geom.xy  # Get the x (longitude) and y (latitude) coordinates

#     # Plot the road segment
#     plt.figure(figsize=(6, 6))
#     plt.plot(x, y, marker="o", color="blue", linestyle="-", linewidth=2)
#     plt.title(f"Road Segment: {edge_data.get('name', 'Unknown Name')}")
#     plt.xlabel("Longitude")
#     plt.ylabel("Latitude")
#     plt.grid(True)
#     plt.show()
# else:
#     print("This road does not have geometry data.")


# You can now use the graph (G) for further processing
