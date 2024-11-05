import pandas as pd
import matplotlib.pyplot as plt

def save_to_csv(df, filename):
    df.to_csv(f"results/{filename}", index=False)
    print(f"Results saved to {filename}")

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

def compare_solutions(comparison_df):
    unique_percentages = comparison_df['percentage_max_num_edges'].unique()
    
    for percentage in unique_percentages:
        subset = comparison_df[comparison_df['percentage_max_num_edges'] == percentage]

        # Total weight comparison
        plt.plot(subset['vertices_num'], subset['exhaustive_total_weight'], marker='+', color='red', label='Exhaustive Search')
        plt.plot(subset['vertices_num'], subset['greedy_total_weight'], marker='x', color='blue', label='Greedy Heuristic')
        plt.title(f"Total Weight Comparison - {percentage*100}% Edge Density")
        plt.xlabel("Number of Vertices")
        plt.ylabel("Total Weight")
        plt.legend()
        plt.savefig(f"graphics/total_weight_comparison_{int(percentage*100)}.png")
        plt.clf()

        # Execution time ratio
        plt.plot(subset['vertices_num'], subset['time_ratio'], marker='o', color='purple')
        plt.title(f"Execution Time Ratio (Greedy / Exhaustive) - {percentage*100}% Edge Density")
        plt.xlabel("Number of Vertices")
        plt.ylabel("Time Ratio (Greedy / Exhaustive)")
        plt.savefig(f"graphics/execution_time_ratio_{int(percentage*100)}.png")
        plt.clf()
