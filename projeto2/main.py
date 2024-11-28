import pandas as pd
import time
import cProfile
import networkx as nx
import matplotlib.pyplot as plt
import os
from graph_generation import generate_weighted_graph, read_arguments
from algorithms import randomized_mweds, dynamic_randomized_mweds
from analysis import save_to_csv

def draw_and_save_graph(graph_file, edge_set, num_vertices, percentage, algorithm_type, title):
    """
    Draws the graph with all edges showing weights, highlights edges in edge_set in red, 
    and saves as PNG with the specified naming convention.
    """
   
    G = nx.read_graphml(graph_file)

    pos = {node: (G.nodes[node]['x'], G.nodes[node]['y']) for node in G.nodes()}

    plt.figure(figsize=(8, 8))

    non_solution_edges = [edge for edge in G.edges if edge not in edge_set]

    nx.draw_networkx_edges(G, pos, edgelist=non_solution_edges, edge_color="lightgray")

    nx.draw_networkx_edges(G, pos, edgelist=edge_set, edge_color="red", width=2)

    nx.draw_networkx_nodes(G, pos, node_size=300, node_color="lightblue")
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    all_edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=all_edge_labels, font_color="black")

    plt.title(title)

    filename = f"graphs_solution/{algorithm_type}_{num_vertices}_percentage_{percentage}.png"

    plt.savefig(filename)
    plt.close()

def main():
    results_randomized = []
    results_randomized_heuristic = []
    comparison_results = []

    vertices_num_last_graph, max_value_coordinate = read_arguments()
    if vertices_num_last_graph <= 3:
        raise ValueError("The number of vertices must be greater than 3.")
    
    graphs_with_metadata = generate_weighted_graph(vertices_num_last_graph, max_value_coordinate)
    
    for i, (G, num_vertices, edge_prob) in enumerate(graphs_with_metadata):

        graph_file = f"graphs/graphml/graph_num_vertices_{num_vertices}_percentage_{edge_prob}.graphml"
        
        #limitation to 8 vertices because of the time complexity of the randomized search (needed for visualization to be limited)
        # if num_vertices <= 8:

        # randomized Search with profiling
        start_time = time.time()
        randomized__set, randomized_weight, randomized_operations,randomized_configurations = randomized_mweds(G)
        end_time = time.time()
        randomized_time = end_time - start_time
        results_randomized.append({
            'vertices_num': num_vertices,
            'percentage_max_num_edges': edge_prob,
            'total_weight': randomized_weight,
            'solution_size': len(randomized__set),
            'execution_time': randomized_time,
            'num_operations': randomized_operations,
            'randomized_configurations': randomized_configurations
        })
        
        # randomized_heuristic Heuristic with profiling
        start_time = time.time()
        randomized_heuristic_set, randomized_heuristic_weight, randomized_heuristic_operations, randomized_heuristic_configurations = dynamic_randomized_mweds(G)
        end_time = time.time()
        randomized_heuristic_time = end_time - start_time
        results_randomized_heuristic.append({
            'vertices_num': num_vertices,
            'percentage_max_num_edges': edge_prob,
            'total_weight': randomized_heuristic_weight,
            'solution_size': len(randomized_heuristic_set),
            'execution_time': randomized_heuristic_time,
            'num_operations': randomized_heuristic_operations,
            'randomized_heuristic_configurations': randomized_heuristic_configurations
        })

        comparison_results.append({
                'vertices_num': num_vertices,
                'percentage_max_num_edges': edge_prob,
                'randomized_total_weight': randomized_weight,
                'randomized_heuristic_total_weight': randomized_heuristic_weight,
                'weight_difference': randomized_weight - randomized_heuristic_weight,
                'randomized_execution_time': randomized_time,
                'randomized_heuristic_execution_time': randomized_heuristic_time,
                'time_ratio': randomized_heuristic_time / randomized_time if randomized_time != 0 else float('inf'),
                'randomized_num_operations': randomized_operations,
                'randomized_heuristic_num_operations': randomized_heuristic_operations,
                'randomized_configurations': randomized_configurations,
                'randomized_heuristic_configurations': randomized_heuristic_configurations
            })

        # Draw and save graphs with marked solutions
        randomized_edges = [(u, v) for u, v, w in randomized__set]
        randomized_heuristic_edges = [(u, v) for u, v, w in randomized_heuristic_set]
        
        if num_vertices <= 8:
            draw_and_save_graph(
                graph_file, randomized_edges, num_vertices, edge_prob, "randomized", "Randomized Solution")
            
            draw_and_save_graph(
                graph_file, randomized_heuristic_edges, num_vertices, edge_prob, "randomized_heuristic", "Randomized Heuristic Solution")

    df_randomized = pd.DataFrame(results_randomized)
    df_randomized_heuristic = pd.DataFrame(results_randomized_heuristic)
    df_comparison = pd.DataFrame(comparison_results)

    save_to_csv(df_randomized, "randomized_results.csv")
    save_to_csv(df_randomized_heuristic, "randomized_heuristic_results.csv")
    save_to_csv(df_comparison, "comparison_results.csv")
    
    # # Generate plots and analyses
    # executions_times(df_randomized, "Randomized Search")
    # executions_times(df_randomized_heuristic, "Randomized Heuristic")
    # basic_operations_num(df_randomized, "Randomized Search")
    # basic_operations_num(df_randomized_heuristic, "Randomized Heuristic")
    # basic_operations_num_aggregated(df_randomized, df_randomized_heuristic)
    # plot_time_complexity(df_randomized, df_randomized_heuristic)
    # compare_solutions(df_comparison)
    # predict_large_graph_times_75(df_randomized, df_randomized_heuristic, [8, 9, 10, 15, 20, 25, 30])
    # predict_large_graph_space([8, 9, 10, 15, 20, 25, 30])
    # greedy_weight_accuracy(df_comparison)


if __name__ == "__main__":
    print("Creating graphs for Minimum Weight Edge Dominating Set problem...")
    main()
