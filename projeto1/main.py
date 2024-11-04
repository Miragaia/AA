import pandas as pd
import time
from graph_generation import generate_weighted_graph, read_arguments
from algorithms import exhaustive_search_mweds, greedy_mweds
from analysis import executions_times, basic_operations_num, compare_solutions

def main():
    seed = 12345  # Example seed value
    results_exhaustive = []
    results_greedy = []

    vertices_num_last_graph, max_value_coordinate = read_arguments()
    G = generate_weighted_graph(vertices_num_last_graph, max_value_coordinate)
    
    # Exhaustive Search
    start_time = time.time()
    exhaustive_set, exhaustive_weight = exhaustive_search_mweds(G)
    end_time = time.time()
    results_exhaustive.append({
        # 'vertices_num': num_vertices,
        # 'percentage_max_num_edges': edge_prob,
        'total_weight': exhaustive_weight,
        'solution_size': len(exhaustive_set),
        'execution_time': end_time - start_time,
        'num_operations': len(exhaustive_set)
    })
    
    # Greedy Heuristic
    start_time = time.time()
    greedy_set, greedy_weight = greedy_mweds(G)
    end_time = time.time()
    results_greedy.append({
        # 'vertices_num': num_vertices,
        # 'percentage_max_num_edges': edge_prob,
        'total_weight': greedy_weight,
        'solution_size': len(greedy_set),
        'execution_time': end_time - start_time,
        'num_operations': len(greedy_set)
    })

    df_exhaustive = pd.DataFrame(results_exhaustive)
    df_greedy = pd.DataFrame(results_greedy)
    
    executions_times(df_exhaustive, "Exhaustive Search")
    executions_times(df_greedy, "Greedy Heuristic")
    basic_operations_num(df_exhaustive, "Exhaustive Search")
    basic_operations_num(df_greedy, "Greedy Heuristic")
    compare_solutions(df_exhaustive, df_greedy)

if __name__ == "__main__":
    # vertices_num_last_graph, max_value_coordinate = read_arguments()
    print("Creating graphs for Minimum Weight Edge Dominating Set problem...")
    # generate_weighted_graph(vertices_num_last_graph, max_value_coordinate)
    main()
