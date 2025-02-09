from src.utils import load_graph, intersection
from shapely.geometry import Polygon
import osmnx as ox
import networkx as nx
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
from xml.dom import minidom

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

        return (path, total_length)

    def save_path_for_navigation(self, path, file_path) -> None:
        """Save the path to a .gpx file with timestamps."""
        gpx = ET.Element('gpx', version="1.1", creator="Filter Paths app", xmlns="http://www.topografix.com/GPX/1/1")

        trk = ET.SubElement(gpx, 'trk')
        trk_name = ET.SubElement(trk, 'name')
        trk_name.text = "User's Route"

        trkseg = ET.SubElement(trk, 'trkseg')

        timestamp = datetime.now(timezone.utc)

        for node in path:
            lat = self.G.nodes[node]['y']
            lon = self.G.nodes[node]['x']
            
            time_str = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
            
            trkpt = ET.SubElement(trkseg, 'trkpt', lat=str(lat), lon=str(lon))
            ele = ET.SubElement(trkpt, 'ele')
            ele.text = str(self.G.nodes[node].get('elevation', 0))
            time = ET.SubElement(trkpt, 'time')
            time.text = time_str
            timestamp += timedelta(seconds=30)

        rough_string = ET.tostring(gpx, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)

        print(f"Path saved to {file_path}")
    
    def visualize(self, path) -> None:
        """Visualize the shortest path on the map."""
        path_coords = [(self.G.nodes[node]['x'], self.G.nodes[node]['y']) for node in path]

        fig, ax = plt.subplots(figsize=(10, 10))

        ox.plot_graph(self.G, ax=ax, node_size=10, edge_color='lightgray', bgcolor='white')

        path_lon, path_lat = zip(*path_coords)
        ax.plot(path_lon, path_lat, color='red', linewidth=3, label="Shortest Path")

        start_node = path[0]
        end_node = path[-1]
        start_coords = (self.G.nodes[start_node]['x'], self.G.nodes[start_node]['y'])
        end_coords = (self.G.nodes[end_node]['x'], self.G.nodes[end_node]['y'])

        ax.text(start_coords[0], start_coords[1], 'Start', fontsize=12, ha='right', color='green')
        ax.text(end_coords[0], end_coords[1], 'End', fontsize=12, ha='left', color='blue')

        ax.legend()
        plt.show()