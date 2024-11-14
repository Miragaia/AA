import pandas as pd
import time
import cProfile
import networkx as nx
import matplotlib.pyplot as plt
import os
from graph_generation import generate_weighted_graph, read_arguments
from algorithms import exhaustive_search_mweds, greedy_mweds
from analysis import executions_times, basic_operations_num, compare_solutions, save_to_csv

def profile_algorithm(algorithm_func, *args, **kwargs):
    """Profile an algorithm's execution."""
    profiler = cProfile.Profile()
    profiler.enable()
    result = algorithm_func(*args, **kwargs)
    profiler.disable()
    profiler.print_stats(sort='cumtime')
    return result


def draw_and_save_graph(graph_file, edge_set, num_vertices, percentage, algorithm_type, title):
    """
    Draws the graph with edges in edge_set highlighted in red, shows edge weights, 
    and saves as PNG using the specified naming convention.
    """
    # Load graph from GraphML file
    G = nx.read_graphml(graph_file)

    # Retrieve positions from node attributes
    pos = {node: (G.nodes[node]['x'], G.nodes[node]['y']) for node in G.nodes()}

    plt.figure(figsize=(8, 8))

    # Draw all edges in light gray
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, edge_color="lightgray")

    # Draw edges in the edge dominating set in red
    nx.draw_networkx_edges(G, pos, edgelist=edge_set, edge_color="red", width=2)

    # Retrieve weights for edges in the solution set
    edge_labels = {edge: G[edge[0]][edge[1]]['weight'] for edge in edge_set}
    
    # Draw edge labels (weights) for edges in the solution
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color="lightblue")
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    # Add title
    plt.title(title)

    # Generate filename based on algorithm type, num_vertices, and percentage
    filename = f"graphs_solution/{algorithm_type}_{num_vertices}_percentage_{percentage}.png"

    # Save the figure
    plt.savefig(filename)
    plt.close()

def main():
    results_exhaustive = []
    results_greedy = []
    comparison_results = []

    vertices_num_last_graph, max_value_coordinate = read_arguments()
    graphs_with_metadata = generate_weighted_graph(vertices_num_last_graph, max_value_coordinate)
    
    for i, (G, num_vertices, edge_prob) in enumerate(graphs_with_metadata):
        # File path for the stored graph layout
        graph_file = f"graphs/graphml/graph_num_vertices_{num_vertices}_percentage_{edge_prob}.graphml"
        
        # Exhaustive Search with profiling
        start_time = time.time()
        exhaustive_set, exhaustive_weight = profile_algorithm(exhaustive_search_mweds, G)
        end_time = time.time()
        exhaustive_time = end_time - start_time
        exhaustive_operations = len(exhaustive_set)
        results_exhaustive.append({
            'vertices_num': num_vertices,
            'percentage_max_num_edges': edge_prob,
            'total_weight': exhaustive_weight,
            'solution_size': len(exhaustive_set),
            'execution_time': exhaustive_time,
            'num_operations': exhaustive_operations
        })
        
        # Greedy Heuristic with profiling
        start_time = time.time()
        greedy_set, greedy_weight = profile_algorithm(greedy_mweds, G)
        end_time = time.time()
        greedy_time = end_time - start_time
        greedy_operations = len(greedy_set)
        results_greedy.append({
            'vertices_num': num_vertices,
            'percentage_max_num_edges': edge_prob,
            'total_weight': greedy_weight,
            'solution_size': len(greedy_set),
            'execution_time': greedy_time,
            'num_operations': greedy_operations
        })

        # Comparison metrics
        comparison_results.append({
            'vertices_num': num_vertices,
            'percentage_max_num_edges': edge_prob,
            'exhaustive_total_weight': exhaustive_weight,
            'greedy_total_weight': greedy_weight,
            'weight_difference': exhaustive_weight - greedy_weight,
            'exhaustive_execution_time': exhaustive_time,
            'greedy_execution_time': greedy_time,
            'time_ratio': greedy_time / exhaustive_time if exhaustive_time != 0 else float('inf')
        })

        # Draw and save graphs with marked solutions
        exhaustive_edges = [(u, v) for u, v, w in exhaustive_set]
        greedy_edges = [(u, v) for u, v, w in greedy_set]
        
        draw_and_save_graph(
            graph_file, exhaustive_edges, num_vertices, edge_prob, "exhaustive", "Exhaustive Solution")
        
        draw_and_save_graph(
            graph_file, greedy_edges, num_vertices, edge_prob, "greedy", "Greedy Solution")

    # Convert results to DataFrames
    df_exhaustive = pd.DataFrame(results_exhaustive)
    df_greedy = pd.DataFrame(results_greedy)
    df_comparison = pd.DataFrame(comparison_results)

    # Save results to CSV files
    save_to_csv(df_exhaustive, "exhaustive_results.csv")
    save_to_csv(df_greedy, "greedy_results.csv")
    save_to_csv(df_comparison, "comparison_results.csv")
    
    # Generate plots and analyses
    executions_times(df_exhaustive, "Exhaustive Search")
    executions_times(df_greedy, "Greedy Heuristic")
    basic_operations_num(df_exhaustive, "Exhaustive Search")
    basic_operations_num(df_greedy, "Greedy Heuristic")
    compare_solutions(df_comparison)


if __name__ == "__main__":
    print("Creating graphs for Minimum Weight Edge Dominating Set problem...")
    main()
