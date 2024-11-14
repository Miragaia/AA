import pandas as pd
import time
import cProfile
import networkx as nx
import matplotlib.pyplot as plt
import os
from graph_generation import generate_weighted_graph, read_arguments
from algorithms import exhaustive_search_mweds, greedy_mweds
from analysis import executions_times, basic_operations_num, compare_solutions, save_to_csv, plot_time_complexity, basic_operations_num_aggregated, predict_large_graph_times_75

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
    results_exhaustive = []
    results_greedy = []
    comparison_results = []

    vertices_num_last_graph, max_value_coordinate = read_arguments()
    if vertices_num_last_graph <= 3:
        raise ValueError("The number of vertices must be greater than 3.")
    
    graphs_with_metadata = generate_weighted_graph(vertices_num_last_graph, max_value_coordinate)
    
    for i, (G, num_vertices, edge_prob) in enumerate(graphs_with_metadata):

        graph_file = f"graphs/graphml/graph_num_vertices_{num_vertices}_percentage_{edge_prob}.graphml"
        
        #limitation to 8 vertices because of the time complexity of the exhaustive search (needed for visualization to be limited)
        if num_vertices <= 8:

            # Exhaustive Search with profiling
            start_time = time.time()
            exhaustive_set, exhaustive_weight, exhaustive_operations = profile_algorithm(exhaustive_search_mweds, G)
            end_time = time.time()
            exhaustive_time = end_time - start_time
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
        greedy_set, greedy_weight, greedy_operations = profile_algorithm(greedy_mweds, G)
        end_time = time.time()
        greedy_time = end_time - start_time
        results_greedy.append({
            'vertices_num': num_vertices,
            'percentage_max_num_edges': edge_prob,
            'total_weight': greedy_weight,
            'solution_size': len(greedy_set),
            'execution_time': greedy_time,
            'num_operations': greedy_operations
        })

        if num_vertices <= 8:
            # Comparison metrics
            comparison_results.append({
                'vertices_num': num_vertices,
                'percentage_max_num_edges': edge_prob,
                'exhaustive_total_weight': exhaustive_weight,
                'greedy_total_weight': greedy_weight,
                'weight_difference': exhaustive_weight - greedy_weight,
                'exhaustive_execution_time': exhaustive_time,
                'greedy_execution_time': greedy_time,
                'time_ratio': greedy_time / exhaustive_time if exhaustive_time != 0 else float('inf'),
                'exhaustive_num_operations': exhaustive_operations,
                'greedy_num_operations': greedy_operations,
            })
        else:
            comparison_results.append({
                'vertices_num': num_vertices,
                'percentage_max_num_edges': edge_prob,
                'exhaustive_total_weight': None,
                'greedy_total_weight': greedy_weight,
                'weight_difference': None,
                'exhaustive_execution_time': None,
                'greedy_execution_time': greedy_time,
                'time_ratio': None,
                'exhaustive_num_operations': None,
                'greedy_num_operations': greedy_operations,
            })

        # Draw and save graphs with marked solutions
        exhaustive_edges = [(u, v) for u, v, w in exhaustive_set]
        greedy_edges = [(u, v) for u, v, w in greedy_set]
        
        if num_vertices <= 8:
            draw_and_save_graph(
                graph_file, exhaustive_edges, num_vertices, edge_prob, "exhaustive", "Exhaustive Solution")
            
            draw_and_save_graph(
                graph_file, greedy_edges, num_vertices, edge_prob, "greedy", "Greedy Solution")

    df_exhaustive = pd.DataFrame(results_exhaustive)
    df_greedy = pd.DataFrame(results_greedy)
    df_comparison = pd.DataFrame(comparison_results)

    save_to_csv(df_exhaustive, "exhaustive_results.csv")
    save_to_csv(df_greedy, "greedy_results.csv")
    save_to_csv(df_comparison, "comparison_results.csv")
    
    # Generate plots and analyses
    executions_times(df_exhaustive, "Exhaustive Search")
    executions_times(df_greedy, "Greedy Heuristic")
    basic_operations_num(df_exhaustive, "Exhaustive Search")
    basic_operations_num(df_greedy, "Greedy Heuristic")
    basic_operations_num_aggregated(df_exhaustive, df_greedy)
    plot_time_complexity(df_exhaustive, df_greedy)
    compare_solutions(df_comparison)
    predict_large_graph_times_75(df_exhaustive, df_greedy, [8, 9, 10, 15, 20, 25, 30])


if __name__ == "__main__":
    print("Creating graphs for Minimum Weight Edge Dominating Set problem...")
    main()
