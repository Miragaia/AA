import os
import random
import networkx as nx
import matplotlib.pyplot as plt
import math
import getopt
import sys

import matplotlib.pyplot as plt

def store_graph(vertices, num_vertices, percentage, graph):
    filename = f"graphs/graphml/graph_num_vertices_{num_vertices}_percentage_{percentage}.graphml"

    # Set node attributes for x, y coordinates, and weights separately
    nx.set_node_attributes(graph, {v: vertices[v][0][0] for v in vertices}, 'x')
    nx.set_node_attributes(graph, {v: vertices[v][0][1] for v in vertices}, 'y')
    nx.set_node_attributes(graph, {v: vertices[v][1] for v in vertices}, 'weight')

    # Save the graph in GraphML format
    nx.write_graphml(graph, filename)

    # Draw the graph with node weights as side labels
    pos = {v: (vertices[v][0][0], vertices[v][0][1]) for v in graph.nodes}
    
    # Draw main node labels (node names)
    nx.draw(graph, pos, with_labels=True, node_color='lightblue')
    
    # Apply an offset for weight labels in display (pixel) coordinates
    fig, ax = plt.gcf(), plt.gca()
    transform = ax.transData.transform
    inverse_transform = ax.transData.inverted().transform

    weight_labels = {v: vertices[v][1] for v in graph.nodes}
    label_pos = {}

    for k, (x, y) in pos.items():
        # Transform data coordinates to display coordinates
        display_x, display_y = transform((x, y))
        # Apply offset in display coordinates (e.g., 15 pixels to the right)
        display_x += 25  # Adjust this value for more/less offset
        # Convert back to data coordinates
        label_pos[k] = inverse_transform((display_x, display_y))

    nx.draw_networkx_labels(graph, label_pos, labels=weight_labels, font_color="red")
    
    # Save the figure
    plt.savefig(f"graphs/png/graph_num_vertices_{num_vertices}_percentage_{percentage}.png")
    plt.clf()




def calculate_max_num_edges(num_vertices):
    return num_vertices * (num_vertices - 1) / 2

def create_edges_and_graph(percentage_max_num_edges, vertices, num_vertices):
    G = nx.Graph()
    num_edges = math.ceil(percentage_max_num_edges * calculate_max_num_edges(num_vertices))
    isolated_vertices = list(vertices.keys())

    # Add all vertices to the graph initially
    for v in vertices.keys():
        G.add_node(v)

    for edge in range(num_edges):
        if isolated_vertices:
            v1 = random.choice(isolated_vertices)
            isolated_vertices.remove(v1)
            v2 = random.choice(isolated_vertices) if isolated_vertices else random.choice(
                [v for v in vertices.keys() if v != v1])
            if v2 in isolated_vertices:
                isolated_vertices.remove(v2)
        else:
            # Choose a random vertex that is not yet connected to all vertices
            v1 = random.choice([v for v in vertices.keys() if len(list(G.neighbors(v))) < num_vertices - 1])
            # Choose a random vertex that is not yet connected to v1
            v2 = random.choice([v for v in vertices.keys() if v != v1 and v not in G[v1]])

        G.add_edge(v1, v2)

    return G


def create_vertices(vertices_num, max_value_coordinate):
    vertices = {}
    alphabet_labels = [chr(65 + i) for i in range(vertices_num)]  # A, B, C, ...

    for i, label in enumerate(alphabet_labels):
        while True:
            x, y = random.randint(1, max_value_coordinate), random.randint(1, max_value_coordinate)
            if (x, y) not in [coord for coord, _ in vertices.values()] and \
               all(math.dist(coord, (x, y)) > 1 for coord, _ in vertices.values()):
                weight = random.randint(1, 50)  # Assign a random weight to each node
                vertices[label] = ((x, y), weight)  # Store (coordinates, weight)
                break
    return vertices


def create_graphs(vertices_num_last_graph, max_value_coordinate):
    for num_vertices in range(4, vertices_num_last_graph + 1):
        vertices = create_vertices(num_vertices, max_value_coordinate)
        for percentage in [0.125, 0.25, 0.50, 0.75]:
            G = create_edges_and_graph(percentage, vertices, num_vertices)
            store_graph(vertices, num_vertices, percentage, G)

def read_arguments():
    argumentList = sys.argv[1:]
    options = "v:m:"
    long_options = ["Vertices_Num_Last_Graph", "Max_Value_Coordinate"]

    vertices_num_last_graph, max_value_coordinate = 10, 1000
    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-v", "--Vertices_Num_Last_Graph"):
                vertices_num_last_graph = int(currentValue)
            elif currentArgument in ("-m", "--Max_Value_Coordinate"):
                max_value_coordinate = int(currentValue)
    except getopt.error as err:
        print(str(err))
    return vertices_num_last_graph, max_value_coordinate

def generate_weighted_graph(vertices_num_last_graph, max_value_coordinate):
    if not os.path.isdir("graphs"):
        os.makedirs("graphs/graphml", exist_ok=True)
        os.makedirs("graphs/png", exist_ok=True)
    random.seed(108317)
    create_graphs(vertices_num_last_graph, max_value_coordinate)
