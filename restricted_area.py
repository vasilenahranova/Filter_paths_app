import osmnx as ox
G = ox.load_graphml("sofia_street_network.graphml")

# List of your 4 main streets
main_streets = ['бул. Васил Левски', 'бул. Сливница', 'Опълченска', 'бул. Патриарх Евтимий', 'бул. Ген. Скобелев']

# Initialize a dictionary to hold information for each street
street_info = {street: [] for street in main_streets}

for u, v, data in G.edges(data=True):
    road_name = data.get('name')
    
    if road_name in main_streets:
        street_info[road_name].append({
            'from_node': u,
            'to_node': v,
            'length': data.get('length', 0),  # Length in meters
            'speed_limit': data.get('maxspeed', 'Unknown'),  # Speed limit
            'geometry': data.get('geometry'),  # Geometry for visualization
        })

# for street in street_info:
#     print(f"{street.key} + {street.value.__len__}")
#     print("\n")

print(street_info['бул. Васил Левски'])

# Now, you can print or process the data
# for street, segments in street_info.items():
#     print(f"Details for {street}:")
#     total_length = sum(segment['length'] for segment in segments)
#     print(f"Total Length: {total_length / 1000} km")
#     print("Segment details:")
#     for segment in segments:
#         print(f"  From Node {segment['from_node']} to Node {segment['to_node']}, Length: {segment['length']} meters, Speed Limit: {segment['speed_limit']}")
#     print("\n")
