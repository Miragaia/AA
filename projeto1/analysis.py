import pandas as pd
import matplotlib.pyplot as plt

def executions_times(df, algorithm_name):
    plt.plot(df['vertices_num'], df['execution_time'], marker='o', label=algorithm_name)
    plt.xlabel("Number of Vertices")
    plt.ylabel("Execution Time (s)")
    plt.title(f"Execution Time - {algorithm_name}")
    plt.legend()
    plt.savefig(f"graphics/{algorithm_name}_execution_times.png")
    plt.clf()

def basic_operations_num(df, algorithm_name):
    plt.plot(df['vertices_num'], df['num_operations'], marker='o', label=algorithm_name)
    plt.xlabel("Number of Vertices")
    plt.ylabel("Number of Basic Operations")
    plt.title(f"Basic Operations - {algorithm_name}")
    plt.legend()
    plt.savefig(f"graphics/{algorithm_name}_basic_operations.png")
    plt.clf()

def compare_solutions(exhaustive_search, greedy):
    for percentage in [0.125, 0.25, 0.50, 0.75]:
        plt.scatter(exhaustive_search['vertices_num'][exhaustive_search['percentage_max_num_edges'] == percentage],
                    exhaustive_search['total_weight'][exhaustive_search['percentage_max_num_edges'] == percentage], 
                    c="r", marker="+", label="Exhaustive Search")
        
        plt.scatter(greedy['vertices_num'][greedy['percentage_max_num_edges'] == percentage],
                    greedy['total_weight'][greedy['percentage_max_num_edges'] == percentage], 
                    c="b", marker="x", label="Greedy")
        
        plt.legend()
        plt.title(f'Total Weight for each Experiment with {percentage*100}% Edges')
        plt.xlabel('Vertices Number')
        plt.ylabel('Total Weight')
        plt.savefig(f"graphics/total_weights_percentage_{percentage}.png")
        plt.clf()
