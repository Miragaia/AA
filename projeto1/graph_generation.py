import os
import random
import networkx as nx
import matplotlib.pyplot as plt
import math
import getopt
import sys

def store_graph(vertices, num_vertices, percentage, graph):
    filename = f"graphs/graph_num_vertices_{num_vertices}_percentage_{percentage}.graphml"

    # Split the tuple and set separate attributes for x and y coordinates
    nx.set_node_attributes(graph, {v: vertices[v][0] for v in vertices}, 'x')
    nx.set_node_attributes(graph, {v: vertices[v][1] for v in vertices}, 'y')

    nx.write_graphml(graph, filename)

    pos = {v: vertices[v] for v in graph.nodes}
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw(graph, pos, with_labels=True, node_color='lightblue')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.savefig(f"graphs/graph_num_vertices_{num_vertices}_percentage_{percentage}.png")
    plt.clf()


def calculate_max_num_edges(num_vertices):
    return num_vertices * (num_vertices - 1) / 2

def create_edges_and_graph(percentage_max_num_edges, vertices, num_vertices):
    G = nx.Graph()
    num_edges = math.ceil(percentage_max_num_edges * calculate_max_num_edges(num_vertices))
    isolated_vertices = list(vertices.keys())

    for edge in range(num_edges):
        if isolated_vertices:
            v1 = random.choice(isolated_vertices)
            isolated_vertices.remove(v1)
            v2 = random.choice(isolated_vertices) if isolated_vertices else random.choice(
                [v for v in vertices.keys() if v != v1])
        else:
            v1, v2 = random.sample([v for v in vertices.keys() if len(list(G.neighbors(v))) < num_vertices - 1], 2)

        weight = random.randint(1, 10)
        G.add_edge(v1, v2, weight=weight)

    return G

def create_vertices(vertices_num, max_value_coordinate):
    vertices = {}
    for v in range(1, vertices_num + 1):
        while True:
            x, y = random.randint(1, max_value_coordinate), random.randint(1, max_value_coordinate)
            if (x, y) not in vertices.values() and all(math.dist(coord, (x, y)) > 1 for coord in vertices.values()):
                vertices[v] = (x, y)
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
        os.mkdir("graphs")
    random.seed(108317)
    create_graphs(vertices_num_last_graph, max_value_coordinate)
