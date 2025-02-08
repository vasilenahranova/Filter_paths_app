import osmnx as ox
import os
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

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

# edges_from_target = [(u, v, data) for u, v, data in G.edges(data=True) if v == roundabout_node]

def intersection() -> None:
    G = load_graph()
    #Intersections
    intersection_1 = "Опълченска & бул.Сливница, България"
    intersection_1_coords = get_coordinates(intersection_1)
    #intersection_2 = "бул. Ген. Скобелев & Опълченска, България"
    roundabout_coords = (42.699849, 23.310175)
    intersection_node = ox.distance.nearest_nodes(G, X=roundabout_coords[1], Y=roundabout_coords[0])
    intersection_2_coords = (G.nodes[intersection_node]['y'], G.nodes[intersection_node]['x'])
    # intersection_3 = "бул. Ген. Скобелев & бул. Патриарх Евтимий, България"
    roundabout_coords = (42.689459, 23.313978)
    intersection_node = ox.distance.nearest_nodes(G, X=roundabout_coords[1], Y=roundabout_coords[0])
    intersection_3_coords = (G.nodes[intersection_node]['y'], G.nodes[intersection_node]['x'])
    #intersection_4 = "бул. Патриарх Евтимий & бул. Васил Левски, България"
    roundabout_coords = (42.688128, 23.328905)
    intersection_node = ox.distance.nearest_nodes(G, X=roundabout_coords[1], Y=roundabout_coords[0])
    intersection_4_coords = (G.nodes[intersection_node]['y'], G.nodes[intersection_node]['x'])
    #"бул. Васил Левски и бул. Сливница"
    roundabout_coords = (42.704872, 23.332491)
    intersection_node = ox.distance.nearest_nodes(G, X=roundabout_coords[1], Y=roundabout_coords[0])
    intersection_5_coords = (G.nodes[intersection_node]['y'], G.nodes[intersection_node]['x'])

    intersection_coords = [intersection_1_coords, intersection_2_coords, intersection_3_coords, intersection_4_coords, intersection_5_coords]
    corrected_coords = [(lon, lat) for lat, lon in intersection_coords]
    restricted_zone = Polygon(corrected_coords)

    # Plot the restricted zone
    x, y = restricted_zone.exterior.xy  # Get the coordinates for plotting
    plt.plot(x, y, color="red")  # Plot the restricted zone
    plt.fill(x, y, color="lightblue", alpha=0.5)  # Fill the polygon
    plt.title("Restricted Zone")
    plt.show()

    return restricted_zone

intersection()