"""Defines the Graph class for managing restricted areas,
graph manipulation, finding shortest paths and saving them in GPX format."""

from datetime import datetime, timedelta, timezone
import xml.etree.ElementTree as ET
from xml.dom import minidom
from shapely.geometry import Polygon
import osmnx as ox
import networkx as nx
from src.utils import load_graph, intersection


class Graph:
    """Graph class."""
    def __init__(self) -> None:
        self.graph = load_graph()
        self.restricted_area = None

    def create_restricted_area(self) -> None:
        """Create the restricted area."""
        intersection_coords = intersection(self.graph)
        self.restricted_area = Polygon(intersection_coords)

    def recalculate_weights(self) -> None:
        """Change edge weights if they are in the restricted area."""
        edges = self.graph.edges(keys=True, data=True)
        for _, _, _, edge_data in edges:
            edge_geometry = edge_data.get("geometry")

            if edge_geometry:
                if edge_geometry.intersects(self.restricted_area):
                    original_length = edge_data.get("length")
                    edge_data["length"] = original_length * 20

    def manipulate_graph(self) -> None:
        """Manipulate the graph"""
        self.create_restricted_area()
        self.recalculate_weights()

    def find_shortest_path(self, start_coords, end_coords) -> tuple:
        """Find shortest path between two points"""
        start_node = ox.distance.nearest_nodes(
            self.graph, X=start_coords[1], Y=start_coords[0]
        )
        end_node = ox.distance.nearest_nodes(
            self.graph, X=end_coords[1], Y=end_coords[0]
        )

        path = nx.dijkstra_path(
            self.graph, source=start_node, target=end_node, weight="length"
        )
        total_length = nx.dijkstra_path_length(
            self.graph, source=start_node, target=end_node, weight="length"
        )

        return (path, total_length)

    def save_path_for_navigation(self, path, file_path) -> None:
        """Save the path to a .gpx file with timestamps."""
        gpx = ET.Element(
            "gpx",
            version="1.1",
            creator="Filter Paths app",
            xmlns="http://www.topografix.com/GPX/1/1",
        )

        trk = ET.SubElement(gpx, "trk")
        trk_name = ET.SubElement(trk, "name")
        trk_name.text = "User's Route"

        trkseg = ET.SubElement(trk, "trkseg")

        timestamp = datetime.now(timezone.utc)

        for node in path:
            lat = self.graph.nodes[node]["y"]
            lon = self.graph.nodes[node]["x"]

            time_str = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")

            trkpt = ET.SubElement(trkseg, "trkpt", lat=str(lat), lon=str(lon))
            ele = ET.SubElement(trkpt, "ele")
            ele.text = str(self.graph.nodes[node].get("elevation", 0))
            time = ET.SubElement(trkpt, "time")
            time.text = time_str
            timestamp += timedelta(seconds=30)

        rough_string = ET.tostring(gpx, "utf-8")
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

        print(f"Path saved to {file_path}")
