import pandas as pd
import time
import cProfile
import networkx as nx
import matplotlib.pyplot as plt
import os
from graph_generation import generate_weighted_graph, read_arguments, load_graphs_with_metadata, store_internet_graph
from algorithms import dynamic_randomized_mweds, dynamic_combined_mweds
from analysis import save_to_csv, save_to_csv_dynamic_combined, save_to_csv_dynamic_randomized, load_exhaustive_results, load_dynamic_results, load_dynamic_combined_results, plot_accuracy, plot_weight_comparison_for_density_50, plot_solution_size_bar_chart, plot_execution_times, plot_basic_operations, plot_weight_comparison

def draw_and_save_graph(graph_file, edge_set, num_vertices, percentage, algorithm_type, title):
    """
    Draws the graph with all edges showing weights, highlights edges in edge_set in red, 
    and saves as PNG with the specified naming convention.
    """

    os.makedirs("graphs_solution", exist_ok=True)

    G = nx.read_graphml(graph_file)

    if all('x' in G.nodes[node] and 'y' in G.nodes[node] for node in G.nodes()):
        pos = {node: (G.nodes[node]['x'], G.nodes[node]['y']) for node in G.nodes()}
    else:
        pos = nx.spring_layout(G)

    plt.figure(figsize=(8, 8))

    edge_set = [(str(u), str(v)) for u, v in edge_set]

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

    threshold_pairs = [
        (0.125, 0.25),
        (0.5, 0.75),
        (0.25, 0.5)
    ]

    graph_source = input("Select graph source (1 for created graphs, 2 for internet graphs): ")
    if graph_source not in ["1", "2"]:
        raise ValueError("Invalid selection. Choose 1 or 2.")

    if graph_source == "1":

        vertices_num_last_graph = int(input("Enter the number of vertices (must be greater than 3): "))
        if vertices_num_last_graph <= 3:
            raise ValueError("The number of vertices must be greater than 3.")
        
        max_value_coordinate = 1000

        graphs_with_metadata = generate_weighted_graph(vertices_num_last_graph, max_value_coordinate)
        is_generated = True
        save_path = "created_graphs"
    else:
        graphs_with_metadata = load_graphs_with_metadata()
        is_generated = False
        save_path = "internet_graphs"

    for base_threshold, refine_threshold in threshold_pairs:
        results_dynamic = []
        results_dynamic_combined = []

        for i, graph_data in enumerate(graphs_with_metadata):
            if is_generated:
                G, num_vertices, edge_prob = graph_data
                graph_file = f"graphs/{save_path}/graphml/graph_num_vertices_{num_vertices}_percentage_{edge_prob}.graphml"
            else:
                G, num_vertices, num_edges = graph_data
                edge_prob = None 
                graph_file = f"graphs/{save_path}/graphml/graph_num_vertices_{num_vertices}_num_edges_{num_edges}.graphml"

            start_time = time.time()
            dynamic_set, dynamic_weight, dynamic_operations, dynamic_configurations = dynamic_randomized_mweds(
                G, base_threshold=base_threshold, refine_threshold=refine_threshold
            )
            end_time = time.time()
            dynamic_time = end_time - start_time

            dynamic_result = {
                'vertices_num': num_vertices,
                'total_weight': dynamic_weight,
                'solution_size': len(dynamic_set),
                'execution_time': dynamic_time,
                'num_operations': dynamic_operations,
                'dynamic_configurations': dynamic_configurations,
                'base_threshold': base_threshold,
                'refine_threshold': refine_threshold
            }
            if is_generated:
                dynamic_result['percentage_max_num_edges'] = edge_prob 
            else:
                dynamic_result['num_edges'] = num_edges
            results_dynamic.append(dynamic_result)

            start_time = time.time()
            dynamic_combined_set, dynamic_combined_weight, dynamic_combined_operations, dynamic_combined_configurations = dynamic_combined_mweds(
                G, base_threshold=base_threshold, refine_threshold=refine_threshold
            )
            end_time = time.time()
            dynamic_combined_time = end_time - start_time

            dynamic_combined_result = {
                'vertices_num': num_vertices,
                'total_weight': dynamic_combined_weight,
                'solution_size': len(dynamic_combined_set),
                'execution_time': dynamic_combined_time,
                'num_operations': dynamic_combined_operations,
                'dynamic_combined_configurations': dynamic_combined_configurations,
                'base_threshold': base_threshold,
                'refine_threshold': refine_threshold
            }
            if is_generated:
                dynamic_combined_result['percentage_max_num_edges'] = edge_prob 
            else:
                dynamic_combined_result['num_edges'] = num_edges  
            results_dynamic_combined.append(dynamic_combined_result)

            if num_vertices <= 8:
                dynamic_edges = [(u, v) for u, v, w in dynamic_set]
                title = f"Randomized Heuristic Solution ({'Generated' if is_generated else 'Internet'})"

            if not is_generated:
                store_internet_graph(G, num_vertices, num_edges)
                graph_file = f"graphs/internet_graphs/graphml/graph_num_vertices_{num_vertices}_num_edges_{num_edges}.graphml"


                draw_and_save_graph(
                    graph_file, dynamic_edges, num_vertices, edge_prob if edge_prob is not None else "NA", 
                    f"{save_path}/dynamic_base_{base_threshold}_refine_{refine_threshold}", 
                    title
                )

        df_dynamic = pd.DataFrame(results_dynamic)
        df_dynamic_combined = pd.DataFrame(results_dynamic_combined)

        dynamic_csv_file_name = f"{save_path}/dynamic_results_base_{base_threshold}_refine_{refine_threshold}.csv"
        save_to_csv_dynamic_randomized(df_dynamic, dynamic_csv_file_name)

        dynamic_combined_csv_file_name = f"{save_path}/dynamic_combined_results_base_{base_threshold}_refine_{refine_threshold}.csv"
        save_to_csv_dynamic_combined(df_dynamic_combined, dynamic_combined_csv_file_name)

        results_dynamic_all.extend(results_dynamic)
        results_dynamic_combined_all.extend(results_dynamic_combined)

    df_dynamic_all = pd.DataFrame(results_dynamic_all)
    df_dynamic_combined_all = pd.DataFrame(results_dynamic_combined_all)

    save_to_csv_dynamic_randomized(df_dynamic_all, f"{save_path}/dynamic_results_combined.csv")
    save_to_csv_dynamic_combined(df_dynamic_combined_all, f"{save_path}/dynamic_combined_results_combined.csv")

    # Perform analysis
    # Load exhaustive results
    exhaustive_df = load_exhaustive_results()

    # Load dynamic results
    dynamic_df = load_dynamic_results()
    dynamic_combined_df = load_dynamic_combined_results()
    greedy_df = pd.read_csv("results/greedy_results.csv")

    # Accuracy
    plot_accuracy(exhaustive_df, dynamic_df, greedy_df, algorithm_type="dynamic")
    plot_accuracy(exhaustive_df, dynamic_combined_df, greedy_df, algorithm_type="dynamic_combined")

    # Weight
    plot_weight_comparison_for_density_50(exhaustive_df, dynamic_df, greedy_df, algorithm_type="dynamic")
    plot_weight_comparison_for_density_50(exhaustive_df, dynamic_combined_df, greedy_df, algorithm_type="dynamic_combined")

    # Solution Size
    plot_solution_size_bar_chart(dynamic_df, "dynamic")
    plot_solution_size_bar_chart(dynamic_combined_df, "dynamic_combined")

    # Execution Time
    plot_execution_times(dynamic_df, "dynamic")
    plot_execution_times(dynamic_combined_df, "dynamic_combined")

    # Basic Operations
    plot_basic_operations(dynamic_df, "dynamic")
    plot_basic_operations(dynamic_combined_df, "dynamic_combined")

    plot_weight_comparison(dynamic_combined_df, dynamic_df)


if __name__ == "__main__":
    print("Creating graphs for Minimum Weight Edge Dominating Set problem...")
    main()

