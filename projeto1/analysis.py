import pandas as pd
import matplotlib.pyplot as plt

def save_to_csv(df, filename):
    df.to_csv(f"results/{filename}", index=False)
    print(f"Results saved to {filename}")

def executions_times(df, algorithm_name):
    # Loop through each unique edge density and plot separately
    unique_densities = df['percentage_max_num_edges'].unique()
    for density in unique_densities:
        subset = df[df['percentage_max_num_edges'] == density]
        plt.plot(subset['vertices_num'], subset['execution_time'], marker='o', label=f"{algorithm_name} - {int(density * 100)}%")
    
    plt.xlabel("Number of Vertices")
    plt.ylabel("Execution Time (s)")
    plt.title(f"Execution Time - {algorithm_name}")
    plt.legend()
    plt.savefig(f"graphics/{algorithm_name}_execution_times.png")
    plt.clf()

def basic_operations_num(df, algorithm_name):
    unique_densities = df['percentage_max_num_edges'].unique()
    plt.figure(figsize=(10, 6))

    for density in unique_densities:
        subset = df[df['percentage_max_num_edges'] == density]
        plt.plot(subset['vertices_num'], subset['num_operations'], marker='o', linestyle='-', label=f"{int(density * 100)}% Density")
    
    plt.xlabel('Number of Vertices')
    plt.ylabel('Number of Basic Operations')
    plt.title(f'Basic Operations Count for {algorithm_name}')
    plt.legend()
    plt.savefig(f"graphics/{algorithm_name}_basic_ops.png")
    plt.clf()

def plot_time_complexity(df_exhaustive, df_greedy):
    plt.figure(figsize=(10, 6))

    # Plot time complexity for each density separately
    for density in df_exhaustive['percentage_max_num_edges'].unique():
        subset_exhaustive = df_exhaustive[df_exhaustive['percentage_max_num_edges'] == density]
        subset_greedy = df_greedy[df_greedy['percentage_max_num_edges'] == density]

        plt.plot(subset_exhaustive['vertices_num'], subset_exhaustive['execution_time'], label=f'Exhaustive - {int(density * 100)}% Density', marker='o')
        plt.plot(subset_greedy['vertices_num'], subset_greedy['execution_time'], label=f'Greedy - {int(density * 100)}% Density', marker='x')

    plt.xlabel('Number of Vertices')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Time Complexity by Number of Vertices')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.savefig("graphics/time_complexity_plot.png")
    plt.clf()

def compare_solutions(comparison_df):
    unique_percentages = comparison_df['percentage_max_num_edges'].unique()
    
    for percentage in unique_percentages:
        subset = comparison_df[comparison_df['percentage_max_num_edges'] == percentage]

        # Total weight comparison
        plt.plot(subset['vertices_num'], subset['exhaustive_total_weight'], marker='+', color='red', label='Exhaustive Search')
        plt.plot(subset['vertices_num'], subset['greedy_total_weight'], marker='x', color='blue', label='Greedy Heuristic')
        plt.title(f"Total Weight Comparison - {int(percentage * 100)}% Edge Density")
        plt.xlabel("Number of Vertices")
        plt.ylabel("Total Weight")
        plt.legend()
        plt.savefig(f"graphics/total_weight_comparison_{int(percentage * 100)}.png")
        plt.clf()

        # Execution time ratio
        plt.plot(subset['vertices_num'], subset['time_ratio'], marker='o', color='purple')
        plt.title(f"Execution Time Ratio (Greedy / Exhaustive) - {int(percentage * 100)}% Edge Density")
        plt.xlabel("Number of Vertices")
        plt.ylabel("Time Ratio (Greedy / Exhaustive)")
        plt.savefig(f"graphics/execution_time_ratio_{int(percentage * 100)}.png")
        plt.clf()
