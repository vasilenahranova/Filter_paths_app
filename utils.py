import osmnx as ox
import re
import os

def get_coordinates(place_name):
    """Convert a place name to latitude and longitude."""
    location = ox.geocode(place_name)
    if location:
        return location[0], location[1]  # Return (latitude, longitude)
    else:
        return None

def is_valid_location(input_str):
    """Checks if the input contains only letters, numbers, commas, and spaces."""
    return bool(re.fullmatch(r'[a-zA-Z0-9,.\s\u0400-\u04FF]+', input_str)) and not input_str.isdigit()

def download_and_save_graph():
    location = "Sofia, Bulgaria"
    G = ox.graph_from_place(location, network_type='drive')

    graph_file = 'sofia_street_network.graphml'
    ox.save_graphml(G, graph_file)
    print(f"Graph saved to {graph_file}")

def load_graph():
    graph_file = 'sofia_street_network.graphml'
    
    if os.path.exists(graph_file):
        G = ox.load_graphml(graph_file)
        print(f"Graph loaded from {graph_file}")
        return G
    else:
        download_and_save_graph()
        G = ox.load_graphml(graph_file)
        print(f"Graph loaded from {graph_file}")
        return G

def intersection(G) -> list[tuple]:
    """Get coordinates of specified intersections."""
    # Define intersection descriptions and their coordinates
    intersections = [
        ("Опълченска & бул.Сливница, България", None),
        ("бул. Ген. Скобелев & Опълченска, България", (42.699849, 23.310175)),
        ("бул. Ген. Скобелев & бул. Патриарх Евтимий, България", (42.689459, 23.313978)),
        ("бул. Патриарх Евтимий & бул. Васил Левски, България", (42.688128, 23.328905)),
        ("бул. Васил Левски и бул. Сливница, България", (42.704872, 23.332491)),
    ]

    intersection_coords = []

    for intersection_name, coords in intersections:
        if coords is None:  # For addresses, get coordinates using get_coordinates function
            coords = get_coordinates(intersection_name)
        # Find the nearest node in the graph
        intersection_node = ox.distance.nearest_nodes(G, X=coords[1], Y=coords[0])
        intersection_coords.append((G.nodes[intersection_node]['y'], G.nodes[intersection_node]['x']))

    return [(lon, lat) for lat, lon in intersection_coords]
