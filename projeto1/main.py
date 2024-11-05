import pandas as pd
import time
from graph_generation import generate_weighted_graph, read_arguments
from algorithms import exhaustive_search_mweds, greedy_mweds
from analysis import executions_times, basic_operations_num, compare_solutions, save_to_csv

def main():
    results_exhaustive = []
    results_greedy = []
    comparison_results = []

    vertices_num_last_graph, max_value_coordinate = read_arguments()
    graphs_with_metadata = generate_weighted_graph(vertices_num_last_graph, max_value_coordinate)
    
    for G, num_vertices, edge_prob in graphs_with_metadata:
        # Exhaustive Search
        start_time = time.time()
        exhaustive_set, exhaustive_weight = exhaustive_search_mweds(G)
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
        
        # Greedy Heuristic
        start_time = time.time()
        greedy_set, greedy_weight = greedy_mweds(G)
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
