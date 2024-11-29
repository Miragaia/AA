import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def save_to_csv(df, filename):
    df.to_csv(f"results/{filename}", index=False)
    print(f"Results saved to {filename}")

def save_to_csv_dynamic_randomized(df, filename):
    df.to_csv(f"results/dynamic/randomized/{filename}", index=False)
    print(f"Results saved to {filename}")

def save_to_csv_dynamic_combined(df, filename):
    df.to_csv(f"results/dynamic/combined/{filename}", index=False)
    print(f"Results saved to {filename}")

def load_exhaustive_results():
    """Load the exhaustive search results from CSV."""
    return pd.read_csv("results/exhaustive_results.csv")

def load_dynamic_results():
    """Load dynamic results from the specified folder."""
    dynamic_results = []
    for file_name in os.listdir("results/dynamic/randomized"):
        if file_name.endswith(".csv"):
            file_path = os.path.join("results/dynamic/randomized", file_name)
            dynamic_results.append(pd.read_csv(file_path))
    return pd.concat(dynamic_results, ignore_index=True)

def load_dynamic_combined_results():
    """Load dynamic results from the specified folder."""
    dynamic_results = []
    for file_name in os.listdir("results/dynamic/combined"):
        if file_name.endswith(".csv"):
            file_path = os.path.join("results/dynamic/combined", file_name)
            dynamic_results.append(pd.read_csv(file_path))
    return pd.concat(dynamic_results, ignore_index=True)

def plot_accuracy(exhaustive_df, dynamic_df, greedy_df):
    """
    Plots the accuracy of dynamic and greedy algorithms compared to exhaustive results as separate line charts for different edge densities.
    Accuracy is calculated as:
    Accuracy = 100 * (1 - abs(Algorithm Total Weight - Exhaustive Total Weight) / Exhaustive Total Weight)
    """
    # Merge the exhaustive, dynamic, and greedy results
    dynamic_merged = pd.merge(exhaustive_df, dynamic_df, on=["vertices_num", "percentage_max_num_edges"], suffixes=('_exhaustive', '_dynamic'))
    greedy_merged = pd.merge(exhaustive_df, greedy_df, on=["vertices_num", "percentage_max_num_edges"], suffixes=('_exhaustive', '_greedy'))

    # Calculate accuracy for dynamic and greedy
    dynamic_merged['dynamic_accuracy'] = 100 * (1 - abs(dynamic_merged['total_weight_dynamic'] - dynamic_merged['total_weight_exhaustive']) / dynamic_merged['total_weight_exhaustive'])
    greedy_merged['greedy_accuracy'] = 100 * (1 - abs(greedy_merged['total_weight_greedy'] - greedy_merged['total_weight_exhaustive']) / greedy_merged['total_weight_exhaustive'])

    # Get unique edge densities
    unique_densities = exhaustive_df['percentage_max_num_edges'].unique()

    # Loop through each edge density and plot accuracy separately
    for density in unique_densities:
        plt.figure(figsize=(10, 6))
        
        # Filter data based on current edge density
        dynamic_subset = dynamic_merged[dynamic_merged['percentage_max_num_edges'] == density]
        greedy_subset = greedy_merged[greedy_merged['percentage_max_num_edges'] == density]
        
        # Plot dynamic accuracy for each threshold pair
        threshold_pairs = dynamic_subset[['base_threshold', 'refine_threshold']].drop_duplicates()
        for _, thresholds in threshold_pairs.iterrows():
            base_threshold = thresholds['base_threshold']
            refine_threshold = thresholds['refine_threshold']
            threshold_subset = dynamic_subset[(dynamic_subset['base_threshold'] == base_threshold) & 
                                              (dynamic_subset['refine_threshold'] == refine_threshold)]
            plt.plot(threshold_subset['vertices_num'], threshold_subset['dynamic_accuracy'], 
                     marker='o', label=f'Dynamic: Base {base_threshold}, Refine {refine_threshold}')
        
        # Plot greedy accuracy as a single line
        plt.plot(greedy_subset['vertices_num'], greedy_subset['greedy_accuracy'], 
                 marker='s', linestyle='--', color='orange', label='Greedy Algorithm')
        
        # Customize plot labels and title
        plt.xlabel('Number of Vertices')
        plt.ylabel('Accuracy (%)')
        plt.title(f'Algorithm Accuracy Compared to Exhaustive Search (Density {int(density * 100)}%)')
        plt.legend()
        plt.grid(True)

        # Save the plot to a separate file for this density
        plt.savefig(f"graphics/accuracy/algorithm_accuracy_density_{int(density * 100)}.png")
        plt.clf()
    
def plot_weight_comparison_for_density_50(exhaustive_df, dynamic_df, greedy_df):
    """
    Creates a bar plot comparing the weights of the set for exhaustive, greedy, and all dynamic configurations
    for a specific edge density of 50%.
    """
    # Filter data for 50% density
    density = 0.5
    exhaustive_subset = exhaustive_df[exhaustive_df['percentage_max_num_edges'] == density]
    dynamic_subset = dynamic_df[dynamic_df['percentage_max_num_edges'] == density]
    greedy_subset = greedy_df[greedy_df['percentage_max_num_edges'] == density]

    # Prepare data for plotting
    vertices = sorted(exhaustive_subset['vertices_num'].unique())
    bar_width = 0.2  # Width of each bar
    x_positions = np.arange(len(vertices))  # Base positions for bars

    # Plot exhaustive weights
    exhaustive_weights = exhaustive_subset.set_index('vertices_num')['total_weight']
    plt.bar(x_positions, exhaustive_weights, bar_width, label='Exhaustive', color='blue')

    # Plot greedy weights
    greedy_weights = greedy_subset.set_index('vertices_num')['total_weight']
    plt.bar(x_positions + bar_width, greedy_weights, bar_width, label='Greedy', color='orange')

    # Plot dynamic weights (average for each configuration)
    dynamic_weights = []
    for v in vertices:
        dynamic_for_vertex = dynamic_subset[dynamic_subset['vertices_num'] == v]
        dynamic_weights.append(dynamic_for_vertex['total_weight'].mean())
    plt.bar(x_positions + 2 * bar_width, dynamic_weights, bar_width, label='Dynamic (Avg)', color='green')

    # Customize the plot
    plt.xlabel('Number of Vertices')
    plt.ylabel('Total Weight')
    plt.title('Weight Comparison for Density 50%')
    plt.xticks(x_positions + bar_width, vertices)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the plot
    plt.tight_layout()
    plt.savefig("graphics/weight/weight_comparison_density_50.png")
    plt.clf()

import pandas as pd
import matplotlib.pyplot as plt

def plot_solution_size_bar_chart():
    """
    Reads a CSV file and plots a bar chart of the occurrences of `solution_size`.
    """
    # Read the CSV file
    try:
        data = pd.read_csv("results/dynamic/randomized/dynamic_results_combined.csv")
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return

    # Check if 'solution_size' column exists
    if 'solution_size' not in data.columns:
        print("The column 'solution_size' is not present in the dataset.")
        return

    # Calculate frequencies of solution_size values
    frequency_counts = data['solution_size'].value_counts().sort_index()

    # Plot the bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(frequency_counts.index, frequency_counts.values, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title('Bar Chart of Solution Size Occurrences', fontsize=14)
    plt.xlabel('Solution Size', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(axis='y', alpha=0.75)
    plt.xticks(frequency_counts.index)
    plt.tight_layout()
    plt.savefig("graphics/solution_size/solution_size_bar_chart.png")
    plt.clf()

