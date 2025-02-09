from src.user import User
from src.graph import Graph

if __name__ == "__main__":
    user = User()
    user.get_user_input()

    g = Graph()
    g.manipulate_graph()

    path, length = g.find_shortest_path(user.start_point_coordinates, user.target_point_coordinates)
    g.save_path_for_navigation(path,'user_path.gpx')
    g.visualize(path)



    