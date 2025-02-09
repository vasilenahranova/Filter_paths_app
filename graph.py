from utils import load_graph, intersection
from shapely.geometry import Polygon
import osmnx as ox
import networkx as nx
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

class Graph:
    def __init__(self) -> None:
        self.G = load_graph()
        self.restricted_area = None

    def create_restricted_area(self) -> None:
        intersection_coords = intersection(self.G)
        self.restricted_area = Polygon(intersection_coords)

    def recalculate_weights(self) -> None:
        edges = self.G.edges(keys=True, data=True)
        for _, _, _, edge_data in edges:
            edge_geometry = edge_data.get("geometry")

            if edge_geometry:
                if edge_geometry.intersects(self.restricted_area):
                    original_length = edge_data.get("length")
                    edge_data["length"] = original_length * 20

    def manipulate_graph(self) -> None:
        self.create_restricted_area()
        self.recalculate_weights()

    def find_shortest_path(self, start_coords, end_coords) -> tuple:
        start_node = ox.distance.nearest_nodes(self.G, X=start_coords[1], Y=start_coords[0])
        end_node = ox.distance.nearest_nodes(self.G, X=end_coords[1], Y=end_coords[0])

        path = nx.dijkstra_path(self.G, source=start_node, target=end_node, weight='length')
        total_length = nx.dijkstra_path_length(self.G, source=start_node, target=end_node, weight='length')
        # total_length = sum(self.G[u][v].get('length', 0) for u, v in zip(path[:-1], path[1:])) #manually calculating length from the path

        return (path, total_length)

    def save_path_for_navigation(self, path, file_path) -> None:
        """Save the path to a .gpx file."""
        gpx = ET.Element('gpx', version="1.1", creator="Filter Paths app", xmlns="http://www.topografix.com/GPX/1/1")

        trk = ET.SubElement(gpx, 'trk')
        trk_name = ET.SubElement(trk, 'name')
        trk_name.text = "User's Route"

        trkseg = ET.SubElement(trk, 'trkseg')

        for node in path:
            lat = self.G.nodes[node]['y']
            lon = self.G.nodes[node]['x']
            trkpt = ET.SubElement(trkseg, 'trkpt', lat=str(lat), lon=str(lon))

        tree = ET.ElementTree(gpx)

        with open("file_path", 'wb') as f:
            tree.write(f)

        print(f"Path saved to {file_path}")

