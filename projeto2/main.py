import pandas as pd
import time
import cProfile
import networkx as nx
import matplotlib.pyplot as plt
import os
from graph_generation import generate_weighted_graph, read_arguments
from algorithms import randomized_mweds, dynamic_randomized_mweds, dynamic_combined_mweds
from analysis import save_to_csv, save_to_csv_dynamic_combined, save_to_csv_dynamic_randomized, load_exhaustive_results, load_dynamic_results, load_dynamic_combined_results, plot_accuracy, plot_weight_comparison_for_density_50, plot_solution_size_bar_chart

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
    results_dynamic_all = []
    results_dynamic_combined_all = []
    results_randomized = []

    # Define pairs of threshold values
    threshold_pairs = [
        (0.125, 0.25),
        (0.5, 0.75),
        (0.25, 0.5)
    ]

    vertices_num_last_graph, max_value_coordinate = read_arguments()
    if vertices_num_last_graph <= 3:
        raise ValueError("The number of vertices must be greater than 3.")

    graphs_with_metadata = generate_weighted_graph(vertices_num_last_graph, max_value_coordinate)

    for base_threshold, refine_threshold in threshold_pairs:

        results_dynamic = []
        results_dynamic_combined = []
        for i, (G, num_vertices, edge_prob) in enumerate(graphs_with_metadata):
            graph_file = f"graphs/graphml/graph_num_vertices_{num_vertices}_percentage_{edge_prob}.graphml"

            # Dynamic Randomized Search
            start_time = time.time()
            dynamic_set, dynamic_weight, dynamic_operations, dynamic_configurations = dynamic_randomized_mweds(
                G, base_threshold=base_threshold, refine_threshold=refine_threshold
            )
            end_time = time.time()
            dynamic_time = end_time - start_time

            results_dynamic.append({
                'vertices_num': num_vertices,
                'percentage_max_num_edges': edge_prob,
                'total_weight': dynamic_weight,
                'solution_size': len(dynamic_set),
                'execution_time': dynamic_time,
                'num_operations': dynamic_operations,
                'dynamic_configurations': dynamic_configurations,
                'base_threshold': base_threshold,
                'refine_threshold': refine_threshold
            })

            # Dynamic Combined Search
            start_time = time.time()
            dynamic_combined_set, dynamic_combined_weight, dynamic_combined_operations, dynamic_combined_configurations = dynamic_combined_mweds(
                G, base_threshold=base_threshold, refine_threshold=refine_threshold
            )
            end_time = time.time()
            dynamic_combined_time = end_time - start_time

            results_dynamic_combined.append({
                'vertices_num': num_vertices,
                'percentage_max_num_edges': edge_prob,
                'total_weight': dynamic_combined_weight,
                'solution_size': len(dynamic_combined_set),
                'execution_time': dynamic_combined_time,
                'num_operations': dynamic_combined_operations,
                'dynamic_combined_configurations': dynamic_combined_configurations,
                'base_threshold': base_threshold,
                'refine_threshold': refine_threshold
            })

            # Draw and save graphs with marked solutions if vertices are small
            if num_vertices <= 8:
                dynamic_edges = [(u, v) for u, v, w in dynamic_set]
                draw_and_save_graph(
                    graph_file, dynamic_edges, num_vertices, edge_prob, 
                    f"dynamic_base_{base_threshold}_refine_{refine_threshold}", 
                    "Randomized Heuristic Solution"
                )

        # Save results to a CSV for this threshold combination
        df_dynamic = pd.DataFrame(results_dynamic)
        df_dynamic_combined = pd.DataFrame(results_dynamic_combined)
        csv_file_name = (f"dynamic_combined_results_base_{base_threshold}_refine_{refine_threshold}.csv")
        save_to_csv_dynamic_combined(df_dynamic_combined, csv_file_name)
        results_dynamic_all.extend(results_dynamic)  # Aggregate all results for summary if needed
        csv_file_name = (f"dynamic_results_base_{base_threshold}_refine_{refine_threshold}.csv")
        save_to_csv_dynamic_randomized(df_dynamic, csv_file_name)
        results_dynamic_combined_all.extend(results_dynamic_combined)
    
    for i, (G, num_vertices, edge_prob) in enumerate(graphs_with_metadata):
        graph_file = f"graphs/graphml/graph_num_vertices_{num_vertices}_percentage_{edge_prob}.graphml"

        # randomized Search
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

        # Draw and save graphs with marked solutions if vertices are small
        if num_vertices <= 8:
            randomized_edges = [(u, v) for u, v, w in randomized__set]
            draw_and_save_graph(
                graph_file, randomized_edges, num_vertices, edge_prob, 
                "randomized", "Randomized Solution"
            )


    # Optional: Save all results to a combined CSV
    df_dynamic_all = pd.DataFrame(results_dynamic_all)
    df_dynamic_combined_all = pd.DataFrame(results_dynamic_combined_all)
    df_randomized = pd.DataFrame(results_randomized)
    save_to_csv_dynamic_combined(df_dynamic_combined_all, "dynamic_combined_results_combined.csv")
    save_to_csv_dynamic_randomized(df_dynamic_all, "dynamic_results_combined.csv")
    save_to_csv(df_randomized, "randomized_results.csv")

    # Perform analysis
    # Load exhaustive results
    exhaustive_df = load_exhaustive_results()

    # Load dynamic results
    dynamic_df = load_dynamic_results()
    dynamic_combined_df = load_dynamic_combined_results()
    randomized_df = pd.read_csv("results/randomized_results.csv")

    greedy_df = pd.read_csv("results/greedy_results.csv")

    # Accuracy
    plot_accuracy(exhaustive_df, dynamic_df, greedy_df, algorithm_type="dynamic")
    plot_accuracy(exhaustive_df, dynamic_combined_df, greedy_df, algorithm_type="dynamic_combined")
    plot_accuracy(exhaustive_df, randomized_df, greedy_df, algorithm_type="randomized")

    #Weight
    plot_weight_comparison_for_density_50(exhaustive_df, dynamic_df, greedy_df, algorithm_type="dynamic")
    plot_weight_comparison_for_density_50(exhaustive_df, dynamic_combined_df, greedy_df, algorithm_type="dynamic_combined")
    plot_weight_comparison_for_density_50(exhaustive_df, randomized_df, greedy_df, algorithm_type="randomized")

    #Solution Size
    plot_solution_size_bar_chart(dynamic_df, "dynamic")
    plot_solution_size_bar_chart(randomized_df, "randomized")
    plot_solution_size_bar_chart(dynamic_combined_df, "dynamic_combined")
    

#     # executions_times(df_randomized, "Randomized Search")
#     # executions_times(df_dynamic, "Randomized Heuristic")

#     # basic_operations_num(df_randomized, "Randomized Search")
#     # basic_operations_num(df_dynamic, "Randomized Heuristic")
#     # basic_operations_num_aggregated(df_randomized, df_dynamic)

#     # plot_time_complexity(df_randomized, df_dynamic)

#     # predict_large_graph_times_75(df_randomized, df_dynamic, [8, 9, 10, 15, 20, 25, 30])
#     # predict_large_graph_space([8, 9, 10, 15, 20, 25, 30])


if __name__ == "__main__":
    print("Creating graphs for Minimum Weight Edge Dominating Set problem...")
    main()
