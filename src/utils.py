"""Contains helper functions for loading graphs, handling intersections, and downloading data."""

import re
import os
import osmnx as ox


def get_coordinates(place_name) -> tuple | None:
    """Convert a place name to (latitude, longitude)."""
    location = ox.geocode(place_name)
    if location:
        return location[0], location[1]
    return None


def is_valid_location(input_str) -> bool:
    """Checks if the input contains only letters, numbers, commas, and spaces."""
    return (
        bool(re.fullmatch(r"[a-zA-Z0-9,.\s\u0400-\u04FF]+", input_str))
        and not input_str.isdigit()
    )


def download_and_save_graph() -> None:
    """Download the map."""
    location = "Sofia, Bulgaria"
    graph = ox.graph_from_place(location, network_type="drive")

    graph_file = "sofia_street_network.graphml"
    ox.save_graphml(graph, graph_file)
    print(f"Graph saved to {graph_file}")


def load_graph():
    """Load the map into a graph."""
    graph_file = "sofia_street_network.graphml"

    if os.path.exists(graph_file):
        graph = ox.load_graphml(graph_file)
        print(f"Graph loaded from {graph_file}")
        return graph
    download_and_save_graph()
    graph = ox.load_graphml(graph_file)
    print(f"Graph loaded from {graph_file}")
    return graph


def intersection(graph) -> list[tuple]:
    """Get coordinates of specified intersections."""
    intersections = [
        ("Опълченска & бул.Сливница, България", None),
        ("бул. Ген. Скобелев & Опълченска, България", (42.699849, 23.310175)),
        (
            "бул. Ген. Скобелев & бул. Патриарх Евтимий, България",
            (42.689459, 23.313978),
        ),
        ("бул. Патриарх Евтимий & бул. Васил Левски, България", (42.688128, 23.328905)),
        ("бул. Васил Левски и бул. Сливница, България", (42.704872, 23.332491)),
    ]

    intersection_coords = []

    for intersection_name, coords in intersections:
        if coords is None:
            coords = get_coordinates(intersection_name)
        intersection_node = ox.distance.nearest_nodes(graph, X=coords[1], Y=coords[0])
        intersection_coords.append(
            (graph.nodes[intersection_node]["y"], graph.nodes[intersection_node]["x"])
        )

    return [(lon, lat) for lat, lon in intersection_coords]
