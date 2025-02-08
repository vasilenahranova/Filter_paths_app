import heapq
import osmnx as ox
import os 
import networkx as nx

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

def get_coordinates(place_name):
    """Convert a place name to latitude and longitude."""
    location = ox.geocode(place_name)
    if location:
        return location[0], location[1]  # Return (latitude, longitude)
    else:
        return None
    
def built_in_dijkstra(G, start_coords, end_coords):
    # Step 1: Convert coordinates to nearest nodes
    start_node = ox.distance.nearest_nodes(G, X=start_coords[1], Y=start_coords[0])
    end_node = ox.distance.nearest_nodes(G, X=end_coords[1], Y=end_coords[0])

    # Step 2: Use built-in Dijkstra functions to find the shortest path
    path = nx.dijkstra_path(G, source=start_node, target=end_node, weight='length')
    total_length = nx.dijkstra_path_length(G, source=start_node, target=end_node, weight='length')

    return path, total_length

# Example usage
start_coords = get_coordinates("ФМИ, България")
end_coords = get_coordinates("Лидл, ж.к. Хаджи Димитър, България")

G = load_graph()
# # Find the shortest path using the custom Dijkstra algorithm
shortest_path, total_length = built_in_dijkstra(G, start_coords, end_coords)

# # Print the results
#print(f"Shortest path (nodes): {shortest_path}")
print(f"Total path length: {total_length} meters")

# # Step 6: (Optional) Visualize the path on the map
# ox.plot_graph_route(G, shortest_path, route_linewidth=6, node_size=0, bgcolor='k')
